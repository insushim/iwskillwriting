#!/usr/bin/env python3
"""
Book Writer - Phase 7: Blurb & Synopsis Generator
블러브(소개글), 시놉시스, 투고용 패키지를 자동 생성합니다.

기능:
- 3종 블러브 (짧은/중간/긴)
- 투고용 시놉시스 (1페이지/3페이지)
- 로그라인 (1문장)
- 투고용 샘플 패키지 (첫 3챕터 + 시놉시스)
- 키워드 추출 (KDP/한국 플랫폼용)
"""

import json
import re
import sys
from pathlib import Path
from datetime import datetime
from collections import Counter


class BlurbGenerator:
    def __init__(self, project_dir: str):
        self.project_dir = Path(project_dir)
        self.config = self._load_config()
        self.chapters = self._load_chapters()
        self.codex = self._load_codex()

    def _load_config(self) -> dict:
        with open(self.project_dir / "project.json", "r", encoding="utf-8") as f:
            return json.load(f)

    def _load_chapters(self) -> list:
        chapters_dir = self.project_dir / "chapters"
        chapters = []
        for ch_file in sorted(chapters_dir.glob("ch*.md")):
            content = ch_file.read_text(encoding="utf-8")
            body = content
            if content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    body = parts[2].strip()
            chapters.append({
                "num": int(re.search(r'\d+', ch_file.stem).group()),
                "content": body,
            })
        return chapters

    def _load_codex(self) -> dict:
        codex_dir = self.project_dir / "codex"
        codex = {}
        if codex_dir.exists():
            for f in codex_dir.glob("*.md"):
                codex[f.stem] = f.read_text(encoding="utf-8")
        return codex

    def generate_all(self) -> dict:
        """모든 마케팅 자료를 생성합니다."""
        results = {}

        # 1. 키워드 추출
        results["keywords"] = self.extract_keywords()

        # 2. 블러브 프롬프트 생성 (Claude가 실제 작성)
        results["blurb_prompts"] = self.generate_blurb_prompts()

        # 3. 시놉시스 소재 추출
        results["synopsis_material"] = self.extract_synopsis_material()

        # 4. 투고용 샘플 패키지
        results["submission_package"] = self.create_submission_package()

        # 5. 메타데이터 생성
        results["metadata"] = self.generate_metadata()

        self._save_results(results)
        return results

    def extract_keywords(self, top_n: int = 20) -> dict:
        """원고에서 핵심 키워드를 추출합니다."""
        all_text = " ".join(ch["content"] for ch in self.chapters)

        # 2-4글자 단어 빈도
        words = re.findall(r'[가-힣]{2,4}', all_text)
        word_freq = Counter(words)

        # 불용어 제거
        stopwords = {
            "그리고", "하지만", "그래서", "때문에", "그러나", "그런데",
            "있었다", "없었다", "했다", "되었다", "것이다", "않았다",
            "그녀가", "그녀의", "그녀는", "그녀를",
            "자신의", "자신이", "자신을", "자신은",
            "그것은", "이것은", "저것은",
        }
        for sw in stopwords:
            word_freq.pop(sw, None)

        top_words = word_freq.most_common(top_n)

        # 장르 키워드 매핑
        genre = self.config.get("genre", "")
        genre_keywords = self._get_genre_keywords(genre)

        return {
            "extracted": [{"word": w, "count": c} for w, c in top_words],
            "genre_suggested": genre_keywords,
            "kdp_keywords": genre_keywords[:7],  # KDP 최대 7개
        }

    def _get_genre_keywords(self, genre: str) -> list:
        """장르별 추천 키워드를 반환합니다."""
        keyword_map = {
            "fantasy": ["판타지소설", "마법", "모험", "이세계", "퀘스트", "드래곤", "성장"],
            "romance": ["로맨스소설", "사랑", "운명", "재회", "달콤한", "가슴설레는", "로맨틱"],
            "thriller": ["스릴러", "추리", "범죄", "미스터리", "반전", "긴장감", "서스펜스"],
            "sf": ["SF소설", "과학소설", "미래", "우주", "인공지능", "디스토피아", "사이버펑크"],
            "horror": ["호러소설", "공포", "초자연", "심리공포", "괴담", "저주", "유령"],
            "self_help": ["자기계발", "습관", "성공", "동기부여", "마인드셋", "성장", "실전"],
            "ya": ["청소년소설", "성장소설", "학교", "우정", "첫사랑", "모험", "정체성"],
            "children": ["동화", "어린이", "모험", "우정", "용기", "교훈", "상상력"],
        }
        return keyword_map.get(genre, ["소설", "한국소설", "신작", "베스트셀러"])

    def generate_blurb_prompts(self) -> dict:
        """블러브 생성을 위한 프롬프트를 생성합니다."""
        # 핵심 정보 수집
        title = self.config.get("title", "")
        genre = self.config.get("genre", "")
        core_idea = self.config.get("core_idea", "")

        # 첫 3챕터 요약
        first_chapters = ""
        for ch in self.chapters[:3]:
            first_chapters += ch["content"][:500] + "\n\n"

        # 캐릭터 정보
        characters_info = self.codex.get("characters", "")[:1000]

        base_context = f"""
제목: {title}
장르: {genre}
핵심 아이디어: {core_idea}
캐릭터: {characters_info[:500]}
첫 3챕터 발췌: {first_chapters[:1000]}
"""

        return {
            "short_blurb": {
                "target_length": "50-80자",
                "purpose": "온라인 서점 한 줄 소개",
                "prompt": f"다음 소설의 한 줄 소개를 50-80자로 작성하세요. 핵심 갈등과 매력을 담아주세요.\n{base_context}",
            },
            "medium_blurb": {
                "target_length": "200-300자",
                "purpose": "온라인 서점 소개글",
                "prompt": f"다음 소설의 소개글을 200-300자로 작성하세요. 구조: 배경→주인공→갈등→후크(질문/궁금증 유발).\n{base_context}",
            },
            "long_blurb": {
                "target_length": "500-800자",
                "purpose": "상세 소개 / 프로모션용",
                "prompt": f"다음 소설의 상세 소개를 500-800자로 작성하세요. 구조: 세계관→주인공 소개→핵심 갈등→판돈→후크. 스포일러 없이.\n{base_context}",
            },
            "logline": {
                "target_length": "25자 이내",
                "purpose": "로그라인 (한 문장 요약)",
                "prompt": f"다음 소설의 로그라인을 25자 이내로 작성하세요. 형식: '[주인공]이 [상황]에서 [목표]를 위해 [행동]하는 이야기'.\n{base_context}",
            },
        }

    def extract_synopsis_material(self) -> dict:
        """시놉시스 작성에 필요한 소재를 추출합니다."""
        # 각 챕터의 첫 문장과 마지막 문장
        chapter_summaries = []
        for ch in self.chapters:
            lines = [l.strip() for l in ch["content"].split("\n") if l.strip() and not l.startswith("#")]
            first_line = lines[0] if lines else ""
            last_line = lines[-1] if lines else ""

            chapter_summaries.append({
                "chapter": ch["num"],
                "first_line": first_line[:100],
                "last_line": last_line[:100],
                "wordcount": len(ch["content"]),
            })

        return {
            "title": self.config.get("title", ""),
            "genre": self.config.get("genre", ""),
            "total_chapters": len(self.chapters),
            "total_wordcount": sum(len(ch["content"]) for ch in self.chapters),
            "chapter_summaries": chapter_summaries,
            "characters": self.codex.get("characters", "")[:2000],
            "themes": self.codex.get("themes", "")[:1000],
        }

    def create_submission_package(self) -> dict:
        """투고용 샘플 패키지를 생성합니다."""
        output_dir = self.project_dir / "output"
        output_dir.mkdir(parents=True, exist_ok=True)

        # 첫 3챕터 추출
        sample_content = f"# {self.config.get('title', '')} — 투고용 샘플\n\n"
        sample_content += f"**장르**: {self.config.get('genre', '')}\n"
        sample_content += f"**분량**: {sum(len(ch['content']) for ch in self.chapters):,}자\n\n"
        sample_content += "---\n\n"

        for ch in self.chapters[:3]:
            sample_content += ch["content"] + "\n\n---\n\n"

        sample_path = output_dir / f"{self.config.get('title', 'sample')}_투고샘플.md"
        with open(sample_path, "w", encoding="utf-8") as f:
            f.write(sample_content)

        return {
            "sample_path": str(sample_path),
            "sample_chapters": min(3, len(self.chapters)),
            "sample_wordcount": sum(len(ch["content"]) for ch in self.chapters[:3]),
        }

    def generate_metadata(self) -> dict:
        """출판 메타데이터를 생성합니다."""
        genre = self.config.get("genre", "")

        # BISAC 코드 매핑
        bisac_map = {
            "fantasy": "FIC009020",  # FICTION / Fantasy / Epic
            "romance": "FIC027020",  # FICTION / Romance / Contemporary
            "thriller": "FIC031010",  # FICTION / Thrillers / Crime
            "mystery": "FIC022000",  # FICTION / Mystery & Detective
            "sf": "FIC028010",       # FICTION / Science Fiction / General
            "horror": "FIC015000",   # FICTION / Horror
            "literary": "FIC019000", # FICTION / Literary
            "ya": "YAF019000",       # YA FICTION / Fantasy
            "children": "JUV037000", # JUVENILE FICTION / Fantasy & Magic
            "self_help": "SEL027000",# SELF-HELP / Personal Growth
            "business": "BUS071000", # BUSINESS / Leadership
        }

        return {
            "title": self.config.get("title", ""),
            "subtitle": self.config.get("subtitle", ""),
            "author": self.config.get("author", ""),
            "language": self.config.get("language", "ko"),
            "genre": genre,
            "bisac_code": bisac_map.get(genre, "FIC000000"),
            "target_audience": self.config.get("target_audience", ""),
            "wordcount": sum(len(ch["content"]) for ch in self.chapters),
            "chapter_count": len(self.chapters),
        }

    def _save_results(self, results: dict):
        output_dir = self.project_dir / "output"
        output_dir.mkdir(parents=True, exist_ok=True)

        with open(output_dir / "marketing_package.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        # 마케팅 패키지 마크다운
        md = f"""# 마케팅 패키지: {self.config.get('title', '')}

## 키워드
{', '.join(k['word'] for k in results['keywords']['extracted'][:10])}

## KDP 키워드 (7개)
{', '.join(results['keywords']['kdp_keywords'])}

## 블러브 프롬프트 (Claude에게 전달)

### 한 줄 소개 (50-80자)
> {results['blurb_prompts']['logline']['prompt'][:200]}...

### 짧은 소개 (200-300자)
> {results['blurb_prompts']['short_blurb']['prompt'][:200]}...

### 상세 소개 (500-800자)
> {results['blurb_prompts']['long_blurb']['prompt'][:200]}...

## 메타데이터
- BISAC: {results['metadata']['bisac_code']}
- 분량: {results['metadata']['wordcount']:,}자
- 챕터: {results['metadata']['chapter_count']}개

## 투고용 샘플
- 경로: {results['submission_package']['sample_path']}
- 포함 챕터: {results['submission_package']['sample_chapters']}개
"""
        with open(output_dir / "marketing_package.md", "w", encoding="utf-8") as f:
            f.write(md)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python blurb_generator.py <project_dir>")
        sys.exit(1)

    gen = BlurbGenerator(sys.argv[1])
    results = gen.generate_all()
    print(json.dumps({"keywords": results["keywords"]["kdp_keywords"],
                       "metadata": results["metadata"]}, ensure_ascii=False, indent=2))
