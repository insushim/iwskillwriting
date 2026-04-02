#!/usr/bin/env python3
"""
HWP Converter — HWP ↔ DOCX/PDF/TXT/MD 변환
한컴오피스 한글 COM 자동화 기반 (PDF/DOCX 변환)
+ 텍스트 기반 변환 (한글 미설치 시)
"""

import json
import sys
from pathlib import Path


def convert_hwp(input_path: str, output_format: str, output_path: str = None) -> dict:
    """HWP 파일을 다른 포맷으로 변환합니다."""
    inp = Path(input_path)
    if not inp.exists():
        return {"error": f"파일을 찾을 수 없습니다: {input_path}"}

    fmt = output_format.lower().strip(".")

    if not output_path:
        output_path = str(inp.with_suffix(f".{fmt}"))

    if fmt == "txt":
        return _convert_to_txt(inp, output_path)
    elif fmt == "md":
        return _convert_to_md(inp, output_path)
    elif fmt in ("pdf", "docx", "doc"):
        return _convert_with_com(inp, fmt, output_path)
    elif fmt == "hwp":
        return _convert_to_hwp(inp, output_path)
    else:
        return {"error": f"지원하지 않는 포맷: {fmt}. 지원: txt, md, pdf, docx, hwp"}


def _convert_to_txt(inp: Path, output_path: str) -> dict:
    """HWP → TXT 변환 (COM 또는 OLE)."""
    from hwp_reader import read_hwp

    result = read_hwp(str(inp))
    if "error" in result:
        return result

    text = result.get("text", "")
    out = Path(output_path)
    out.write_text(text, encoding="utf-8")

    return {
        "status": "success",
        "input": inp.name,
        "output": str(out),
        "format": "txt",
        "char_count": len(text),
    }


def _convert_to_md(inp: Path, output_path: str) -> dict:
    """HWP → 마크다운 변환."""
    from hwp_reader import read_hwp

    result = read_hwp(str(inp))
    if "error" in result:
        return result

    text = result.get("text", "")

    # 간단한 마크다운 변환 (제목 감지 등)
    lines = text.split("\n")
    md_lines = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            md_lines.append("")
            continue

        # 짧고 끝에 마침표 없으면 제목 가능성
        if len(stripped) < 50 and not stripped.endswith((".","?","!",",",";")):
            if len(stripped) < 20:
                md_lines.append(f"## {stripped}")
            else:
                md_lines.append(f"### {stripped}")
        else:
            md_lines.append(stripped)

    md_text = "\n\n".join(md_lines)
    out = Path(output_path)
    out.write_text(md_text, encoding="utf-8")

    return {
        "status": "success",
        "input": inp.name,
        "output": str(out),
        "format": "md",
        "char_count": len(md_text),
    }


def _convert_with_com(inp: Path, fmt: str, output_path: str) -> dict:
    """한컴오피스 COM 자동화로 PDF/DOCX 변환."""
    try:
        from pyhwpx import Hwp
    except ImportError:
        return {"error": f"{fmt.upper()} 변환은 한컴오피스 한글 + pyhwpx 필요"}

    hwp = Hwp(visible=False)
    try:
        hwp.open(str(inp.resolve()))
        out = Path(output_path).resolve()

        if fmt == "pdf":
            hwp.save_as(str(out), "PDF")
        elif fmt in ("docx", "doc"):
            hwp.save_as(str(out), "DOCX")
        else:
            hwp.save_as(str(out))

        return {
            "status": "success",
            "input": inp.name,
            "output": str(out),
            "format": fmt,
            "size_kb": round(out.stat().st_size / 1024, 1) if out.exists() else 0,
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        hwp.quit()


def _convert_to_hwp(inp: Path, output_path: str) -> dict:
    """DOCX/TXT/MD → HWP 변환."""
    try:
        from pyhwpx import Hwp
    except ImportError:
        return {"error": "HWP 생성은 한컴오피스 한글 + pyhwpx 필요"}

    ext = inp.suffix.lower()

    if ext == ".docx":
        # DOCX → HWP: 한글에서 직접 열기
        hwp = Hwp(visible=False)
        try:
            hwp.open(str(inp.resolve()))
            out = Path(output_path).resolve()
            hwp.save_as(str(out))
            return {
                "status": "success",
                "input": inp.name,
                "output": str(out),
                "format": "hwp",
            }
        finally:
            hwp.quit()

    elif ext in (".txt", ".md"):
        # TXT/MD → HWP: 텍스트 읽어서 생성
        text = inp.read_text(encoding="utf-8")
        from hwp_writer import create_hwp
        return create_hwp(output_path, text)

    else:
        return {"error": f"HWP 변환을 지원하지 않는 입력 포맷: {ext}"}


def batch_convert(input_dir: str, output_format: str, output_dir: str = None) -> dict:
    """디렉토리의 모든 HWP 파일을 일괄 변환합니다."""
    inp_dir = Path(input_dir)
    if not inp_dir.is_dir():
        return {"error": f"디렉토리가 아닙니다: {input_dir}"}

    out_dir = Path(output_dir) if output_dir else inp_dir / "converted"
    out_dir.mkdir(parents=True, exist_ok=True)

    hwp_files = list(inp_dir.glob("*.hwp")) + list(inp_dir.glob("*.hwpx"))
    results = {"total": len(hwp_files), "success": 0, "failed": 0, "files": []}

    for hwp_file in hwp_files:
        out_path = out_dir / hwp_file.with_suffix(f".{output_format}").name
        result = convert_hwp(str(hwp_file), output_format, str(out_path))

        if result.get("status") == "success":
            results["success"] += 1
        else:
            results["failed"] += 1

        results["files"].append({
            "input": hwp_file.name,
            "status": result.get("status", "error"),
            "output": result.get("output", ""),
        })

    return results


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python hwp_converter.py <input.hwp> <format>        — 단일 변환")
        print("  python hwp_converter.py <input.hwp> <format> <out>  — 출력 경로 지정")
        print("  python hwp_converter.py --batch <dir> <format>      — 일괄 변환")
        print()
        print("Formats: txt, md, pdf, docx, hwp")
        sys.exit(1)

    if sys.argv[1] == "--batch":
        result = batch_convert(sys.argv[2], sys.argv[3],
                               sys.argv[4] if len(sys.argv) > 4 else None)
    else:
        out = sys.argv[3] if len(sys.argv) > 3 else None
        result = convert_hwp(sys.argv[1], sys.argv[2], out)

    print(json.dumps(result, ensure_ascii=False, indent=2))
