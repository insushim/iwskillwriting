#!/usr/bin/env python3
"""
Book Writer - Phase 4.5: Emotional Arc Analyzer
Vonnegut Story Shape 기반 감정 아크 분석 및 시각화.

기능:
- 챕터별 감정 극성(positive/negative) 추적
- Vonnegut 8가지 스토리 형태 매칭
- 긴장도 곡선 생성 (텍스트 기반 ASCII)
- 급격한 감정 전환 검출
- 페이싱 분석 (액션/대화/묘사 비율)
"""

import json
import re
import sys
from pathlib import Path
from datetime import datetime
from collections import Counter


# 감정 키워드 사전
POSITIVE_WORDS = [
    "웃", "미소", "행복", "기쁘", "사랑", "희망", "따뜻", "감사", "환호", "빛",
    "축하", "성공", "기대", "설레", "평화", "즐거", "감동", "포근", "밝", "좋",
    "승리", "축복", "안도", "편안", "자유", "용기", "자신감", "치유", "화해", "재회",
    "꿈", "보람", "뿌듯", "신나", "활기", "생기", "향기", "달콤", "아름다",
]

NEGATIVE_WORDS = [
    "눈물", "슬프", "분노", "두려", "절망", "어둠", "죽음", "고통", "상실", "배신",
    "공포", "비명", "괴로", "외로", "불안", "위험", "파괴", "실패", "증오", "피",
    "상처", "우울", "한숨", "질투", "복수", "저주", "독", "함정", "재앙", "폐허",
    "이별", "후회", "절규", "악몽", "그림자", "냉기", "비참", "참혹", "비극",
]

# 긴장 키워드
TENSION_WORDS = [
    "갑자기", "그 순간", "비명", "폭발", "충격", "위기", "추격", "도망", "숨", "빠르",
    "심장", "긴장", "위험", "함정", "적", "공격", "방어", "전투", "싸움", "충돌",
    "비밀", "발각", "배신", "거짓", "반전", "시한", "마감", "데드라인",
]

# Vonnegut 스토리 형태
STORY_SHAPES = {
    "rags_to_riches": {
        "name": "Rags to Riches (가난에서 부로)",
        "pattern": "상승",
        "description": "시작은 나쁘지만 계속 좋아지는 이야기",
        "examples": "신데렐라, 성공 스토리",
    },
    "riches_to_rags": {
        "name": "Riches to Rags (부에서 가난으로)",
        "pattern": "하강",
        "description": "좋은 상황에서 나빠지는 비극",
        "examples": "비극, 몰락 서사",
    },
    "man_in_hole": {
        "name": "Man in a Hole (구덩이에 빠진 사람)",
        "pattern": "하강 후 상승",
        "description": "좋음 → 나쁨 → 좋음 (가장 흔한 형태)",
        "examples": "대부분의 모험 이야기",
    },
    "icarus": {
        "name": "Icarus (이카루스)",
        "pattern": "상승 후 하강",
        "description": "나쁨 → 좋음 → 나쁨 (교만의 대가)",
        "examples": "그리스 비극, 범죄 서사",
    },
    "cinderella": {
        "name": "Cinderella (신데렐라)",
        "pattern": "상승-하강-상승",
        "description": "나쁨 → 좋음 → 나쁨 → 좋음",
        "examples": "로맨스, 동화",
    },
    "oedipus": {
        "name": "Oedipus (오이디푸스)",
        "pattern": "하강-상승-하강",
        "description": "좋음 → 나쁨 → 좋음 → 나쁨",
        "examples": "비극적 아이러니",
    },
    "steady_ascent": {
        "name": "Steady Ascent (꾸준한 상승)",
        "pattern": "점진적 상승",
        "description": "성장 소설, 성공 서사",
        "examples": "자기계발 서사, 영웅 서사",
    },
    "steady_descent": {
        "name": "Steady Descent (꾸준한 하강)",
        "pattern": "점진적 하강",
        "description": "몰락 서사, 호러",
        "examples": "공포물, 디스토피아",
    },
}


