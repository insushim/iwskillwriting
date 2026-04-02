#!/usr/bin/env python3
"""
Book Writer - Chapter Splitter
긴 챕터를 웹소설 연재용으로 자동 분할하는 도구.

기능:
- 플랫폼별 목표 글자수 기준 분할
- 씬 브레이크/문단 경계에서 분할 (문맥 보존)
- 분할 후 각 에피소드에 후크/클리프행어 보강 프롬프트 생성
- 이전 화 요약 자동 삽입 옵션
- 분할 결과 미리보기
"""

import json
import re
import sys
from pathlib import Path
from datetime import datetime


# 분할 포인트 우선순위
SPLIT_PRIORITY = [
    (r'\n---\n', "씬 브레이크 (---)"),
    (r'\n\*\s*\*\s*\*\n', "씬 브레이크 (***)"),
    (r'\n#{1,3}\s', "소제목"),
    (r'\n\n(?=["""])', "대화 시작 전"),
    (r'(?<=[.!?。])\n\n', "문단 경계"),
    (r'(?<=[.!?。])\s', "문장 경계 (최후 수단)"),
]


class ChapterSplitter:
    def __init__(self, project_dir: str, target_wordcount: int = 4000,
                 platform: str = "kakaopage"):
        self.project_dir = Path(project_dir)
        self.config = self._load_config()
        self.target_wc = target_wordcount
        self.platform = platform
        self.tolerance = 0.25  # ±25% 허용

    def _load_config(self) -> dict:
        with open(self.project_dir / "project.json", "r", encoding="utf-8") as f:
            return json.load(f)

    def split_all(self, dry_run: bool = True) -> dict:
        """모든 챕터를 분석하고 분할합니다."""
        chapters_dir = self.project_dir / "chapters"
        results = {"splits": [], "total_episodes": 0, "unchanged": 0}

        min_wc = int(self.target_wc * (1 - self.tolerance))
        max_wc = int(self.target_wc * (1 + self.tolerance))

        for ch_file in sorted(chapters_dir.glob("ch*.md")):
            content = ch_file.read_text(encoding="utf-8")

            # 프론트매터 분리
            body = content
            frontmatter = ""
            if content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    frontmatter = f"---{parts[1]}---\n\n"
                    body = parts[2].strip()

            wc = len(body)
            ch_num = int(re.search(r'\d+', ch_file.stem).group())

            if wc <= max_wc:
                results["unchanged"] += 1
                results["total_episodes"] += 1
                continue

            # 분할 필요
            parts_needed = max(2, wc // self.target_wc + (1 if wc % self.target_wc > min_wc * 0.5 else 0))
            split_points = self._find_split_points(body, parts_needed)

            if not split_points:
                # 균등 분할 (폴백)
                part_size = wc // parts_needed
                split_points = [part_size * i for i in range(1, parts_needed)]

            # 분할 실행
            parts = self._split_at_points(body, split_points)

            split_info = {
                "original_chapter": ch_num,
                "original_wordcount": wc,
                "parts": len(parts),
                "part_details": [],
            }

            for i, part in enumerate(parts):
                part_wc = len(part)
                split_info["part_details"].append({
                    "episode": f"{ch_num}-{i+1}",
                    "wordcount": part_wc,
                    "in_range": min_wc <= part_wc <= max_wc,
                    "first_line": part[:80].replace("\n", " "),
                    "last_line": part[-80:].replace("\n", " "),
                })

                if not dry_run:
                    ep_file = chapters_dir / f"ep{ch_num:02d}_{i+1:02d}.md"
                    ep_content = f"---\nchapter: {ch_num}\nepisode: {i+1}\nwordcount: {part_wc}\nstatus: \"split\"\n---\n\n"
                    ep_content += part
                    ep_file.write_text(ep_content, encoding="utf-8")

            results["splits"].append(split_info)
            results["total_episodes"] += len(parts)

        results["total_episodes"] += results["unchanged"]

        self._save_report(results, dry_run)
        return results

    def _find_split_points(self, text: str, parts_needed: int) -> list:
        """최적의 분할 포인트를 찾습니다."""
        target_size = len(text) // parts_needed
        split_points = []

        for part_idx in range(1, parts_needed):
            ideal_pos = target_size * part_idx
            best_pos = None
            best_distance = float('inf')
            best_priority = len(SPLIT_PRIORITY)

            # 이상적 위치 ±30% 범위에서 분할점 탐색
            search_start = int(ideal_pos * 0.7)
            search_end = int(ideal_pos * 1.3)
            search_text = text[search_start:search_end]

            for priority, (pattern, _name) in enumerate(SPLIT_PRIORITY):
                for match in re.finditer(pattern, search_text):
                    abs_pos = search_start + match.start()
                    distance = abs(abs_pos - ideal_pos)

                    # 우선순위가 더 높거나, 같은 우선순위에서 더 가까운 위치
                    if (priority < best_priority or
                        (priority == best_priority and distance < best_distance)):
                        best_pos = abs_pos
                        best_distance = distance
                        best_priority = priority

            if best_pos is not None:
                split_points.append(best_pos)
            else:
                # 폴백: 가장 가까운 문장 끝
                fallback_pattern = r'[.!?。]\s'
                fallback_text = text[max(0, ideal_pos - 500):ideal_pos + 500]
                matches = list(re.finditer(fallback_pattern, fallback_text))
                if matches:
                    # 이상적 위치에 가장 가까운 것
                    closest = min(matches, key=lambda m: abs(
                        (max(0, ideal_pos - 500) + m.end()) - ideal_pos))
                    split_points.append(max(0, ideal_pos - 500) + closest.end())

        return sorted(split_points)

    def _split_at_points(self, text: str, split_points: list) -> list:
        """분할 포인트에서 텍스트를 나눕니다."""
        parts = []
        prev = 0
        for pos in split_points:
            part = text[prev:pos].strip()
            if part:
                parts.append(part)
            prev = pos
        # 마지막 부분
        last_part = text[prev:].strip()
        if last_part:
            parts.append(last_part)
        return parts

    def preview_split(self, chapter_num: int) -> dict:
        """특정 챕터의 분할 미리보기를 생성합니다."""
        ch_file = self.project_dir / "chapters" / f"ch{chapter_num:02d}.md"
        if not ch_file.exists():
            return {"error": f"챕터 {chapter_num} 파일을 찾을 수 없습니다."}

        content = ch_file.read_text(encoding="utf-8")
        body = content
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                body = parts[2].strip()

        wc = len(body)
        min_wc = int(self.target_wc * (1 - self.tolerance))
        max_wc = int(self.target_wc * (1 + self.tolerance))

        if wc <= max_wc:
            return {
                "chapter": chapter_num,
                "wordcount": wc,
                "needs_split": False,
                "message": f"분할 불필요 ({wc}자, 범위: {min_wc}-{max_wc}자)",
            }

        parts_needed = max(2, wc // self.target_wc + 1)
        split_points = self._find_split_points(body, parts_needed)
        parts = self._split_at_points(body, split_points)

        preview = {
            "chapter": chapter_num,
            "wordcount": wc,
            "needs_split": True,
            "target_range": f"{min_wc}-{max_wc}자",
            "parts_count": len(parts),
            "parts": [],
        }

        for i, part in enumerate(parts):
            preview["parts"].append({
                "episode": i + 1,
                "wordcount": len(part),
                "in_range": min_wc <= len(part) <= max_wc,
                "opening": part[:100].replace("\n", " ") + "...",
                "closing": "..." + part[-100:].replace("\n", " "),
            })

        return preview

    def generate_hook_prompts(self, parts: list) -> list:
        """분할된 각 에피소드에 후크/클리프행어 보강 프롬프트를 생성합니다."""
        prompts = []
        for i, part in enumerate(parts):
            if i < len(parts) - 1:  # 마지막 에피소드 제외
                prompts.append({
                    "episode": i + 1,
                    "prompt": f"""이 에피소드의 마지막 부분을 클리프행어로 강화해주세요.
현재 마지막 문장: "{part[-100:]}"
다음 에피소드 시작: "{parts[i+1][:100]}"

클리프행어 유형 중 선택:
1. 위기 예고: 다음 장면의 위험을 암시
2. 비밀 공개: 충격적 정보를 마지막 줄에
3. 선택의 갈림길: 결정하지 않은 채 끝
4. 타이머: 시간 제한 설정
5. 감정 반전: 예상과 반대 감정
6. 새 캐릭터: 의문의 인물 등장""",
                })
        return prompts

    def _save_report(self, results: dict, dry_run: bool):
        edits_dir = self.project_dir / "edits"
        edits_dir.mkdir(parents=True, exist_ok=True)

        with open(edits_dir / "split_report.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        mode = "미리보기 (dry run)" if dry_run else "실행 완료"
        md = f"""# 챕터 분할 리포트 [{mode}]

> 플랫폼: {self.platform}
> 목표 글자수: {self.target_wc}자 (±{int(self.tolerance*100)}%)
> 총 에피소드: {results['total_episodes']}개
> 분할 없이 유지: {results['unchanged']}개
> 분할된 챕터: {len(results['splits'])}개

"""
        for split in results["splits"]:
            md += f"## 챕터 {split['original_chapter']} ({split['original_wordcount']:,}자 → {split['parts']}개)\n\n"
            for pd in split["part_details"]:
                in_range = "OK" if pd["in_range"] else "범위 초과"
                md += f"- ep{pd['episode']}: {pd['wordcount']:,}자 [{in_range}]\n"
            md += "\n"

        with open(edits_dir / "split_report.md", "w", encoding="utf-8") as f:
            f.write(md)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python chapter_splitter.py <project_dir> [--target 4000] [--platform kakaopage]")
        print("  python chapter_splitter.py <project_dir> --preview <chapter_num>")
        print("  python chapter_splitter.py <project_dir> --execute")
        sys.exit(1)

    project_dir = sys.argv[1]
    target = 4000
    platform = "kakaopage"
    dry_run = True
    preview_ch = None

    for i, arg in enumerate(sys.argv[2:], 2):
        if arg == "--target" and i + 1 < len(sys.argv):
            target = int(sys.argv[i + 1])
        elif arg == "--platform" and i + 1 < len(sys.argv):
            platform = sys.argv[i + 1]
        elif arg == "--execute":
            dry_run = False
        elif arg == "--preview" and i + 1 < len(sys.argv):
            preview_ch = int(sys.argv[i + 1])

    splitter = ChapterSplitter(project_dir, target, platform)

    if preview_ch:
        result = splitter.preview_split(preview_ch)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        result = splitter.split_all(dry_run=dry_run)
        mode = "미리보기" if dry_run else "실행"
        print(f"\n[{mode}] 총 에피소드: {result['total_episodes']}개")
        print(f"분할된 챕터: {len(result['splits'])}개")
        print(f"유지: {result['unchanged']}개")
