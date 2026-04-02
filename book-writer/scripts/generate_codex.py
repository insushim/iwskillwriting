#!/usr/bin/env python3
"""
Book Writer - Phase 3: Codex (Story Bible) Generator
Novelcrafter의 Codex 시스템을 참고한 스토리 바이블 자동 생성.

이 스크립트는 Claude Code가 직접 호출하여 Codex를 생성하는 가이드라인을 제공합니다.
실제 텍스트 생성은 Claude LLM이 수행합니다.
"""

import json
import sys
from pathlib import Path
from datetime import datetime


# Codex 엔트리 타입 정의
CODEX_TYPES = {
    "fiction": {
        "characters": {
            "file": "characters.md",
            "description": "캐릭터 프로필",
            "template": """## {name}

### 기본 정보
- **이름**: {name}
- **나이**:
- **성별**:
- **직업/역할**:
- **첫 등장**: 챕터

### 외모
- **신체**:
- **얼굴**:
- **특징**:
- **복장**:

### 성격
- **MBTI/유형**:
- **강점**:
- **약점/결점**:
- **습관/버릇**:
- **말투 특징**:

### 동기
- **외적 목표 (Want)**:
- **내적 욕구 (Need)**:
- **두려움**:
- **비밀**:

### 캐릭터 아크
- **시작 상태**:
- **변화의 계기**:
- **최종 상태**:

### 관계
| 인물 | 관계 | 설명 |
|------|------|------|

### Progression Tracker
| 챕터 | 상태/변화 | 핵심 사건 |
|------|----------|----------|

---
""",
        },
        "worldbuilding": {
            "file": "worldbuilding.md",
            "description": "세계관 설정",
            "template": """## 세계관: {world_name}

### 기본 설정
- **시대**:
- **기술 수준**:
- **사회 체제**:

### 지리
| 장소 | 설명 | 관련 챕터 |
|------|------|----------|

### 역사
| 시기 | 사건 | 영향 |
|------|------|------|

### 마법/기술 체계
- **이름**:
- **원리**:
- **비용/제한**:
- **사용자**:

### 문화
- **언어**:
- **종교/신앙**:
- **관습**:
- **금기**:

### 정치/권력 구조
- **지배 체제**:
- **주요 세력**:
- **갈등 구도**:

---
""",
        },
        "timeline": {
            "file": "timeline.md",
            "description": "타임라인",
            "template": """## 타임라인

### 작품 이전 주요 사건
| 시기 | 사건 | 영향 |
|------|------|------|

### 작품 내 타임라인
| 챕터 | 작품 내 시간 | 사건 | 관련 인물 |
|------|-------------|------|----------|

### 계절/날씨 트래커
| 챕터 | 계절 | 날씨/시간대 |
|------|------|------------|

---
""",
        },
        "themes": {
            "file": "themes.md",
            "description": "주제 & 모티프",
            "template": """## 주제 & 모티프

### 핵심 주제
1. **{theme_1}**
   - 설명:
   - 표현 방식:
   - 관련 캐릭터:
   - 관련 챕터:

### 반복 모티프
| 모티프 | 의미 | 등장 위치 |
|--------|------|----------|

### 상징
| 상징 | 의미 | 첫 등장 |
|------|------|---------|

### 주제적 질문
- 이 작품이 묻는 질문:
- 작품이 제시하는 답:

---
""",
        },
        "rules": {
            "file": "rules.md",
            "description": "작품 규칙 & 제약",
            "template": """## 작품 규칙 & 제약

### 설정 규칙
| 규칙 | 설명 | 예외 |
|------|------|------|

### 마법/기술 규칙
| 규칙 | 비용 | 한계 |
|------|------|------|

### 문체 규칙
- **시점**:
- **시제**:
- **어조**:
- **금지 표현**:

### 연속성 규칙
- **시간 경과 방식**:
- **장소 이동 규칙**:
- **정보 공개 순서**:

---
""",
        },
    },
    "nonfiction": {
        "research": {
            "file": "research.md",
            "description": "리서치 노트",
            "template": """## 리서치 노트

### 주제: {topic}

### 핵심 데이터
| 출처 | 데이터/인용 | 사용 챕터 |
|------|-----------|----------|

### 전문가 의견
| 전문가 | 주장 | 출처 |
|--------|------|------|

### 통계
| 수치 | 설명 | 출처 | 검증 |
|------|------|------|------|

---
""",
        },
        "sources": {
            "file": "sources.md",
            "description": "참고 자료",
            "template": """## 참고 자료

### 도서
| 제목 | 저자 | 연도 | 관련 챕터 |
|------|------|------|----------|

### 논문/연구
| 제목 | 저자 | 저널 | 연도 | DOI |
|------|------|------|------|-----|

### 웹 자료
| 제목 | URL | 접근일 | 관련 챕터 |
|------|-----|--------|----------|

### 인터뷰/1차 자료
| 대상 | 일시 | 주제 | 관련 챕터 |
|------|------|------|----------|

---
""",
        },
        "themes": {
            "file": "themes.md",
            "description": "핵심 주제",
            "template": """## 핵심 주제

### 주요 주장
1. **{thesis}**
   - 근거:
   - 반론:
   - 재반론:

### 보조 주장
| 주장 | 근거 | 관련 챕터 |
|------|------|----------|

### 독자에게 전달할 핵심 메시지
1.
2.
3.

---
""",
        },
    },
}


