#!/usr/bin/env python3
"""
HWP Reader — HWP/HWPX 파일 텍스트 추출
방법 1: pyhwpx COM 자동화 (한글 설치 시)
방법 2: olefile OLE 직접 파싱 (한글 미설치 시)
방법 3: HWPX XML 직접 파싱 (한글 미설치 시)
"""

import json
import os
import re
import sys
import struct
import zlib
from pathlib import Path


def read_hwp(file_path: str) -> dict:
    """HWP 파일을 읽어 텍스트와 메타데이터를 반환합니다."""
    path = Path(file_path)
    if not path.exists():
        return {"error": f"파일을 찾을 수 없습니다: {file_path}"}

    ext = path.suffix.lower()

    if ext == ".hwpx":
        return _read_hwpx(path)

    # HWP: COM 자동화 시도 → 실패 시 OLE 파싱
    try:
        return _read_hwp_com(path)
    except Exception as e_com:
        try:
            return _read_hwp_ole(path)
        except Exception as e_ole:
            return {
                "error": f"COM 자동화 실패: {e_com}\nOLE 파싱 실패: {e_ole}",
                "hint": "한컴오피스 한글이 설치되지 않았거나 파일이 손상되었습니다.",
            }


def _read_hwp_com(path: Path) -> dict:
    """pyhwpx COM 자동화로 HWP 읽기 (한글 설치 필요)."""
    from pyhwpx import Hwp

    hwp = Hwp(visible=False)
    try:
        hwp.open(str(path.resolve()))

        # 전체 텍스트 추출
        hwp.init_scan()
        texts = []
        while True:
            result = hwp.get_text()
            if result[0] == 1:  # 텍스트 있음
                text = result[1].strip()
                if text:
                    texts.append(text)
            elif result[0] == 0:  # 끝
                break

        full_text = "\n".join(texts)

        # 문서 정보
        info = {
            "file": path.name,
            "method": "COM (pyhwpx)",
            "text": full_text,
            "char_count": len(full_text),
            "line_count": full_text.count("\n") + 1,
            "page_count": hwp.PageCount if hasattr(hwp, 'PageCount') else "N/A",
        }

        return info
    finally:
        hwp.quit()


def _read_hwp_ole(path: Path) -> dict:
    """olefile OLE 파싱으로 HWP 텍스트 추출 (한글 미설치)."""
    import olefile

    if not olefile.isOleFile(str(path)):
        raise ValueError("유효한 OLE (HWP) 파일이 아닙니다.")

    ole = olefile.OleFileIO(str(path))
    try:
        texts = []

        # 문서 속성
        meta = {}
        if ole.exists("\\x05HwpSummaryInformation"):
            try:
                si = ole.getproperties("\\x05HwpSummaryInformation")
                meta["title"] = si.get(2, "")
                meta["subject"] = si.get(3, "")
                meta["author"] = si.get(4, "")
                meta["keywords"] = si.get(5, "")
                meta["comments"] = si.get(6, "")
            except Exception:
                pass

        # 본문 스트림에서 텍스트 추출
        # HWP 파일 헤더 확인
        if ole.exists("FileHeader"):
            header_data = ole.openstream("FileHeader").read()
            # 압축 여부 확인 (offset 36, bit 0)
            compressed = bool(header_data[36] & 0x01) if len(header_data) > 36 else False
        else:
            compressed = False

        # BodyText 섹션에서 텍스트 추출
        section_idx = 0
        while True:
            stream_name = f"BodyText/Section{section_idx}"
            if not ole.exists(stream_name):
                break

            data = ole.openstream(stream_name).read()

            if compressed:
                try:
                    data = zlib.decompress(data, -15)
                except zlib.error:
                    try:
                        data = zlib.decompress(data)
                    except zlib.error:
                        pass

            # 바이너리에서 한글 텍스트 추출
            extracted = _extract_text_from_body(data)
            if extracted:
                texts.append(extracted)

            section_idx += 1

        full_text = "\n\n".join(texts)

        return {
            "file": path.name,
            "method": "OLE (olefile) — 텍스트만 추출",
            "text": full_text,
            "char_count": len(full_text),
            "line_count": full_text.count("\n") + 1,
            "meta": meta,
            "sections": section_idx,
        }
    finally:
        ole.close()


