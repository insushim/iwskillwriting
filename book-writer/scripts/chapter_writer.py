#!/usr/bin/env python3
"""
Book Writer - Phase 4: Context-Isolated Chapter Writer
각 챕터를 독립적 컨텍스트에서 작성하는 엔진.

이 스크립트는 Claude Code가 각 챕터 작성 시 필요한 컨텍스트를 조합하고,
작성된 챕터를 저장하는 역할을 합니다.
실제 텍스트 생성은 Claude LLM이 수행합니다.
"""

import json
import sys
import re
from pathlib import Path
from datetime import datetime


def prepare_chapter_context(project_dir: str, chapter_num: int) -> dict:
    """챕터 작성에 필요한 모든 컨텍스트를 조합합니다.

    Context Injection 전략:
    1. 전체 아웃라인 요약
    2. 해당 챕터의 상세 계획
    3. 이전 챕터 요약 (최근 2-3개)
    4. 관련 Codex 엔트리
    5. 문체 가이드라인
    """
    project_path = Path(project_dir)
    config = _load_config(project_path)

    context = {
        "chapter_num": chapter_num,
        "total_chapters": config["chapters"],
        "title": config["title"],
        "genre": config["genre"],
        "tone": config.get("tone", ""),
        "target_wordcount": config.get("chapter_wordcount", 4000),
    }

    # 1. 전체 아웃라인 요약
    outline_file = project_path / "outline" / "structure.md"
    if outline_file.exists():
        context["outline_summary"] = outline_file.read_text(encoding="utf-8")

    # 2. 해당 챕터의 상세 계획
    chapters_plan_file = project_path / "outline" / "chapters.md"
    if chapters_plan_file.exists():
        context["chapter_plan"] = _extract_chapter_plan(
            chapters_plan_file.read_text(encoding="utf-8"), chapter_num
        )

    # 비트시트 참조
    beats_file = project_path / "outline" / "beats.md"
    if beats_file.exists():
        context["beats"] = beats_file.read_text(encoding="utf-8")

    # 3. 이전 챕터 요약 (최근 3개)
    prev_summaries = []
    for prev_num in range(max(1, chapter_num - 3), chapter_num):
        prev_file = project_path / "chapters" / f"ch{prev_num:02d}.md"
        if prev_file.exists():
            content = prev_file.read_text(encoding="utf-8")
            summary = _create_chapter_summary(content, prev_num)
            prev_summaries.append(summary)
    context["previous_chapters"] = prev_summaries

    # 4. 관련 Codex 엔트리
    codex_dir = project_path / "codex"
    if codex_dir.exists():
        codex_data = {}
        for codex_file in codex_dir.glob("*.md"):
            codex_data[codex_file.stem] = codex_file.read_text(encoding="utf-8")
        context["codex"] = codex_data

    # 5. 문체 가이드라인
    rules_file = project_path / "codex" / "rules.md"
    if rules_file.exists():
        context["style_rules"] = rules_file.read_text(encoding="utf-8")

    return context


def build_writing_prompt(context: dict) -> str:
    """챕터 작성을 위한 프롬프트를 구성합니다."""

    prompt_parts = []

    # 기본 지시
    prompt_parts.append(f"""## 챕터 작성 지시

당신은 **{context['title']}**의 {context['chapter_num']}장을 작성합니다.
- 장르: {context['genre']}
- 톤: {context.get('tone', '작품에 맞게')}
- 목표 분량: {context['target_wordcount']:,}자
- 전체 챕터: {context['chapter_num']}/{context['total_chapters']}
""")

    # 아웃라인
    if context.get("outline_summary"):
        prompt_parts.append(f"""## 전체 구조
{context['outline_summary'][:2000]}
""")

    # 챕터 계획
    if context.get("chapter_plan"):
        prompt_parts.append(f"""## 이번 챕터 계획
{context['chapter_plan']}
""")

    # 이전 챕터 요약
    if context.get("previous_chapters"):
        prompt_parts.append("## 이전 챕터 요약")
        for summary in context["previous_chapters"]:
            prompt_parts.append(summary)

    # Codex 정보 (핵심만)
    if context.get("codex"):
        prompt_parts.append("## Codex (스토리 바이블)")
        for key, content in context["codex"].items():
            # 너무 길면 앞부분만
            truncated = content[:1500] if len(content) > 1500 else content
            prompt_parts.append(f"### {key}\n{truncated}")

    # 문체 규칙
    if context.get("style_rules"):
        prompt_parts.append(f"""## 문체 규칙
{context['style_rules'][:1000]}
""")

    # 작성 지침
    prompt_parts.append("""## 작성 지침
1. **Show, don't tell**: 감정을 직접 서술하지 말고 행동/감각으로 묘사
2. **문장 다양성**: 단문, 중문, 장문을 혼합하여 리듬감 부여
3. **감각 묘사**: 시각, 청각, 촉각, 후각, 미각 중 2가지 이상 포함
4. **AI 패턴 회피**: 클리셰, 과도한 부사, 반복적 문장 구조 금지
5. **서브텍스트**: 대화에 말하지 않는 의미를 담기
6. **연결성**: 이전 챕터의 마지막 장면과 자연스럽게 이어지기
7. **클리프행어**: 챕터 끝에 다음이 궁금해지는 요소 배치
8. **일관성**: Codex의 캐릭터 설정, 세계관 규칙 엄수
""")

    return "\n\n".join(prompt_parts)


