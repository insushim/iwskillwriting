#!/usr/bin/env python3
"""
Book Writer - Phase 0: Project Initialization
프로젝트 디렉토리 구조를 생성하고 project.json 설정 파일을 만듭니다.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path


# 장르별 기본 설정
GENRE_DEFAULTS = {
    "fantasy": {
        "structure": "heros_journey",
        "target_wordcount": 100000,
        "chapters": 20,
        "chapter_wordcount": 5000,
    },
    "romance": {
        "structure": "save_the_cat",
        "target_wordcount": 80000,
        "chapters": 25,
        "chapter_wordcount": 3200,
    },
    "thriller": {
        "structure": "save_the_cat",
        "target_wordcount": 90000,
        "chapters": 30,
        "chapter_wordcount": 3000,
    },
    "mystery": {
        "structure": "story_grid",
        "target_wordcount": 80000,
        "chapters": 25,
        "chapter_wordcount": 3200,
    },
    "sf": {
        "structure": "snowflake",
        "target_wordcount": 100000,
        "chapters": 20,
        "chapter_wordcount": 5000,
    },
    "horror": {
        "structure": "seven_point",
        "target_wordcount": 70000,
        "chapters": 20,
        "chapter_wordcount": 3500,
    },
    "literary": {
        "structure": "kishotenketsu",
        "target_wordcount": 80000,
        "chapters": 15,
        "chapter_wordcount": 5333,
    },
    "ya": {
        "structure": "save_the_cat",
        "target_wordcount": 60000,
        "chapters": 20,
        "chapter_wordcount": 3000,
    },
    "children": {
        "structure": "kishotenketsu",
        "target_wordcount": 15000,
        "chapters": 10,
        "chapter_wordcount": 1500,
    },
    "self_help": {
        "structure": "problem_cause_solution",
        "target_wordcount": 50000,
        "chapters": 12,
        "chapter_wordcount": 4167,
    },
    "business": {
        "structure": "case_study",
        "target_wordcount": 60000,
        "chapters": 15,
        "chapter_wordcount": 4000,
    },
    "essay": {
        "structure": "thematic",
        "target_wordcount": 40000,
        "chapters": 15,
        "chapter_wordcount": 2667,
    },
    "how_to": {
        "structure": "how_to",
        "target_wordcount": 50000,
        "chapters": 15,
        "chapter_wordcount": 3333,
    },
    "narrative_nonfiction": {
        "structure": "narrative_nonfiction",
        "target_wordcount": 80000,
        "chapters": 20,
        "chapter_wordcount": 4000,
    },
}

# 소설 vs 비소설 분류
FICTION_GENRES = {"fantasy", "romance", "thriller", "mystery", "sf", "horror", "literary", "ya", "children"}
NONFICTION_GENRES = {"self_help", "business", "essay", "how_to", "narrative_nonfiction"}


def create_project(config: dict) -> str:
    """프로젝트 디렉토리를 생성하고 초기 파일을 만듭니다."""

    project_name = config.get("project_name", config.get("title", "untitled"))
    project_dir = Path(config.get("output_dir", ".")) / sanitize_dirname(project_name)

    # 디렉토리 생성
    dirs = [
        project_dir,
        project_dir / "outline",
        project_dir / "codex",
        project_dir / "chapters",
        project_dir / "edits",
        project_dir / "output",
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)

    # 장르 기본값 적용
    genre = config.get("genre", "literary").lower().replace(" ", "_")
    defaults = GENRE_DEFAULTS.get(genre, GENRE_DEFAULTS["literary"])

    # project.json 생성
    project_config = {
        "title": config.get("title", project_name),
        "subtitle": config.get("subtitle", ""),
        "author": config.get("author", ""),
        "genre": genre,
        "sub_genre": config.get("sub_genre", ""),
        "type": "fiction" if genre in FICTION_GENRES else "nonfiction",
        "language": config.get("language", "ko"),
        "target_audience": config.get("target_audience", ""),
        "tone": config.get("tone", ""),
        "core_idea": config.get("core_idea", ""),
        "structure": config.get("structure", defaults["structure"]),
        "target_wordcount": config.get("target_wordcount", defaults["target_wordcount"]),
        "chapters": config.get("chapters", defaults["chapters"]),
        "chapter_wordcount": config.get("chapter_wordcount", defaults["chapter_wordcount"]),
        "characters": config.get("characters", []),
        "themes": config.get("themes", []),
        "references": config.get("references", []),
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "status": "initialized",
        "current_phase": 0,
        "project_dir": str(project_dir),
    }

    config_path = project_dir / "project.json"
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(project_config, f, ensure_ascii=False, indent=2)

    # 초기 파일 생성
    _create_initial_files(project_dir, project_config)

    return str(project_dir)


def _create_initial_files(project_dir: Path, config: dict):
    """초기 마크다운 파일들을 생성합니다."""

    # outline/structure.md
    structure_content = f"""# {config['title']} — 구조 설계

