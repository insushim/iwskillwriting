#!/usr/bin/env python3
"""
Book Writer - Phase 7: Web Novel Optimizer
웹소설 플랫폼별 최적화 및 연재 분할 도구.

기능:
- 플랫폼별 챕터 길이 검증/분할
- 후크/클리프행어 품질 분석
- 첫 3화 몰입도 점수
- 유료 전환 포인트 분석
- 연재 스케줄 생성
- 플랫폼별 포맷 변환
"""

import json
import re
import sys
from pathlib import Path
from datetime import datetime, timedelta


# 플랫폼별 규격
PLATFORM_SPECS = {
    "kakaopage": {
        "name": "카카오페이지",
        "min_wordcount": 3000,
        "max_wordcount": 5000,
        "optimal_wordcount": 4000,
        "free_episodes": 50,
        "paid_conversion": "기다리면 무료",
        "genres": ["판타지", "로맨스", "무협", "현대", "BL"],
        "format": "txt",
    },
    "munpia": {
        "name": "문피아",
        "min_wordcount": 4000,
        "max_wordcount": 8000,
        "optimal_wordcount": 5500,
        "free_episodes": "전체 가능",
        "paid_conversion": "프리미엄 전환",
        "genres": ["판타지", "무협", "현대판타지", "게임"],
        "format": "txt",
    },
    "naver_series": {
        "name": "네이버 시리즈",
        "min_wordcount": 3000,
        "max_wordcount": 5000,
        "optimal_wordcount": 4000,
        "free_episodes": 5,
        "paid_conversion": "쿠키 시스템",
        "genres": ["로맨스", "판타지", "스릴러", "무협"],
        "format": "txt",
    },
    "ridi": {
        "name": "리디",
        "min_wordcount": 4000,
        "max_wordcount": 7000,
        "optimal_wordcount": 5000,
        "free_episodes": 3,
        "paid_conversion": "회당 결제",
        "genres": ["로맨스", "BL", "판타지", "현대"],
        "format": "epub",
    },
    "novelpia": {
        "name": "노벨피아",
        "min_wordcount": 3000,
        "max_wordcount": 5000,
        "optimal_wordcount": 4000,
        "free_episodes": "전체 가능",
        "paid_conversion": "후원 기반",
        "genres": ["판타지", "현대", "SF", "호러"],
        "format": "txt",
    },
    "joara": {
        "name": "조아라",
        "min_wordcount": 3000,
        "max_wordcount": 6000,
        "optimal_wordcount": 4500,
        "free_episodes": "전체 가능",
        "paid_conversion": "출판사 연동",
        "genres": ["로맨스", "판타지", "BL", "현대"],
        "format": "txt",
    },
    "royal_road": {
        "name": "Royal Road",
        "min_wordcount": 2000,
        "max_wordcount": 5000,
        "optimal_wordcount": 3000,
        "free_episodes": "전체",
        "paid_conversion": "Patreon 연동",
        "genres": ["LitRPG", "Progression", "Fantasy", "Isekai"],
        "format": "markdown",
    },
    "wattpad": {
        "name": "Wattpad",
        "min_wordcount": 1500,
        "max_wordcount": 3000,
        "optimal_wordcount": 2000,
        "free_episodes": "전체",
        "paid_conversion": "Paid Stories",
        "genres": ["Romance", "Fantasy", "Fanfiction", "Teen"],
        "format": "txt",
    },
}


