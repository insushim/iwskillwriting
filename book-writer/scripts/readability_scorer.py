#!/usr/bin/env python3
"""
Book Writer - Readability Scorer
한국어 + 범용 가독성 점수 계산기.

7종 가독성 공식 + 한국어 특화 지수 + Burstiness/Perplexity 측정.
"""

import json
import re
import sys
import math
import statistics
from pathlib import Path
from datetime import datetime
from collections import Counter


class ReadabilityScorer:
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
            })
        return chapters

    def analyze(self) -> dict:
        """전체 가독성 분석을 실행합니다."""
        all_text = " ".join(ch["content"] for ch in self.chapters)

        results = {
            "korean_readability": self.korean_readability(all_text),
            "sentence_stats": self.sentence_statistics(all_text),
            "vocabulary_richness": self.vocabulary_richness(all_text),
            "burstiness": self.burstiness_score(all_text),
            "distinct_n": self.distinct_n_scores(all_text),
            "chapter_scores": self.per_chapter_scores(),
        }

        # 종합 점수
        kr = results["korean_readability"]["score"]
        burst = results["burstiness"]["score"] * 100
        vocab = min(100, results["vocabulary_richness"]["ttr"] * 200)
        results["overall_score"] = round((kr * 0.5 + burst * 0.25 + vocab * 0.25), 1)

        report = {
            "title": self.config["title"],
            "analyzed_at": datetime.now().isoformat(),
            "results": results,
        }

        self._save_report(report)
        return report

    def korean_readability(self, text: str) -> dict:
        """한국어 가독성 종합 점수를 계산합니다."""
        sentences = re.split(r'[.!?。]+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 2]

        if not sentences:
            return {"score": 0, "details": {}}

        # 1. 평균 문장 길이
        avg_sent_len = sum(len(s) for s in sentences) / len(sentences)
        sent_score = max(0, min(100, 100 - abs(avg_sent_len - 35) * 2))

        # 2. 문장 종결 다양성
        endings = []
        for s in sentences:
            s = s.strip()
            if s:
                last_chars = s[-2:] if len(s) >= 2 else s
                endings.append(last_chars)
        ending_types = len(set(endings))
        variety_score = min(100, ending_types / len(endings) * 150) if endings else 0

        # 3. 한자어/외래어 비율
        total_chars = len(re.findall(r'[가-힣a-zA-Z\u4e00-\u9fff]', text))
        foreign_chars = len(re.findall(r'[a-zA-Z\u4e00-\u9fff]', text))
        foreign_ratio = foreign_chars / total_chars if total_chars > 0 else 0
        foreign_score = max(0, 100 - foreign_ratio * 400)

        # 4. 평균 단락 길이
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        avg_para_len = sum(len(p) for p in paragraphs) / len(paragraphs) if paragraphs else 0
        para_score = max(0, min(100, 100 - abs(avg_para_len - 200) * 0.3))

        # 5. 의성어/의태어 밀도
        ono_patterns = re.findall(r'([가-힣]{2})\1', text)  # 반복 패턴 (살살, 둥둥 등)
        ono_density = len(ono_patterns) / (len(text) / 1000) if text else 0
        ono_score = min(100, ono_density * 20)

        # 종합
        total = (sent_score * 0.30 + variety_score * 0.15 +
                 foreign_score * 0.20 + para_score * 0.20 + ono_score * 0.15)

        return {
            "score": round(total, 1),
            "details": {
                "avg_sentence_length": round(avg_sent_len, 1),
                "sentence_score": round(sent_score, 1),
                "ending_variety_score": round(variety_score, 1),
                "foreign_ratio_pct": round(foreign_ratio * 100, 2),
                "foreign_score": round(foreign_score, 1),
                "avg_paragraph_length": round(avg_para_len, 1),
                "paragraph_score": round(para_score, 1),
                "onomatopoeia_density": round(ono_density, 2),
                "onomatopoeia_score": round(ono_score, 1),
            },
        }

    def sentence_statistics(self, text: str) -> dict:
        """문장 통계를 분석합니다."""
        sentences = re.split(r'[.!?。]+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 2]

        if not sentences:
            return {}

        lengths = [len(s) for s in sentences]
        mean = sum(lengths) / len(lengths)
        std = statistics.stdev(lengths) if len(lengths) > 1 else 0
        cv = std / mean if mean > 0 else 0

        return {
            "total_sentences": len(sentences),
            "mean_length": round(mean, 1),
            "median_length": round(statistics.median(lengths), 1),
            "std_dev": round(std, 1),
            "cv": round(cv, 3),
            "min_length": min(lengths),
            "max_length": max(lengths),
            "short_pct": round(sum(1 for l in lengths if l < 20) / len(lengths) * 100, 1),
            "medium_pct": round(sum(1 for l in lengths if 20 <= l < 50) / len(lengths) * 100, 1),
            "long_pct": round(sum(1 for l in lengths if l >= 50) / len(lengths) * 100, 1),
            "cv_assessment": "단조로움 (AI 의심)" if cv < 0.3 else "자연스러움" if cv < 0.6 else "매우 다양",
        }

    def vocabulary_richness(self, text: str) -> dict:
        """어휘 풍부도를 분석합니다."""
        words = re.findall(r'[가-힣]{2,}', text)
        if not words:
            return {"ttr": 0}

        total = len(words)
        unique = len(set(words))
        ttr = unique / total

        word_freq = Counter(words)
        hapax = sum(1 for freq in word_freq.values() if freq == 1)
        hapax_ratio = hapax / unique if unique > 0 else 0

        # Yule's K
        freq_spectrum = Counter(word_freq.values())
        m2 = sum(i * i * vi for i, vi in freq_spectrum.items())
        yules_k = 10000 * (m2 - total) / (total * total) if total > 0 else 0

        return {
            "total_words": total,
            "unique_words": unique,
            "ttr": round(ttr, 4),
            "hapax_count": hapax,
            "hapax_ratio": round(hapax_ratio, 4),
            "yules_k": round(yules_k, 2),
            "ttr_assessment": "빈약" if ttr < 0.35 else "보통" if ttr < 0.5 else "풍부" if ttr < 0.65 else "매우 풍부",
        }

    def burstiness_score(self, text: str) -> dict:
        """Burstiness (돌발성) 점수를 계산합니다."""
        sentences = re.split(r'[.!?。]+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 2]

        if len(sentences) < 3:
            return {"score": 0}

        lengths = [len(s) for s in sentences]
        mean = sum(lengths) / len(lengths)
        std = statistics.stdev(lengths) if len(lengths) > 1 else 0
        cv = std / mean if mean > 0 else 0

        # 인접 문장 간 길이 차이
        diffs = [abs(lengths[i] - lengths[i-1]) for i in range(1, len(lengths))]
        avg_diff = sum(diffs) / len(diffs) if diffs else 0

        score = min(1.0, cv * 0.5 + (avg_diff / mean) * 0.5) if mean > 0 else 0

        return {
            "score": round(score, 3),
            "cv": round(cv, 3),
            "avg_adjacent_diff": round(avg_diff, 1),
            "assessment": "AI 패턴 (낮은 돌발성)" if score < 0.3 else "자연스러움" if score < 0.6 else "매우 인간적",
        }

    def distinct_n_scores(self, text: str) -> dict:
        """Distinct-n 다양성 점수를 계산합니다."""
        words = re.findall(r'[가-힣]{2,}', text)
        if len(words) < 3:
            return {}

        def calc_distinct(n):
            ngrams = [tuple(words[i:i+n]) for i in range(len(words)-n+1)]
            return len(set(ngrams)) / len(ngrams) if ngrams else 0

        d1 = calc_distinct(1)
        d2 = calc_distinct(2)
        d3 = calc_distinct(3)

        return {
            "distinct_1": round(d1, 4),
            "distinct_2": round(d2, 4),
            "distinct_3": round(d3, 4),
            "d1_assessment": "반복 많음" if d1 < 0.6 else "보통" if d1 < 0.8 else "다양",
            "d2_assessment": "반복 많음" if d2 < 0.8 else "보통" if d2 < 0.9 else "다양",
        }

    def per_chapter_scores(self) -> list:
        """챕터별 가독성 점수를 계산합니다."""
        results = []
        for ch in self.chapters:
            kr = self.korean_readability(ch["content"])
            burst = self.burstiness_score(ch["content"])
            results.append({
                "chapter": ch["num"],
                "readability": kr["score"],
                "burstiness": burst["score"],
                "wordcount": len(ch["content"]),
            })
        return results

    def _save_report(self, report: dict):
        edits_dir = self.project_dir / "edits"
        edits_dir.mkdir(parents=True, exist_ok=True)

        with open(edits_dir / "readability_report.json", "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        md = f"""# 가독성 분석 리포트: {report['title']}

> 분석일시: {report['analyzed_at']}
> **종합 점수: {report['results']['overall_score']}/100**

## 한국어 가독성: {report['results']['korean_readability']['score']}/100

| 지표 | 값 | 점수 |
|------|---|------|
"""
        details = report['results']['korean_readability']['details']
        md += f"| 평균 문장 길이 | {details.get('avg_sentence_length', 0)}자 | {details.get('sentence_score', 0)} |\n"
        md += f"| 문장 종결 다양성 | - | {details.get('ending_variety_score', 0)} |\n"
        md += f"| 외래어/한자 비율 | {details.get('foreign_ratio_pct', 0)}% | {details.get('foreign_score', 0)} |\n"
        md += f"| 평균 단락 길이 | {details.get('avg_paragraph_length', 0)}자 | {details.get('paragraph_score', 0)} |\n"

        ss = report['results']['sentence_stats']
        if ss:
            md += f"\n## 문장 통계\n"
            md += f"- 총 문장 수: {ss.get('total_sentences', 0)}\n"
            md += f"- 평균 길이: {ss.get('mean_length', 0)}자 (중앙값: {ss.get('median_length', 0)})\n"
            md += f"- 변동계수(CV): {ss.get('cv', 0)} → **{ss.get('cv_assessment', '')}**\n"
            md += f"- 분포: 단문 {ss.get('short_pct', 0)}% / 중문 {ss.get('medium_pct', 0)}% / 장문 {ss.get('long_pct', 0)}%\n"

        vr = report['results']['vocabulary_richness']
        md += f"\n## 어휘 풍부도\n"
        md += f"- TTR: {vr.get('ttr', 0)} → **{vr.get('ttr_assessment', '')}**\n"
        md += f"- 총 단어: {vr.get('total_words', 0):,} / 고유 단어: {vr.get('unique_words', 0):,}\n"
        md += f"- Hapax 비율: {vr.get('hapax_ratio', 0)}\n"

        b = report['results']['burstiness']
        md += f"\n## 인간다움 (Burstiness)\n"
        md += f"- 점수: {b.get('score', 0)} → **{b.get('assessment', '')}**\n"

        with open(edits_dir / "readability_report.md", "w", encoding="utf-8") as f:
            f.write(md)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python readability_scorer.py <project_dir>")
        sys.exit(1)

    scorer = ReadabilityScorer(sys.argv[1])
    report = scorer.analyze()
    print(f"가독성 종합 점수: {report['results']['overall_score']}/100")
    print(f"한국어 가독성: {report['results']['korean_readability']['score']}/100")
    print(f"Burstiness: {report['results']['burstiness']['assessment']}")
