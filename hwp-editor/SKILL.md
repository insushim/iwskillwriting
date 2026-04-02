# HWP Editor Skill

> **Trigger**: `/hwp`, "HWP", "hwp", "한글 파일", "한글 문서", "HWP 읽어", "HWP 수정", "한글 열어", ".hwp", ".hwpx"
> **Description**: HWP/HWPX 파일을 읽고, 수정하고, 생성하는 스킬. 한컴오피스 한글 COM 자동화 + OLE 직접 파싱 이중 지원.

---

## 핵심 기능

### 1. HWP 읽기 (Read)
- HWP/HWPX 파일에서 텍스트 추출
- 표(Table) 데이터 추출
- 문서 속성(제목, 저자, 페이지 수) 읽기
- 한글 미설치 환경에서도 OLE 파싱으로 텍스트 추출 가능

### 2. HWP 수정 (Edit)
- 텍스트 찾기/바꾸기
- 특정 위치에 텍스트 삽입
- 표 데이터 수정
- 글꼴/크기/스타일 변경
- 머리글/바닥글 설정

### 3. HWP 생성 (Create)
- 마크다운 → HWP 변환
- 텍스트 → HWP 변환
- 템플릿 기반 HWP 생성
- 표 자동 생성

### 4. HWP 변환 (Convert)
- HWP → DOCX 변환
- HWP → PDF 변환
- HWP → TXT 변환
- HWP → 마크다운 변환
- DOCX → HWP 변환

---

## 사용 환경

### 방법 1: 한컴오피스 한글 설치됨 (COM 자동화, 추천)
- `pyhwpx` 라이브러리 사용
- 모든 기능 완전 지원 (읽기/쓰기/수정/변환)
- Windows 전용

### 방법 2: 한글 미설치 (OLE 직접 파싱)
- `olefile` 라이브러리 사용
- 텍스트 추출만 가능 (읽기 전용)
- 모든 OS 지원

---

## 사용법

### 읽기
```
/hwp 이 파일 읽어줘: C:\문서\보고서.hwp
/hwp ~/Desktop/논문.hwpx 내용 보여줘
한글 파일 열어서 요약해줘
```

### 수정
```
/hwp 이 파일에서 "홍길동"을 "김철수"로 바꿔줘
/hwp 보고서.hwp의 3페이지에 표 추가해줘
한글 파일 수정해서 저장해줘
```

### 생성
```
/hwp 이 마크다운을 HWP로 변환해줘
/hwp 보고서 양식으로 HWP 만들어줘
한글 파일로 만들어줘
```

### 변환
```
/hwp 이 HWP를 PDF로 변환해줘
/hwp DOCX로 변환
/hwp 텍스트로 추출
```

---

## 스크립트

| 스크립트 | 기능 |
|---------|------|
| `hwp_reader.py` | HWP 읽기 (COM + OLE 이중 지원) |
| `hwp_writer.py` | HWP 생성/수정 (COM 자동화) |
| `hwp_converter.py` | HWP ↔ DOCX/PDF/TXT/MD 변환 |

---

## 의존성

```bash
# 필수
pip install olefile pyhwpx

# 선택 (DOCX 변환용)
pip install python-docx
```

---

## 제약 사항

- HWP 수정/생성은 **한컴오피스 한글이 설치된 Windows**에서만 가능
- 한글 미설치 시 **텍스트 추출(읽기)만** 가능 (OLE 파싱)
- HWPX(XML 기반)는 한글 없이도 일부 읽기/수정 가능
- 이미지/차트 등 OLE 개체는 텍스트 추출 시 제외