def save_chapter(project_dir: str, chapter_num: int, content: str, metadata: dict = None) -> str:
    """작성된 챕터를 저장합니다."""
    project_path = Path(project_dir)
    chapters_dir = project_path / "chapters"
    chapters_dir.mkdir(parents=True, exist_ok=True)

    # 프론트매터 생성
    frontmatter = {
        "chapter": chapter_num,
        "title": metadata.get("title", f"Chapter {chapter_num}") if metadata else f"Chapter {chapter_num}",
        "pov": metadata.get("pov", "") if metadata else "",
        "location": metadata.get("location", "") if metadata else "",
        "timeline": metadata.get("timeline", "") if metadata else "",
        "wordcount": len(content),
        "status": "draft",
        "created_at": datetime.now().isoformat(),
    }

    # 마크다운 파일 작성
    chapter_file = chapters_dir / f"ch{chapter_num:02d}.md"

    frontmatter_str = "---\n"
    for key, value in frontmatter.items():
        frontmatter_str += f"{key}: {json.dumps(value, ensure_ascii=False)}\n"
    frontmatter_str += "---\n\n"

    full_content = frontmatter_str + content

    with open(chapter_file, "w", encoding="utf-8") as f:
        f.write(full_content)

    # project.json 업데이트
    _update_project_progress(project_path, chapter_num)

    return str(chapter_file)


def get_chapter_status(project_dir: str) -> list:
    """모든 챕터의 작성 상태를 반환합니다."""
    project_path = Path(project_dir)
    config = _load_config(project_path)
    chapters_dir = project_path / "chapters"

    statuses = []
    for i in range(1, config["chapters"] + 1):
        ch_file = chapters_dir / f"ch{i:02d}.md"
        if ch_file.exists():
            content = ch_file.read_text(encoding="utf-8")
            # 프론트매터 파싱
            wordcount = len(content)
            status = "draft"
            if "status:" in content:
                for line in content.split("\n"):
                    if line.startswith("status:"):
                        status = line.split(":")[1].strip().strip('"')
                        break
            statuses.append({
                "chapter": i,
                "file": ch_file.name,
                "wordcount": wordcount,
                "status": status,
                "exists": True,
            })
        else:
            statuses.append({
                "chapter": i,
                "file": f"ch{i:02d}.md",
                "wordcount": 0,
                "status": "not_started",
                "exists": False,
            })

    return statuses


def _load_config(project_path: Path) -> dict:
    config_file = project_path / "project.json"
    with open(config_file, "r", encoding="utf-8") as f:
        return json.load(f)


def _extract_chapter_plan(full_plan: str, chapter_num: int) -> str:
    """전체 챕터 계획에서 특정 챕터의 계획을 추출합니다."""
    lines = full_plan.split("\n")
    result = []
    in_chapter = False

    patterns = [
        f"## {chapter_num}장",
        f"## 챕터 {chapter_num}",
        f"## Chapter {chapter_num}",
        f"## {chapter_num}.",
    ]

    for line in lines:
        if any(p in line for p in patterns):
            in_chapter = True
        elif in_chapter and line.startswith("## "):
            break

        if in_chapter:
            result.append(line)

    return "\n".join(result) if result else f"(챕터 {chapter_num}의 상세 계획이 아직 없습니다)"


def _create_chapter_summary(content: str, chapter_num: int) -> str:
    """챕터 내용의 요약을 생성합니다. (간단한 앞부분 추출)"""
    # 프론트매터 제거
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            content = parts[2]

    # 앞 500자 + 마지막 200자
    content = content.strip()
    if len(content) > 700:
        summary = content[:500] + "\n\n...(중략)...\n\n" + content[-200:]
    else:
        summary = content

    return f"### {chapter_num}장 요약\n{summary}"


def _update_project_progress(project_path: Path, chapter_num: int):
    """프로젝트 진행 상태를 업데이트합니다."""
    config_file = project_path / "project.json"
    with open(config_file, "r", encoding="utf-8") as f:
        config = json.load(f)

    config["updated_at"] = datetime.now().isoformat()
    config["current_phase"] = max(config.get("current_phase", 0), 4)
    config["status"] = "writing"

    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python chapter_writer.py <project_dir> context <chapter_num>")
        print("  python chapter_writer.py <project_dir> status")
        sys.exit(1)

    project_dir = sys.argv[1]
    command = sys.argv[2]

    if command == "context":
        chapter_num = int(sys.argv[3])
        context = prepare_chapter_context(project_dir, chapter_num)
        prompt = build_writing_prompt(context)
        print(prompt)
    elif command == "status":
        statuses = get_chapter_status(project_dir)
        print(json.dumps(statuses, ensure_ascii=False, indent=2))
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