## 기본 정보
- **제목**: {config['title']}
- **장르**: {config['genre']}
- **구조**: {config['structure']}
- **목표 분량**: {config['target_wordcount']:,}자
- **챕터 수**: {config['chapters']}개
- **챕터당 분량**: {config['chapter_wordcount']:,}자

## 핵심 아이디어
{config.get('core_idea', '(아직 미정)')}

## 구조 프레임워크
> 선택된 구조: **{config['structure']}**

(Phase 1에서 상세 구조가 생성됩니다)
"""
    _write_file(project_dir / "outline" / "structure.md", structure_content)

    # outline/beats.md
    _write_file(project_dir / "outline" / "beats.md",
                f"# {config['title']} — 비트시트\n\n(Phase 2에서 생성됩니다)\n")

    # outline/chapters.md
    _write_file(project_dir / "outline" / "chapters.md",
                f"# {config['title']} — 챕터 목록\n\n(Phase 2에서 생성됩니다)\n")

    # codex files
    if config["type"] == "fiction":
        _write_file(project_dir / "codex" / "characters.md",
                    f"# {config['title']} — 캐릭터 프로필\n\n(Phase 3에서 생성됩니다)\n")
        _write_file(project_dir / "codex" / "worldbuilding.md",
                    f"# {config['title']} — 세계관 설정\n\n(Phase 3에서 생성됩니다)\n")
        _write_file(project_dir / "codex" / "timeline.md",
                    f"# {config['title']} — 타임라인\n\n(Phase 3에서 생성됩니다)\n")
        _write_file(project_dir / "codex" / "themes.md",
                    f"# {config['title']} — 주제 & 모티프\n\n(Phase 3에서 생성됩니다)\n")
        _write_file(project_dir / "codex" / "rules.md",
                    f"# {config['title']} — 작품 규칙\n\n(Phase 3에서 생성됩니다)\n")
    else:
        _write_file(project_dir / "codex" / "research.md",
                    f"# {config['title']} — 리서치 노트\n\n(Phase 3에서 생성됩니다)\n")
        _write_file(project_dir / "codex" / "sources.md",
                    f"# {config['title']} — 참고 자료\n\n(Phase 3에서 생성됩니다)\n")
        _write_file(project_dir / "codex" / "themes.md",
                    f"# {config['title']} — 핵심 주제\n\n(Phase 3에서 생성됩니다)\n")


def sanitize_dirname(name: str) -> str:
    """디렉토리 이름에 사용할 수 없는 문자를 제거합니다."""
    invalid_chars = '<>:"/\\|?*'
    result = name
    for ch in invalid_chars:
        result = result.replace(ch, "")
    return result.strip().replace(" ", "_")


def _write_file(path: Path, content: str):
    """파일을 UTF-8로 작성합니다."""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def load_project(project_dir: str) -> dict:
    """기존 프로젝트의 설정을 로드합니다."""
    config_path = Path(project_dir) / "project.json"
    if not config_path.exists():
        raise FileNotFoundError(f"프로젝트 설정 파일을 찾을 수 없습니다: {config_path}")
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def update_project(project_dir: str, updates: dict):
    """프로젝트 설정을 업데이트합니다."""
    config = load_project(project_dir)
    config.update(updates)
    config["updated_at"] = datetime.now().isoformat()
    config_path = Path(project_dir) / "project.json"
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


def get_project_status(project_dir: str) -> dict:
    """프로젝트의 현재 상태를 반환합니다."""
    config = load_project(project_dir)
    chapters_dir = Path(project_dir) / "chapters"
    existing_chapters = list(chapters_dir.glob("ch*.md"))

    total_wordcount = 0
    chapter_statuses = []
    for ch_file in sorted(existing_chapters):
        content = ch_file.read_text(encoding="utf-8")
        wc = len(content)
        chapter_statuses.append({
            "file": ch_file.name,
            "wordcount": wc,
        })
        total_wordcount += wc

    return {
        "title": config["title"],
        "status": config["status"],
        "current_phase": config["current_phase"],
        "chapters_written": len(existing_chapters),
        "chapters_total": config["chapters"],
        "total_wordcount": total_wordcount,
        "target_wordcount": config["target_wordcount"],
        "progress_pct": round(total_wordcount / config["target_wordcount"] * 100, 1) if config["target_wordcount"] > 0 else 0,
        "chapter_details": chapter_statuses,
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python init_project.py <config.json>")
        print("  config.json: 프로젝트 설정 파일 경로")
        sys.exit(1)

    config_path = sys.argv[1]
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    project_dir = create_project(config)
    print(f"프로젝트가 생성되었습니다: {project_dir}")
    print(json.dumps(get_project_status(project_dir), ensure_ascii=False, indent=2))
