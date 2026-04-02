#!/usr/bin/env python3
"""
HWP Writer — HWP 파일 생성/수정 (pyhwpx COM 자동화)
한컴오피스 한글이 설치된 Windows에서만 동작합니다.
"""

import json
import sys
from pathlib import Path


def check_hwp_available() -> bool:
    """한컴오피스 한글 COM 사용 가능 여부 확인."""
    try:
        from pyhwpx import Hwp
        hwp = Hwp(visible=False)
        hwp.quit()
        return True
    except Exception:
        return False


def create_hwp(output_path: str, content: str, title: str = "",
               font: str = "맑은 고딕", font_size: int = 11,
               line_spacing: int = 160) -> dict:
    """새 HWP 파일을 생성합니다."""
    from pyhwpx import Hwp

    hwp = Hwp(visible=False)
    try:
        # 기본 설정
        hwp.set_font(font, font_size)
        hwp.set_line_spacing(line_spacing)

        # 마크다운 → HWP 변환
        lines = content.split("\n")
        for line in lines:
            stripped = line.strip()

            if stripped.startswith("# "):
                # 제목 (Heading 1)
                hwp.set_font(font, font_size + 8)
                hwp.set_bold(True)
                hwp.insert_text(stripped[2:])
                hwp.press_enter()
                hwp.set_font(font, font_size)
                hwp.set_bold(False)

            elif stripped.startswith("## "):
                # 소제목 (Heading 2)
                hwp.set_font(font, font_size + 4)
                hwp.set_bold(True)
                hwp.insert_text(stripped[3:])
                hwp.press_enter()
                hwp.set_font(font, font_size)
                hwp.set_bold(False)

            elif stripped.startswith("### "):
                # 소소제목 (Heading 3)
                hwp.set_font(font, font_size + 2)
                hwp.set_bold(True)
                hwp.insert_text(stripped[4:])
                hwp.press_enter()
                hwp.set_font(font, font_size)
                hwp.set_bold(False)

            elif stripped.startswith("- ") or stripped.startswith("* "):
                # 목록
                hwp.insert_text("  • " + stripped[2:])
                hwp.press_enter()

            elif stripped.startswith("> "):
                # 인용
                hwp.set_italic(True)
                hwp.insert_text("  " + stripped[2:])
                hwp.set_italic(False)
                hwp.press_enter()

            elif stripped == "---" or stripped == "***":
                # 구분선
                hwp.insert_text("─" * 40)
                hwp.press_enter()

            elif stripped == "":
                hwp.press_enter()

            else:
                hwp.insert_text(stripped)
                hwp.press_enter()

        # 저장
        out = Path(output_path).resolve()
        hwp.save_as(str(out))

        return {
            "status": "success",
            "path": str(out),
            "char_count": len(content),
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        hwp.quit()


def modify_hwp(file_path: str, operations: list) -> dict:
    """기존 HWP 파일을 수정합니다.

    operations: [
        {"type": "replace", "find": "홍길동", "replace": "김철수"},
        {"type": "insert", "position": "end", "text": "추가 텍스트"},
        {"type": "font", "name": "나눔명조", "size": 12},
        {"type": "header", "text": "보고서 제목"},
        {"type": "footer", "text": "페이지 {page}"},
    ]
    """
    from pyhwpx import Hwp

    hwp = Hwp(visible=False)
    try:
        hwp.open(str(Path(file_path).resolve()))

        results = []
        for op in operations:
            op_type = op.get("type", "")

            if op_type == "replace":
                find_text = op.get("find", "")
                replace_text = op.get("replace", "")
                if find_text:
                    count = 0
                    hwp.MovePos(2)  # 문서 시작
                    while hwp.find_replace(find_text, replace_text):
                        count += 1
                        if count > 1000:
                            break
                    results.append({"type": "replace", "find": find_text, "count": count})

            elif op_type == "insert":
                position = op.get("position", "end")
                text = op.get("text", "")
                if position == "end":
                    hwp.MovePos(3)  # 문서 끝
                elif position == "start":
                    hwp.MovePos(2)  # 문서 시작
                hwp.insert_text(text)
                results.append({"type": "insert", "position": position, "length": len(text)})

            elif op_type == "font":
                font_name = op.get("name", "맑은 고딕")
                font_size = op.get("size", 11)
                # 전체 선택 후 폰트 변경
                hwp.select_all()
                hwp.set_font(font_name, font_size)
                results.append({"type": "font", "name": font_name, "size": font_size})

        # 저장
        save_path = op.get("save_as", file_path) if operations else file_path
        hwp.save_as(str(Path(save_path).resolve()))

        return {
            "status": "success",
            "path": str(Path(save_path).resolve()),
            "operations": results,
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        hwp.quit()


def insert_table(file_path: str, rows: int, cols: int, data: list = None,
                 save_as: str = None) -> dict:
    """HWP 파일에 표를 삽입합니다."""
    from pyhwpx import Hwp

    hwp = Hwp(visible=False)
    try:
        hwp.open(str(Path(file_path).resolve()))
        hwp.MovePos(3)  # 문서 끝
        hwp.press_enter()

        # 표 생성
        hwp.create_table(rows, cols)

        # 데이터 입력
        if data:
            for row_idx, row_data in enumerate(data):
                for col_idx, cell_text in enumerate(row_data):
                    if row_idx < rows and col_idx < cols:
                        try:
                            hwp.put_cell_text(row_idx, col_idx, str(cell_text))
                        except Exception:
                            pass

        out = save_as or file_path
        hwp.save_as(str(Path(out).resolve()))

        return {
            "status": "success",
            "path": str(Path(out).resolve()),
            "table": {"rows": rows, "cols": cols},
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        hwp.quit()


def create_from_template(template_path: str, replacements: dict,
                         output_path: str) -> dict:
    """템플릿 HWP를 열어 텍스트를 치환하고 저장합니다."""
    operations = [
        {"type": "replace", "find": key, "replace": value}
        for key, value in replacements.items()
    ]
    # 원본 보호를 위해 먼저 복사
    import shutil
    temp_path = str(Path(output_path).with_suffix(".tmp.hwp"))
    shutil.copy2(template_path, temp_path)

    result = modify_hwp(temp_path, operations)

    if result["status"] == "success":
        # 최종 경로로 이동
        from pyhwpx import Hwp
        hwp = Hwp(visible=False)
        try:
            hwp.open(temp_path)
            hwp.save_as(str(Path(output_path).resolve()))
        finally:
            hwp.quit()
        Path(temp_path).unlink(missing_ok=True)
        result["path"] = str(Path(output_path).resolve())

    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python hwp_writer.py check        — 한글 설치 확인")
        print("  python hwp_writer.py create <output.hwp> <text>")
        print("  python hwp_writer.py replace <file.hwp> <find> <replace>")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "check":
        available = check_hwp_available()
        print(f"한컴오피스 한글: {'설치됨 (COM 사용 가능)' if available else '미설치'}")

    elif cmd == "create" and len(sys.argv) >= 4:
        result = create_hwp(sys.argv[2], sys.argv[3])
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif cmd == "replace" and len(sys.argv) >= 5:
        result = modify_hwp(sys.argv[2], [
            {"type": "replace", "find": sys.argv[3], "replace": sys.argv[4]}
        ])
        print(json.dumps(result, ensure_ascii=False, indent=2))