def _extract_text_from_body(data: bytes) -> str:
    """HWP BodyText 바이너리에서 텍스트를 추출합니다."""
    texts = []
    pos = 0

    while pos < len(data) - 4:
        # HWP 레코드 헤더 파싱 (4바이트)
        try:
            header = struct.unpack_from("<I", data, pos)[0]
        except struct.error:
            break

        tag_id = header & 0x3FF
        level = (header >> 10) & 0x3FF
        size = (header >> 20) & 0xFFF

        if size == 0xFFF:
            # 확장 크기
            if pos + 8 > len(data):
                break
            size = struct.unpack_from("<I", data, pos + 4)[0]
            pos += 8
        else:
            pos += 4

        if pos + size > len(data):
            break

        # HWPTAG_PARA_TEXT = 67 (0x43)
        if tag_id == 67:
            # UTF-16LE 텍스트 추출
            text_data = data[pos:pos + size]
            try:
                text = ""
                i = 0
                while i < len(text_data) - 1:
                    char_code = struct.unpack_from("<H", text_data, i)[0]
                    i += 2

                    if char_code == 0:
                        break
                    elif char_code < 32:
                        # 제어 문자 처리
                        if char_code == 13:  # 줄바꿈
                            text += "\n"
                        elif char_code == 10:
                            text += "\n"
                        elif char_code in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31):
                            # 특수 제어 코드 (인라인, 확장 등) — 건너뛰기
                            if char_code in (1, 2, 3, 11, 12, 14, 15, 16, 17, 18, 21, 22, 23):
                                i += 14  # 확장 문자 크기
                        continue
                    else:
                        text += chr(char_code)

                text = text.strip()
                if text:
                    texts.append(text)
            except Exception:
                pass

        pos += size

    return "\n".join(texts)


def _read_hwpx(path: Path) -> dict:
    """HWPX (Open XML 기반) 파일 읽기."""
    import zipfile

    if not zipfile.is_zipfile(str(path)):
        return {"error": "유효한 HWPX 파일이 아닙니다."}

    texts = []
    meta = {}

    with zipfile.ZipFile(str(path), "r") as zf:
        # 목록 확인
        names = zf.namelist()

        # 메타데이터 (META-INF/manifest.xml 또는 settings.xml)
        for name in names:
            if "meta" in name.lower() and name.endswith(".xml"):
                try:
                    content = zf.read(name).decode("utf-8", errors="ignore")
                    # 간단한 메타 추출
                    title_match = re.search(r"<dc:title>(.*?)</dc:title>", content)
                    if title_match:
                        meta["title"] = title_match.group(1)
                    author_match = re.search(r"<dc:creator>(.*?)</dc:creator>", content)
                    if author_match:
                        meta["author"] = author_match.group(1)
                except Exception:
                    pass

        # 본문 텍스트 (Contents/section*.xml)
        section_files = sorted([n for n in names if "section" in n.lower() and n.endswith(".xml")])

        for sf in section_files:
            try:
                content = zf.read(sf).decode("utf-8", errors="ignore")
                # XML에서 텍스트 추출
                text = re.sub(r"<[^>]+>", "", content)
                text = re.sub(r"\s+", " ", text).strip()
                if text:
                    texts.append(text)
            except Exception:
                pass

    full_text = "\n\n".join(texts)

    return {
        "file": path.name,
        "method": "HWPX (ZIP/XML 파싱)",
        "text": full_text,
        "char_count": len(full_text),
        "line_count": full_text.count("\n") + 1,
        "meta": meta,
        "sections": len([n for n in zipfile.ZipFile(str(path)).namelist() if "section" in n.lower()]),
    }


def read_hwp_tables(file_path: str) -> dict:
    """HWP 파일에서 표(Table) 데이터를 추출합니다 (COM 필요)."""
    try:
        from pyhwpx import Hwp
    except ImportError:
        return {"error": "표 추출은 pyhwpx (한글 설치) 필요"}

    hwp = Hwp(visible=False)
    try:
        hwp.open(str(Path(file_path).resolve()))

        tables = []
        # 표 찾기 시도
        hwp.MovePos(2)  # 문서 시작
        table_idx = 0

        while hwp.find_ctrl("tbl"):
            table_data = []
            # 표 안의 셀 텍스트 추출 시도
            try:
                cell_texts = hwp.get_table_text()
                if cell_texts:
                    tables.append({
                        "table_index": table_idx,
                        "data": cell_texts,
                    })
            except Exception:
                pass
            table_idx += 1
            if table_idx > 100:
                break

        return {
            "file": Path(file_path).name,
            "tables_found": len(tables),
            "tables": tables,
        }
    finally:
        hwp.quit()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python hwp_reader.py <file.hwp|hwpx> [--tables]")
        sys.exit(1)

    file_path = sys.argv[1]
    if "--tables" in sys.argv:
        result = read_hwp_tables(file_path)
    else:
        result = read_hwp(file_path)

    if "text" in result and len(result["text"]) > 2000:
        preview = result["text"][:2000] + f"\n\n... ({result['char_count']:,}자 중 2000자 미리보기)"
        result["text_preview"] = preview
        del result["text"]

    print(json.dumps(result, ensure_ascii=False, indent=2))