class EmotionalArcAnalyzer:
    def __init__(self, project_dir: str):
        self.project_dir = Path(project_dir)
        self.config = self._load_config()
        self.chapters = self._load_chapters()

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
            })
        return chapters

    def analyze(self) -> dict:
        """전체 감정 아크 분석을 실행합니다."""
        results = {}

        # 1. 챕터별 감정 분석
        results["chapter_emotions"] = self._analyze_chapter_emotions()

        # 2. 긴장도 곡선
        results["tension_curve"] = self._analyze_tension()

        # 3. 스토리 형태 매칭
        results["story_shape"] = self._match_story_shape(results["chapter_emotions"])

        # 4. 급격한 감정 전환 검출
        results["abrupt_changes"] = self._detect_abrupt_changes(results["chapter_emotions"])

        # 5. 페이싱 분석
        results["pacing"] = self._analyze_pacing()

        # 6. ASCII 시각화
        results["ascii_chart"] = self._generate_ascii_chart(results["chapter_emotions"])

        # 점수
        results["score"] = self._calculate_score(results)

        report = {
            "title": self.config["title"],
            "analyzed_at": datetime.now().isoformat(),
            "chapters_analyzed": len(self.chapters),
            "results": results,
        }

        self._save_report(report)
        return report

    def _analyze_chapter_emotions(self) -> list:
        """챕터별 감정 극성을 분석합니다."""
        emotions = []
        for ch in self.chapters:
            pos = sum(ch["content"].count(w) for w in POSITIVE_WORDS)
            neg = sum(ch["content"].count(w) for w in NEGATIVE_WORDS)
            total = pos + neg
            polarity = (pos - neg) / total if total > 0 else 0
            intensity = total / (ch["wordcount"] / 1000) if ch["wordcount"] > 0 else 0

            emotions.append({
                "chapter": ch["num"],
                "positive": pos,
                "negative": neg,
                "polarity": round(polarity, 3),
                "intensity": round(intensity, 1),
                "dominant": "positive" if pos > neg else "negative" if neg > pos else "neutral",
            })
        return emotions

    def _analyze_tension(self) -> list:
        """챕터별 긴장도를 분석합니다."""
        tensions = []
        for ch in self.chapters:
            tension_count = sum(ch["content"].count(w) for w in TENSION_WORDS)
            density = tension_count / (ch["wordcount"] / 1000) if ch["wordcount"] > 0 else 0

            # 대화문 비율 (대화가 많으면 빠른 페이스)
            dialogues = re.findall(r'["""][^"""]+["""]', ch["content"])
            dialogue_ratio = sum(len(d) for d in dialogues) / ch["wordcount"] if ch["wordcount"] > 0 else 0

            # 문장 길이 (짧으면 긴장감 높음)
            sentences = re.split(r'[.!?。]+', ch["content"])
            sentences = [s.strip() for s in sentences if s.strip()]
            avg_sentence_len = sum(len(s) for s in sentences) / len(sentences) if sentences else 0

            # 종합 긴장도 (0-10)
            tension_score = min(10, density * 1.5 + dialogue_ratio * 3 + max(0, (50 - avg_sentence_len) / 10))

            tensions.append({
                "chapter": ch["num"],
                "tension_score": round(tension_score, 1),
                "tension_words": tension_count,
                "dialogue_ratio": round(dialogue_ratio * 100, 1),
                "avg_sentence_len": round(avg_sentence_len, 1),
            })
        return tensions

    def _match_story_shape(self, emotions: list) -> dict:
        """Vonnegut 스토리 형태에 매칭합니다."""
        if len(emotions) < 3:
            return {"shape": "unknown", "confidence": 0}

        polarities = [e["polarity"] for e in emotions]
        n = len(polarities)

        # 전반부/후반부 평균
        first_half = sum(polarities[:n//2]) / (n//2) if n >= 2 else 0
        second_half = sum(polarities[n//2:]) / (n - n//2) if n >= 2 else 0

        # 최저점/최고점 위치
        min_idx = polarities.index(min(polarities))
        max_idx = polarities.index(max(polarities))
        min_pos = min_idx / n
        max_pos = max_idx / n

        # 시작과 끝
        start = polarities[0]
        end = polarities[-1]

        # 패턴 매칭
        best_match = "man_in_hole"
        confidence = 50

        if start < 0 and end > 0 and min_pos < 0.5:
            best_match = "rags_to_riches"
            confidence = 70
        elif start > 0 and end < 0:
            best_match = "riches_to_rags"
            confidence = 70
        elif start > -0.1 and min_pos < 0.7 and end > start:
            best_match = "man_in_hole"
            confidence = 75
        elif start < 0.1 and max_pos < 0.7 and end < start:
            best_match = "icarus"
            confidence = 70
        elif start < 0 and end > 0 and min_pos > 0.3 and min_pos < 0.8:
            best_match = "cinderella"
            confidence = 65
        elif first_half > 0 and second_half > first_half:
            best_match = "steady_ascent"
            confidence = 60
        elif first_half < 0 and second_half < first_half:
            best_match = "steady_descent"
            confidence = 60

        shape_info = STORY_SHAPES[best_match]
        return {
            "shape": best_match,
            "name": shape_info["name"],
            "pattern": shape_info["pattern"],
            "description": shape_info["description"],
            "confidence": confidence,
        }

    def _detect_abrupt_changes(self, emotions: list) -> list:
        """급격한 감정 전환을 검출합니다."""
        abrupt = []
        for i in range(1, len(emotions)):
            diff = emotions[i]["polarity"] - emotions[i-1]["polarity"]
            if abs(diff) > 0.5:
                abrupt.append({
                    "from_chapter": emotions[i-1]["chapter"],
                    "to_chapter": emotions[i]["chapter"],
                    "polarity_change": round(diff, 3),
                    "direction": "급상승" if diff > 0 else "급하강",
                    "severity": "critical" if abs(diff) > 0.8 else "warning",
                })
        return abrupt

    def _analyze_pacing(self) -> dict:
        """페이싱을 분석합니다."""
        chapter_pacing = []
        for ch in self.chapters:
            content = ch["content"]

            # 대화 비율
            dialogues = re.findall(r'["""][^"""]+["""]', content)
            dialogue_len = sum(len(d) for d in dialogues)

            # 액션 키워드 밀도
            action_words = ["달렸", "뛰어", "쳐다", "잡았", "던졌", "피했", "때렸", "찔렀",
                           "부딪", "넘어", "쫓", "막았", "밀었", "끌었", "공격", "방어"]
            action_count = sum(content.count(w) for w in action_words)

            total = ch["wordcount"]
            dialogue_pct = dialogue_len / total * 100 if total > 0 else 0
            action_density = action_count / (total / 1000) if total > 0 else 0

            # 페이스 분류
            if action_density > 5 or dialogue_pct > 50:
                pace = "fast"
            elif dialogue_pct < 20 and action_density < 2:
                pace = "slow"
            else:
                pace = "medium"

            chapter_pacing.append({
                "chapter": ch["num"],
                "pace": pace,
                "dialogue_pct": round(dialogue_pct, 1),
                "action_density": round(action_density, 1),
            })

        # 연속 느린 구간 검출
        slow_streaks = []
        streak = 0
        for cp in chapter_pacing:
            if cp["pace"] == "slow":
                streak += 1
                if streak >= 3:
                    slow_streaks.append(cp["chapter"])
            else:
                streak = 0

        return {
            "chapter_pacing": chapter_pacing,
            "slow_streaks": slow_streaks,
            "fast_count": sum(1 for cp in chapter_pacing if cp["pace"] == "fast"),
            "medium_count": sum(1 for cp in chapter_pacing if cp["pace"] == "medium"),
            "slow_count": sum(1 for cp in chapter_pacing if cp["pace"] == "slow"),
        }

    def _generate_ascii_chart(self, emotions: list) -> str:
        """감정 곡선을 ASCII 차트로 시각화합니다."""
        if not emotions:
            return "(데이터 없음)"

        height = 10
        width = min(len(emotions), 50)

        # -1 ~ +1 을 0 ~ height로 매핑
        polarities = [e["polarity"] for e in emotions]

        chart = []
        chart.append("감정 아크 시각화 (+ 긍정 / - 부정)")
        chart.append("=" * (width + 10))

        for row in range(height, -1, -1):
            threshold = (row - height/2) / (height/2)  # -1 to +1
            line = f"{threshold:+.1f} |"
            for i, pol in enumerate(polarities):
                if abs(pol - threshold) < 0.15:
                    line += "●"
                elif row == height // 2:
                    line += "─"
                else:
                    line += " "
            chart.append(line)

        chart.append(f"     +{''.join(str(e['chapter'] % 10) for e in emotions)}")
        chart.append(f"      {''.join('─' for _ in emotions)}")
        chart.append(f"      챕터 번호")

        return "\n".join(chart)

    def _calculate_score(self, results: dict) -> int:
        """감정 아크 품질 점수를 계산합니다."""
        score = 100

        # 급격한 전환 감점
        abrupt = results["abrupt_changes"]
        score -= len([a for a in abrupt if a["severity"] == "critical"]) * 15
        score -= len([a for a in abrupt if a["severity"] == "warning"]) * 5

        # 느린 연속 구간 감점
        score -= len(results["pacing"]["slow_streaks"]) * 10

        # 스토리 형태 매칭 신뢰도
        if results["story_shape"]["confidence"] < 50:
            score -= 10

        # 감정 변화가 너무 적으면 감점
        polarities = [e["polarity"] for e in results["chapter_emotions"]]
        if polarities:
            polarity_range = max(polarities) - min(polarities)
            if polarity_range < 0.3:
                score -= 15  # 감정 변화 부족

        return max(0, min(100, score))

    def _save_report(self, report: dict):
        edits_dir = self.project_dir / "edits"
        edits_dir.mkdir(parents=True, exist_ok=True)

        with open(edits_dir / "emotion_arc_report.json", "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        md = self._to_markdown(report)
        with open(edits_dir / "emotion_arc_report.md", "w", encoding="utf-8") as f:
            f.write(md)

    def _to_markdown(self, report: dict) -> str:
        r = report["results"]
        md = f"""# 감정 아크 분석 리포트: {report['title']}

> 분석일시: {report['analyzed_at']}
> 분석 챕터: {report['chapters_analyzed']}개
> **점수: {r['score']}/100**

---

## 스토리 형태 (Vonnegut Story Shape)

- **매칭 형태**: {r['story_shape']['name']}
- **패턴**: {r['story_shape']['pattern']}
- **설명**: {r['story_shape']['description']}
- **신뢰도**: {r['story_shape']['confidence']}%

---

## 감정 곡선

```
{r['ascii_chart']}
```

---

## 챕터별 감정 분석

| 챕터 | 긍정 | 부정 | 극성 | 강도 | 지배 |
|------|------|------|------|------|------|
"""
        for e in r["chapter_emotions"]:
            md += f"| {e['chapter']} | {e['positive']} | {e['negative']} | {e['polarity']:+.2f} | {e['intensity']:.1f} | {e['dominant']} |\n"

        if r["abrupt_changes"]:
            md += "\n## 급격한 감정 전환\n\n"
            for ac in r["abrupt_changes"]:
                icon = "🔴" if ac["severity"] == "critical" else "🟡"
                md += f"- {icon} {ac['from_chapter']}장 → {ac['to_chapter']}장: {ac['direction']} ({ac['polarity_change']:+.3f})\n"

        md += f"\n## 페이싱 분석\n\n"
        md += f"- 빠른 장: {r['pacing']['fast_count']}개\n"
        md += f"- 보통 장: {r['pacing']['medium_count']}개\n"
        md += f"- 느린 장: {r['pacing']['slow_count']}개\n"
        if r['pacing']['slow_streaks']:
            md += f"- **주의**: 연속 느린 구간 검출 (챕터 {', '.join(str(s) for s in r['pacing']['slow_streaks'])})\n"

        return md


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python emotional_arc_analyzer.py <project_dir>")
        sys.exit(1)

    analyzer = EmotionalArcAnalyzer(sys.argv[1])
    report = analyzer.analyze()
    print(f"감정 아크 점수: {report['results']['score']}/100")
    print(f"스토리 형태: {report['results']['story_shape']['name']}")
    print(report["results"]["ascii_chart"])
