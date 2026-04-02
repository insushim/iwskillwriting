#!/usr/bin/env python3
"""
Book Writer - QA: Final Quality Reviewer
최종 품질 검증 및 종합 점수 산출.

모든 편집 단계의 결과를 종합하여 최종 품질 등급을 부여합니다.
"""

import json
import sys
from pathlib import Path
from datetime import datetime


class QAReviewer:
    def __init__(self, project_dir: str):
        self.project_dir = Path(project_dir)
        self.config = self._load_config()

    def _load_config(self) -> dict:
        with open(self.project_dir / "project.json", "r", encoding="utf-8") as f:
            return json.load(f)

    def run_review(self) -> dict:
        """전체 QA 리뷰를 실행합니다."""
        scores = {}

        # 1. 구조 완성도
        scores["structure"] = self._check_structure()

        # 2. 분량 달성도
        scores["wordcount"] = self._check_wordcount()

        # 3. 일관성 점수 (consistency_checker 결과)
        scores["consistency"] = self._load_consistency_score()

        # 4. 문체 점수 (style_analyzer 결과)
        scores["style"] = self._load_style_score()

        # 5. Codex 완성도
        scores["codex"] = self._check_codex()

        # 6. 출력 파일 생성 여부
        scores["output"] = self._check_output()

        # 종합 점수
        weights = {
            "structure": 0.20,
            "wordcount": 0.15,
            "consistency": 0.25,
            "style": 0.25,
            "codex": 0.10,
            "output": 0.05,
        }

        total_score = sum(
            scores[key]["score"] * weights[key]
            for key in weights
        )
        total_score = round(total_score, 1)

        # 등급
        if total_score >= 90:
            grade = "A"
        elif total_score >= 80:
            grade = "B"
        elif total_score >= 70:
            grade = "C"
        elif total_score >= 60:
            grade = "D"
        else:
            grade = "F"

        report = {
            "title": self.config["title"],
            "reviewed_at": datetime.now().isoformat(),
            "total_score": total_score,
            "grade": grade,
            "category_scores": scores,
            "weights": weights,
            "recommendations": self._generate_final_recommendations(scores, total_score),
            "is_publishable": total_score >= 70,
        }

        self._save_report(report)
        return report

    def _check_structure(self) -> dict:
        """구조 완성도를 검사합니다."""
        outline_dir = self.project_dir / "outline"
        chapters_dir = self.project_dir / "chapters"

        checks = {
            "structure_exists": (outline_dir / "structure.md").exists(),
            "beats_exists": (outline_dir / "beats.md").exists(),
            "chapters_plan_exists": (outline_dir / "chapters.md").exists(),
            "all_chapters_written": False,
        }

        expected_chapters = self.config.get("chapters", 0)
        actual_chapters = len(list(chapters_dir.glob("ch*.md"))) if chapters_dir.exists() else 0
        checks["all_chapters_written"] = actual_chapters >= expected_chapters

        passed = sum(1 for v in checks.values() if v)
        total = len(checks)
        score = round(passed / total * 100)

        return {
            "score": score,
            "checks": checks,
            "chapters_expected": expected_chapters,
            "chapters_written": actual_chapters,
        }

    def _check_wordcount(self) -> dict:
        """분량 달성도를 검사합니다."""
        chapters_dir = self.project_dir / "chapters"
        target = self.config.get("target_wordcount", 0)

        total_wc = 0
        chapter_wcs = []
        if chapters_dir.exists():
            for ch_file in sorted(chapters_dir.glob("ch*.md")):
                content = ch_file.read_text(encoding="utf-8")
                wc = len(content)
                total_wc += wc
                chapter_wcs.append({"file": ch_file.name, "wordcount": wc})

        ratio = total_wc / target * 100 if target > 0 else 0
        # 90-110% 범위면 100점, 그 외는 비례 감점
        if 90 <= ratio <= 110:
            score = 100
        elif ratio < 90:
            score = max(0, round(ratio / 90 * 100))
        else:
            score = max(0, round(100 - (ratio - 110) * 2))

        return {
            "score": min(100, score),
            "total_wordcount": total_wc,
            "target_wordcount": target,
            "achievement_pct": round(ratio, 1),
        }

    def _load_consistency_score(self) -> dict:
        """consistency_checker의 결과를 로드합니다."""
        report_path = self.project_dir / "edits" / "consistency_report.json"
        if report_path.exists():
            with open(report_path, "r", encoding="utf-8") as f:
                report = json.load(f)
            return {
                "score": report.get("score", 50),
                "source": "consistency_checker",
                "issues": report.get("summary", {}),
            }
        return {
            "score": 50,
            "source": "not_run",
            "message": "일관성 검사가 실행되지 않았습니다.",
        }

    def _load_style_score(self) -> dict:
        """style_analyzer의 결과를 로드합니다."""
        report_path = self.project_dir / "edits" / "style_report.json"
        if report_path.exists():
            with open(report_path, "r", encoding="utf-8") as f:
                report = json.load(f)
            return {
                "score": report.get("score", 50),
                "source": "style_analyzer",
                "recommendations_count": len(report.get("recommendations", [])),
            }
        return {
            "score": 50,
            "source": "not_run",
            "message": "문체 분석이 실행되지 않았습니다.",
        }

    def _check_codex(self) -> dict:
        """Codex 완성도를 검사합니다."""
        codex_dir = self.project_dir / "codex"
        if not codex_dir.exists():
            return {"score": 0, "message": "Codex 디렉토리가 없습니다."}

        codex_files = list(codex_dir.glob("*.md"))
        if not codex_files:
            return {"score": 0, "message": "Codex 파일이 없습니다."}

        complete = 0
        for f in codex_files:
            content = f.read_text(encoding="utf-8")
            # 템플릿 placeholder 또는 너무 짧으면 미완성
            if len(content) > 300 and "Phase 3에서 생성됩니다" not in content:
                complete += 1

        total = len(codex_files)
        score = round(complete / total * 100) if total > 0 else 0

        return {
            "score": score,
            "total_files": total,
            "complete_files": complete,
        }

    def _check_output(self) -> dict:
        """출력 파일 생성 여부를 검사합니다."""
        output_dir = self.project_dir / "output"
        if not output_dir.exists():
            return {"score": 0, "files": []}

        files = list(output_dir.glob("*"))
        output_files = []
        for f in files:
            if f.suffix in (".docx", ".epub", ".pdf"):
                output_files.append({"name": f.name, "size_kb": round(f.stat().st_size / 1024, 1)})

        score = min(100, len(output_files) * 50)  # 1개=50, 2개 이상=100
        return {
            "score": score,
            "files": output_files,
        }

    def _generate_final_recommendations(self, scores: dict, total_score: float) -> list:
        """최종 권고 사항을 생성합니다."""
        recs = []

        if scores["structure"]["score"] < 100:
            missing = scores["structure"]["chapters_expected"] - scores["structure"]["chapters_written"]
            if missing > 0:
                recs.append(f"챕터 {missing}개가 아직 작성되지 않았습니다.")

        if scores["wordcount"]["achievement_pct"] < 90:
            recs.append(f"분량이 목표의 {scores['wordcount']['achievement_pct']:.0f}%입니다. 내용을 보강하세요.")

        if scores["consistency"]["score"] < 70:
            recs.append("일관성 점수가 낮습니다. consistency_checker 리포트를 확인하고 수정하세요.")

        if scores["style"]["score"] < 70:
            recs.append("문체 점수가 낮습니다. style_analyzer 리포트를 확인하고 개선하세요.")

        if scores["codex"]["score"] < 50:
            recs.append("Codex(스토리 바이블)가 미완성입니다. 일관성 유지를 위해 완성하세요.")

        if scores["output"]["score"] < 50:
            recs.append("출력 파일이 생성되지 않았습니다. format_manuscript.py를 실행하세요.")

        if total_score >= 70:
            recs.append("출판 가능 수준입니다. 최종 교정 후 출판을 진행하세요.")
        else:
            recs.append("아직 출판하기에는 품질이 부족합니다. 위 권고 사항을 수정한 후 다시 검증하세요.")

        return recs

    def _save_report(self, report: dict):
        """QA 리포트를 저장합니다."""
        edits_dir = self.project_dir / "edits"
        edits_dir.mkdir(parents=True, exist_ok=True)

        # JSON
        with open(edits_dir / "qa_report.json", "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        # Markdown
        md = self._report_to_markdown(report)
        with open(edits_dir / "qa_report.md", "w", encoding="utf-8") as f:
            f.write(md)

    def _report_to_markdown(self, report: dict) -> str:
        grade_emoji = {"A": "🏆", "B": "✅", "C": "⚠️", "D": "🔶", "F": "❌"}
        emoji = grade_emoji.get(report["grade"], "")

        md = f"""# QA 최종 리포트: {report['title']}

> 검증일시: {report['reviewed_at']}
> **종합 점수: {report['total_score']}/100**
> **등급: {emoji} {report['grade']}**
> **출판 가능: {'예' if report['is_publishable'] else '아니오'}**

---

## 카테고리별 점수

| 카테고리 | 점수 | 가중치 | 기여도 |
|---------|------|--------|-------|
"""
        for cat, weight in report["weights"].items():
            score = report["category_scores"][cat]["score"]
            contrib = round(score * weight, 1)
            bar = "█" * int(score / 10) + "░" * (10 - int(score / 10))
            md += f"| {cat} | {score} {bar} | {weight*100:.0f}% | {contrib} |\n"

        md += f"\n**총점: {report['total_score']}**\n\n"

        md += "---\n\n## 권고 사항\n\n"
        for i, rec in enumerate(report["recommendations"], 1):
            md += f"{i}. {rec}\n"

        md += "\n---\n\n## 상세 정보\n\n"

        # 구조
        struct = report["category_scores"]["structure"]
        md += f"### 구조 ({struct['score']}점)\n"
        md += f"- 챕터: {struct.get('chapters_written', 0)}/{struct.get('chapters_expected', 0)}\n\n"

        # 분량
        wc = report["category_scores"]["wordcount"]
        md += f"### 분량 ({wc['score']}점)\n"
        md += f"- 현재: {wc.get('total_wordcount', 0):,}자 / 목표: {wc.get('target_wordcount', 0):,}자\n"
        md += f"- 달성률: {wc.get('achievement_pct', 0)}%\n\n"

        # 출력 파일
        out = report["category_scores"]["output"]
        md += f"### 출력 파일 ({out['score']}점)\n"
        for f in out.get("files", []):
            md += f"- {f['name']} ({f['size_kb']} KB)\n"

        return md


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python qa_reviewer.py <project_dir>")
        sys.exit(1)

    reviewer = QAReviewer(sys.argv[1])
    report = reviewer.run_review()

    print(f"\n{'='*50}")
    print(f"  QA 결과: {report['title']}")
    print(f"  종합 점수: {report['total_score']}/100 (등급: {report['grade']})")
    print(f"  출판 가능: {'예' if report['is_publishable'] else '아니오'}")
    print(f"{'='*50}\n")

    for rec in report["recommendations"]:
        print(f"  - {rec}")
    print()
