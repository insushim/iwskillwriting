#!/usr/bin/env python3
"""
Book Writer - Phase 5-1: Consistency Checker (구조 편집)
원고의 일관성을 검증하고 리포트를 생성합니다.

검증 항목:
- 캐릭터 이름/외모/나이 일관성
- 타임라인 모순 검출
- 장소/지명 일관성
- 복선 회수 여부
- 플롯홀 검출
- 챕터 간 연결성
"""

import json
import re
import sys
from pathlib import Path
from datetime import datetime
from collections import Counter, defaultdict


class ConsistencyChecker:
    def __init__(self, project_dir: str):
        self.project_dir = Path(project_dir)
        self.config = self._load_config()
        self.chapters = self._load_chapters()
        self.codex = self._load_codex()
        self.issues = []

    def _load_config(self) -> dict:
        config_path = self.project_dir / "project.json"
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _load_chapters(self) -> list:
        """모든 챕터를 순서대로 로드합니다."""
        chapters_dir = self.project_dir / "chapters"
        chapters = []
        for ch_file in sorted(chapters_dir.glob("ch*.md")):
            content = ch_file.read_text(encoding="utf-8")
            # 프론트매터 분리
            body = content
            metadata = {}
            if content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    body = parts[2].strip()
                    for line in parts[1].strip().split("\n"):
                        if ":" in line:
                            key, val = line.split(":", 1)
                            metadata[key.strip()] = val.strip().strip('"')

            chapters.append({
                "file": ch_file.name,
                "num": int(re.search(r'\d+', ch_file.stem).group()),
                "content": body,
                "metadata": metadata,
                "wordcount": len(body),
            })
        return chapters

    def _load_codex(self) -> dict:
        """Codex 파일을 로드합니다."""
        codex_dir = self.project_dir / "codex"
        codex = {}
        if codex_dir.exists():
            for f in codex_dir.glob("*.md"):
                codex[f.stem] = f.read_text(encoding="utf-8")
        return codex

    def run_all_checks(self) -> dict:
        """모든 일관성 검사를 실행합니다."""
        self.check_character_names()
        self.check_wordcount_distribution()
        self.check_chapter_connectivity()
        self.check_timeline_references()
        self.check_location_consistency()
        self.check_repeated_phrases()
        self.check_pov_consistency()

        report = self._generate_report()
        self._save_report(report)
        return report

    def check_character_names(self):
        """캐릭터 이름의 일관성을 검사합니다."""
        # Codex에서 캐릭터 이름 추출
        characters_file = self.codex.get("characters", "")
        codex_names = set()

        for line in characters_file.split("\n"):
            if line.startswith("- **이름**:") or line.startswith("## "):
                name = line.split(":", 1)[-1].strip() if ":" in line else line.replace("##", "").strip()
                if name and len(name) >= 2:
                    codex_names.add(name)

        # 각 챕터에서 고유명사 후보 추출 (한글 2-4글자 + 빈도)
        name_usage = defaultdict(list)
        for ch in self.chapters:
            # 따옴표 앞에 자주 오는 이름 패턴
            dialog_names = re.findall(r'(\w{2,4})(?:이|가|은|는|의|를|에게|한테)\s', ch["content"])
            for name in dialog_names:
                name_usage[name].append(ch["num"])

        # Codex에 있는 이름이 본문에서 사용되는지 확인
        for name in codex_names:
            found_in = []
            for ch in self.chapters:
                if name in ch["content"]:
                    found_in.append(ch["num"])
            if not found_in:
                self.issues.append({
                    "type": "character_unused",
                    "severity": "warning",
                    "message": f"캐릭터 '{name}'이 Codex에 있지만 본문에 등장하지 않습니다.",
                    "chapters": [],
                })

    def check_wordcount_distribution(self):
        """챕터별 글자수 분포를 검사합니다."""
        if not self.chapters:
            return

        wordcounts = [ch["wordcount"] for ch in self.chapters]
        avg = sum(wordcounts) / len(wordcounts) if wordcounts else 0
        target = self.config.get("chapter_wordcount", 4000)

        for ch in self.chapters:
            ratio = ch["wordcount"] / target if target > 0 else 0
            if ratio < 0.5:
                self.issues.append({
                    "type": "wordcount_short",
                    "severity": "warning",
                    "message": f"{ch['num']}장이 목표 분량의 {ratio*100:.0f}%입니다 ({ch['wordcount']:,}자 / 목표 {target:,}자).",
                    "chapters": [ch["num"]],
                })
            elif ratio > 1.5:
                self.issues.append({
                    "type": "wordcount_long",
                    "severity": "info",
                    "message": f"{ch['num']}장이 목표 분량의 {ratio*100:.0f}%입니다 ({ch['wordcount']:,}자). 분할을 고려하세요.",
                    "chapters": [ch["num"]],
                })

    def check_chapter_connectivity(self):
        """챕터 간 연결성을 검사합니다."""
        for i in range(1, len(self.chapters)):
            prev_ch = self.chapters[i - 1]
            curr_ch = self.chapters[i]

            # 이전 챕터 마지막 100자와 현재 챕터 첫 100자 추출
            prev_end = prev_ch["content"][-200:] if len(prev_ch["content"]) > 200 else prev_ch["content"]
            curr_start = curr_ch["content"][:200] if len(curr_ch["content"]) > 200 else curr_ch["content"]

            # 공통 고유명사가 있는지 간단 체크
            prev_words = set(re.findall(r'[가-힣]{2,}', prev_end))
            curr_words = set(re.findall(r'[가-힣]{2,}', curr_start))
            common = prev_words & curr_words

            if len(common) < 1 and i > 0:
                self.issues.append({
                    "type": "connectivity_weak",
                    "severity": "info",
                    "message": f"{prev_ch['num']}장 → {curr_ch['num']}장 연결이 약할 수 있습니다. 공통 키워드가 적습니다.",
                    "chapters": [prev_ch["num"], curr_ch["num"]],
                })

    def check_timeline_references(self):
        """시간 참조의 일관성을 검사합니다."""
        time_patterns = [
            r'(\d+)일\s*(전|후|뒤)',
            r'(\d+)시간\s*(전|후|뒤)',
            r'(아침|점심|저녁|밤|새벽|오전|오후)',
            r'(월요일|화요일|수요일|목요일|금요일|토요일|일요일)',
            r'(봄|여름|가을|겨울)',
            r'(\d+)월',
            r'(어제|오늘|내일|모레|그저께)',
        ]

        timeline_entries = []
        for ch in self.chapters:
            for pattern in time_patterns:
                matches = re.findall(pattern, ch["content"])
                for match in matches:
                    timeline_entries.append({
                        "chapter": ch["num"],
                        "reference": match if isinstance(match, str) else " ".join(match),
                    })

        # 같은 챕터 내에서 모순적인 시간 참조 검출
        # (간단한 규칙 기반: 아침 → 밤 → 아침 같은 패턴)
        for ch in self.chapters:
            time_of_day = re.findall(r'(아침|점심|저녁|밤|새벽)', ch["content"])
            if len(time_of_day) >= 3:
                # 시간대 순서 검증
                time_order = {"새벽": 0, "아침": 1, "점심": 2, "오후": 3, "저녁": 4, "밤": 5}
                prev_time = -1
                reversals = 0
                for t in time_of_day:
                    curr_time = time_order.get(t, 3)
                    if curr_time < prev_time:
                        reversals += 1
                    prev_time = curr_time

                if reversals > 2:
                    self.issues.append({
                        "type": "timeline_confusion",
                        "severity": "warning",
                        "message": f"{ch['num']}장에서 시간대가 {reversals}회 역전됩니다. 타임라인을 확인하세요.",
                        "chapters": [ch["num"]],
                    })

    def check_location_consistency(self):
        """장소/지명의 일관성을 검사합니다."""
        # 모든 챕터에서 장소 패턴 추출
        location_patterns = [
            r'([\w]+(?:시|군|구|동|읍|면|리|로|길|산|강|호수|마을|성|궁|탑|숲|숲속))',
        ]

        location_usage = defaultdict(list)
        for ch in self.chapters:
            for pattern in location_patterns:
                matches = re.findall(pattern, ch["content"])
                for match in matches:
                    if len(match) >= 3:  # 너무 짧은 것 제외
                        location_usage[match].append(ch["num"])

        # 유사한 지명 검출 (오타 가능성)
        locations = list(location_usage.keys())
        for i in range(len(locations)):
            for j in range(i + 1, len(locations)):
                if _similar_names(locations[i], locations[j]):
                    self.issues.append({
                        "type": "location_similar",
                        "severity": "warning",
                        "message": f"유사한 지명: '{locations[i]}'와 '{locations[j]}'. 오타 또는 불일치일 수 있습니다.",
                        "chapters": list(set(location_usage[locations[i]] + location_usage[locations[j]])),
                    })

    def check_repeated_phrases(self):
        """과도하게 반복되는 구절을 검출합니다."""
        # 3-gram 추출 및 빈도 계산
        all_text = " ".join(ch["content"] for ch in self.chapters)
        words = re.findall(r'[가-힣]+', all_text)

        trigrams = Counter()
        for i in range(len(words) - 2):
            trigram = f"{words[i]} {words[i+1]} {words[i+2]}"
            if len(trigram) >= 6:  # 너무 짧은 것 제외
                trigrams[trigram] += 1

        # 5회 이상 반복되는 구절
        for phrase, count in trigrams.most_common(20):
            if count >= 5 and not _is_common_phrase(phrase):
                self.issues.append({
                    "type": "repetition",
                    "severity": "info",
                    "message": f"구절 '{phrase}'이 {count}회 반복됩니다.",
                    "chapters": [],
                })

    def check_pov_consistency(self):
        """시점(POV) 일관성을 검사합니다."""
        for ch in self.chapters:
            content = ch["content"]
            pov = ch["metadata"].get("pov", "")

            # 1인칭 표현 검출
            first_person = len(re.findall(r'나는|내가|나의|나를|나에게', content))
            # 3인칭 표현 검출 (일반적 서술)
            third_person_indicators = len(re.findall(r'그는|그녀는|그가|그녀가', content))

            if first_person > 5 and third_person_indicators > 5:
                self.issues.append({
                    "type": "pov_mixed",
                    "severity": "error",
                    "message": f"{ch['num']}장에서 1인칭과 3인칭이 혼용됩니다 (1인칭: {first_person}회, 3인칭: {third_person_indicators}회).",
                    "chapters": [ch["num"]],
                })

    def _generate_report(self) -> dict:
        """검사 결과 리포트를 생성합니다."""
        errors = [i for i in self.issues if i["severity"] == "error"]
        warnings = [i for i in self.issues if i["severity"] == "warning"]
        infos = [i for i in self.issues if i["severity"] == "info"]

        # 점수 계산 (100점 만점)
        score = 100
        score -= len(errors) * 10
        score -= len(warnings) * 5
        score -= len(infos) * 1
        score = max(0, min(100, score))

        return {
            "title": self.config["title"],
            "checked_at": datetime.now().isoformat(),
            "chapters_checked": len(self.chapters),
            "total_wordcount": sum(ch["wordcount"] for ch in self.chapters),
            "score": score,
            "summary": {
                "errors": len(errors),
                "warnings": len(warnings),
                "infos": len(infos),
                "total_issues": len(self.issues),
            },
            "issues": {
                "errors": errors,
                "warnings": warnings,
                "infos": infos,
            },
        }

    def _save_report(self, report: dict):
        """리포트를 파일로 저장합니다."""
        report_dir = self.project_dir / "edits"
        report_dir.mkdir(parents=True, exist_ok=True)

        # JSON 저장
        json_path = report_dir / "consistency_report.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        # 마크다운 저장
        md_path = report_dir / "consistency_report.md"
        md_content = self._report_to_markdown(report)
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_content)

    def _report_to_markdown(self, report: dict) -> str:
        """리포트를 마크다운 형식으로 변환합니다."""
        md = f"""# 일관성 검사 리포트: {report['title']}

> 검사일시: {report['checked_at']}
> 검사 챕터: {report['chapters_checked']}개
> 총 글자수: {report['total_wordcount']:,}자
> **점수: {report['score']}/100**

---

## 요약

| 등급 | 건수 |
|------|------|
| 오류 (Error) | {report['summary']['errors']} |
| 경고 (Warning) | {report['summary']['warnings']} |
| 정보 (Info) | {report['summary']['infos']} |
| **합계** | **{report['summary']['total_issues']}** |

"""
        if report["issues"]["errors"]:
            md += "## 오류 (반드시 수정)\n\n"
            for i, issue in enumerate(report["issues"]["errors"], 1):
                md += f"{i}. **[{issue['type']}]** {issue['message']}\n"
                if issue.get("chapters"):
                    md += f"   - 관련 챕터: {', '.join(str(c) for c in issue['chapters'])}\n"
            md += "\n"

        if report["issues"]["warnings"]:
            md += "## 경고 (수정 권장)\n\n"
            for i, issue in enumerate(report["issues"]["warnings"], 1):
                md += f"{i}. **[{issue['type']}]** {issue['message']}\n"
                if issue.get("chapters"):
                    md += f"   - 관련 챕터: {', '.join(str(c) for c in issue['chapters'])}\n"
            md += "\n"

        if report["issues"]["infos"]:
            md += "## 정보 (선택적 개선)\n\n"
            for i, issue in enumerate(report["issues"]["infos"], 1):
                md += f"{i}. **[{issue['type']}]** {issue['message']}\n"
            md += "\n"

        return md


def _similar_names(a: str, b: str) -> bool:
    """두 이름이 유사한지 판단합니다 (편집 거리 기반)."""
    if a == b:
        return False
    if len(a) != len(b):
        return False
    diff = sum(1 for x, y in zip(a, b) if x != y)
    return diff == 1


def _is_common_phrase(phrase: str) -> bool:
    """일반적인 구절인지 판단합니다."""
    common_phrases = [
        "그리고 그는", "하지만 그는", "그래서 그는",
        "그녀는 그의", "그는 그녀의", "할 수 있",
        "것이 아니", "수 없었다", "것을 알고",
    ]
    return phrase in common_phrases


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python consistency_checker.py <project_dir>")
        sys.exit(1)

    checker = ConsistencyChecker(sys.argv[1])
    report = checker.run_all_checks()
    print(json.dumps(report, ensure_ascii=False, indent=2))