class WebNovelOptimizer:
    def __init__(self, project_dir: str, platform: str = "kakaopage"):
        self.project_dir = Path(project_dir)
        self.config = self._load_config()
        self.chapters = self._load_chapters()
        self.platform = platform
        self.specs = PLATFORM_SPECS.get(platform, PLATFORM_SPECS["kakaopage"])

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
                "wordcount": len(body),
                "file": ch_file.name,
            })
        return chapters

    def optimize(self) -> dict:
        """전체 웹소설 최적화를 실행합니다."""
        results = {}

        results["platform"] = self.specs
        results["length_analysis"] = self.analyze_chapter_lengths()
        results["hook_analysis"] = self.analyze_hooks()
        results["first3_score"] = self.score_first_three()
        results["paid_conversion"] = self.analyze_paid_conversion()
        results["schedule"] = self.generate_schedule()
        results["split_suggestions"] = self.suggest_splits()

        # 종합 점수
        scores = [
            results["length_analysis"]["compliance_pct"],
            results["hook_analysis"]["avg_score"] * 10,
            results["first3_score"]["total_score"],
        ]
        results["overall_score"] = round(sum(scores) / len(scores), 1)

        self._save_report(results)
        return results

    def analyze_chapter_lengths(self) -> dict:
        """챕터 길이의 플랫폼 적합성을 분석합니다."""
        min_wc = self.specs["min_wordcount"]
        max_wc = self.specs["max_wordcount"]
        optimal = self.specs["optimal_wordcount"]

        compliant = 0
        issues = []

        for ch in self.chapters:
            wc = ch["wordcount"]
            if min_wc <= wc <= max_wc:
                compliant += 1
            elif wc < min_wc:
                issues.append({
                    "chapter": ch["num"],
                    "wordcount": wc,
                    "issue": f"너무 짧음 (최소 {min_wc}자, 현재 {wc}자)",
                    "action": "다음 챕터와 병합 고려",
                })
            else:
                issues.append({
                    "chapter": ch["num"],
                    "wordcount": wc,
                    "issue": f"너무 김 (최대 {max_wc}자, 현재 {wc}자)",
                    "action": "분할 필요",
                })

        total = len(self.chapters)
        compliance_pct = round(compliant / total * 100, 1) if total > 0 else 0

        return {
            "platform": self.specs["name"],
            "optimal_range": f"{min_wc}~{max_wc}자",
            "compliant_chapters": compliant,
            "total_chapters": total,
            "compliance_pct": compliance_pct,
            "issues": issues,
        }

    def analyze_hooks(self) -> dict:
        """각 화의 후크/클리프행어를 분석합니다."""
        HOOK_PATTERNS = [
            r'^["""]',  # 대화로 시작
            r'[?!]+$',  # 질문/느낌표로 끝
            r'갑자기|그 순간|그때',  # 긴장 유발
            r'비명|폭발|충격',  # 액션 시작
        ]

        CLIFF_PATTERNS = [
            r'\.\.\.$|…$',  # 말줄임
            r'[?!]+\s*$',  # 질문/느낌표로 끝
            r'그리고|하지만|그때',  # 전환
            r'다음|이어서|계속',  # 연속 암시
        ]

        results = []
        for ch in self.chapters:
            lines = ch["content"].strip().split("\n")
            first_3_lines = "\n".join(lines[:3]) if lines else ""
            last_3_lines = "\n".join(lines[-3:]) if lines else ""

            hook_score = 0
            for pattern in HOOK_PATTERNS:
                if re.search(pattern, first_3_lines):
                    hook_score += 2.5

            cliff_score = 0
            for pattern in CLIFF_PATTERNS:
                if re.search(pattern, last_3_lines):
                    cliff_score += 2.5

            results.append({
                "chapter": ch["num"],
                "hook_score": min(10, hook_score),
                "cliff_score": min(10, cliff_score),
                "has_hook": hook_score >= 2.5,
                "has_cliff": cliff_score >= 2.5,
            })

        avg = sum(r["hook_score"] + r["cliff_score"] for r in results) / (len(results) * 2) if results else 0

        return {
            "chapter_details": results,
            "avg_score": round(avg, 1),
            "chapters_without_hook": [r["chapter"] for r in results if not r["has_hook"]],
            "chapters_without_cliff": [r["chapter"] for r in results if not r["has_cliff"]],
        }

    def score_first_three(self) -> dict:
        """첫 3화의 몰입도를 점수화합니다."""
        scores = {}

        for i, ch in enumerate(self.chapters[:3], 1):
            content = ch["content"]
            episode_score = 0
            details = []

            # 길이 적절성 (10점)
            if self.specs["min_wordcount"] <= ch["wordcount"] <= self.specs["max_wordcount"]:
                episode_score += 10
                details.append("길이 적절 (+10)")

            # 대화 비율 (10점)
            dialogues = re.findall(r'["""][^"""]+["""]', content)
            dialogue_ratio = sum(len(d) for d in dialogues) / ch["wordcount"] if ch["wordcount"] > 0 else 0
            if 0.2 <= dialogue_ratio <= 0.6:
                episode_score += 10
                details.append(f"대화 비율 적절: {dialogue_ratio*100:.0f}% (+10)")

            # 캐릭터 등장 (10점)
            # 고유명사 추정 (따옴표 앞 2-4글자)
            names = re.findall(r'(\w{2,4})(?:이|가|은|는|의)', content)
            if len(set(names)) >= 2:
                episode_score += 10
                details.append(f"캐릭터 {len(set(names))}명 등장 (+10)")

            # 갈등/긴장 존재 (10점)
            tension_words = ["하지만", "그러나", "위험", "적", "갈등", "문제", "싸움", "대결"]
            tension = sum(content.count(w) for w in tension_words)
            if tension >= 3:
                episode_score += 10
                details.append(f"갈등 요소 {tension}개 (+10)")

            scores[f"episode_{i}"] = {
                "score": episode_score,
                "max": 40,
                "details": details,
            }

        total = sum(s["score"] for s in scores.values())
        max_total = sum(s["max"] for s in scores.values())

        return {
            "episodes": scores,
            "total_score": round(total / max_total * 100, 1) if max_total > 0 else 0,
        }

    def analyze_paid_conversion(self) -> dict:
        """유료 전환 포인트를 분석합니다."""
        free_eps = self.specs.get("free_episodes", 50)
        if isinstance(free_eps, str):
            return {"analysis": "이 플랫폼은 전체 무료 또는 유연한 모델입니다."}

        if len(self.chapters) < free_eps:
            return {
                "warning": f"현재 {len(self.chapters)}화인데 무료 구간이 {free_eps}화입니다. 더 많은 화가 필요합니다.",
                "needed": free_eps - len(self.chapters),
            }

        # 전환 직전 5화의 긴장도 분석
        pre_conversion = self.chapters[max(0, free_eps-5):free_eps]
        tension_scores = []
        for ch in pre_conversion:
            tension_words = ["위기", "비밀", "반전", "충격", "갑자기", "죽", "배신"]
            score = sum(ch["content"].count(w) for w in tension_words)
            tension_scores.append(score)

        avg_tension = sum(tension_scores) / len(tension_scores) if tension_scores else 0

        return {
            "free_episodes": free_eps,
            "total_episodes": len(self.chapters),
            "pre_conversion_tension": round(avg_tension, 1),
            "recommendation": "매우 좋음" if avg_tension > 5 else "보통" if avg_tension > 2 else "긴장감 보강 필요",
        }

    def generate_schedule(self, episodes_per_week: int = 5, start_date: str = None) -> dict:
        """연재 스케줄을 생성합니다."""
        if start_date:
            start = datetime.strptime(start_date, "%Y-%m-%d")
        else:
            start = datetime.now() + timedelta(days=7)

        total_eps = len(self.chapters)
        weeks_needed = total_eps / episodes_per_week if episodes_per_week > 0 else 0

        schedule = []
        current_date = start
        ep_num = 1

        for ch in self.chapters:
            schedule.append({
                "episode": ep_num,
                "date": current_date.strftime("%Y-%m-%d"),
                "day": ["월", "화", "수", "목", "금", "토", "일"][current_date.weekday()],
            })
            ep_num += 1
            # 주 N회 배치 (월~금 우선)
            current_date += timedelta(days=1)
            if current_date.weekday() >= episodes_per_week:
                current_date += timedelta(days=7 - current_date.weekday())

        return {
            "start_date": start.strftime("%Y-%m-%d"),
            "end_date": schedule[-1]["date"] if schedule else "",
            "episodes_per_week": episodes_per_week,
            "total_weeks": round(weeks_needed, 1),
            "schedule_preview": schedule[:14],  # 2주치 미리보기
        }

    def suggest_splits(self) -> list:
        """긴 챕터의 분할 지점을 제안합니다."""
        max_wc = self.specs["max_wordcount"]
        suggestions = []

        for ch in self.chapters:
            if ch["wordcount"] > max_wc:
                # 분할 지점 찾기: 씬 브레이크(---) 또는 빈 줄 기준
                content = ch["content"]
                splits = []

                # --- 씬 브레이크 위치
                for m in re.finditer(r'\n---\n|\n\*\s*\*\s*\*\n', content):
                    pos = m.start()
                    if max_wc * 0.4 < pos < max_wc * 1.5:
                        splits.append(pos)

                # 대화 후 빈 줄 위치 (백업)
                if not splits:
                    for m in re.finditer(r'\n\n', content):
                        pos = m.start()
                        if max_wc * 0.4 < pos < max_wc * 0.8:
                            splits.append(pos)
                            break

                suggestions.append({
                    "chapter": ch["num"],
                    "wordcount": ch["wordcount"],
                    "suggested_parts": max(2, ch["wordcount"] // max_wc + 1),
                    "split_points": len(splits),
                })

        return suggestions

    def _save_report(self, results: dict):
        edits_dir = self.project_dir / "edits"
        edits_dir.mkdir(parents=True, exist_ok=True)

        with open(edits_dir / "webnovel_optimization.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2, default=str)

        md = f"""# 웹소설 최적화 리포트

> 플랫폼: {self.specs['name']}
> 적정 분량: {self.specs['min_wordcount']}~{self.specs['max_wordcount']}자/화
> **종합 점수: {results['overall_score']}/100**

## 챕터 길이 적합성
- 적합: {results['length_analysis']['compliant_chapters']}/{results['length_analysis']['total_chapters']}화
- 적합률: {results['length_analysis']['compliance_pct']}%

## 후크/클리프행어 분석
- 평균 점수: {results['hook_analysis']['avg_score']}/10
- 후크 없는 화: {', '.join(str(c) for c in results['hook_analysis']['chapters_without_hook']) or '없음'}
- 클리프행어 없는 화: {', '.join(str(c) for c in results['hook_analysis']['chapters_without_cliff']) or '없음'}

## 첫 3화 몰입도
- 점수: {results['first3_score']['total_score']}/100

## 연재 스케줄
- 시작: {results['schedule']['start_date']}
- 주 {results['schedule']['episodes_per_week']}회
- 예상 완료: {results['schedule']['end_date']}
"""
        with open(edits_dir / "webnovel_optimization.md", "w", encoding="utf-8") as f:
            f.write(md)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python webnovel_optimizer.py <project_dir> [platform]")
        print(f"Platforms: {', '.join(PLATFORM_SPECS.keys())}")
        sys.exit(1)

    project_dir = sys.argv[1]
    platform = sys.argv[2] if len(sys.argv) > 2 else "kakaopage"

    optimizer = WebNovelOptimizer(project_dir, platform)
    results = optimizer.optimize()
    print(f"\n웹소설 최적화 점수: {results['overall_score']}/100")
    print(f"플랫폼: {results['platform']['name']}")
    print(f"챕터 적합률: {results['length_analysis']['compliance_pct']}%")