def generate_codex_skeleton(project_dir: str) -> dict:
    """프로젝트 타입에 맞는 Codex 스켈레톤을 생성합니다."""
    config_path = Path(project_dir) / "project.json"
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    book_type = config.get("type", "fiction")
    codex_dir = Path(project_dir) / "codex"
    codex_dir.mkdir(parents=True, exist_ok=True)

    codex_types = CODEX_TYPES.get(book_type, CODEX_TYPES["fiction"])
    generated_files = []

    for key, entry_type in codex_types.items():
        file_path = codex_dir / entry_type["file"]
        header = f"# {config['title']} — {entry_type['description']}\n\n"
        header += f"> 생성일: {datetime.now().strftime('%Y-%m-%d')}\n"
        header += f"> 타입: {book_type}\n\n---\n\n"

        content = header + entry_type["template"]

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        generated_files.append(str(file_path))

    return {
        "project": config["title"],
        "type": book_type,
        "codex_dir": str(codex_dir),
        "generated_files": generated_files,
    }


def get_codex_for_chapter(project_dir: str, chapter_num: int) -> dict:
    """특정 챕터 작성에 필요한 Codex 정보를 추출합니다.

    이 함수는 chapter_writer.py에서 사용됩니다.
    각 챕터에 관련된 캐릭터, 장소, 타임라인 정보만 추출하여
    context window를 효율적으로 사용합니다.
    """
    config_path = Path(project_dir) / "project.json"
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    codex_dir = Path(project_dir) / "codex"
    codex_data = {}

    # 모든 Codex 파일 읽기
    for codex_file in codex_dir.glob("*.md"):
        content = codex_file.read_text(encoding="utf-8")
        codex_data[codex_file.stem] = content

    # 챕터 계획에서 관련 엔트리 참조
    chapters_file = Path(project_dir) / "outline" / "chapters.md"
    chapter_plan = ""
    if chapters_file.exists():
        full_plan = chapters_file.read_text(encoding="utf-8")
        # 해당 챕터 섹션 추출
        lines = full_plan.split("\n")
        in_chapter = False
        for line in lines:
            if f"## {chapter_num}장" in line or f"## Chapter {chapter_num}" in line or f"## 챕터 {chapter_num}" in line:
                in_chapter = True
            elif in_chapter and line.startswith("## "):
                break
            if in_chapter:
                chapter_plan += line + "\n"

    return {
        "chapter_num": chapter_num,
        "chapter_plan": chapter_plan,
        "codex": codex_data,
        "config": config,
    }


def validate_codex(project_dir: str) -> dict:
    """Codex의 완성도를 검증합니다."""
    codex_dir = Path(project_dir) / "codex"
    results = {"complete": [], "incomplete": [], "missing": []}

    config_path = Path(project_dir) / "project.json"
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    book_type = config.get("type", "fiction")
    expected_files = CODEX_TYPES.get(book_type, CODEX_TYPES["fiction"])

    for key, entry_type in expected_files.items():
        file_path = codex_dir / entry_type["file"]
        if not file_path.exists():
            results["missing"].append(entry_type["file"])
            continue

        content = file_path.read_text(encoding="utf-8")
        # 템플릿 placeholder가 남아있으면 미완성
        if "{" in content and "}" in content:
            results["incomplete"].append(entry_type["file"])
        elif len(content) < 200:
            results["incomplete"].append(entry_type["file"])
        else:
            results["complete"].append(entry_type["file"])

    total = len(expected_files)
    complete = len(results["complete"])
    results["completeness_pct"] = round(complete / total * 100, 1) if total > 0 else 0

    return results


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_codex.py <project_dir> [--validate]")
        sys.exit(1)

    project_dir = sys.argv[1]

    if "--validate" in sys.argv:
        result = validate_codex(project_dir)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        result = generate_codex_skeleton(project_dir)
        print(json.dumps(result, ensure_ascii=False, indent=2))
