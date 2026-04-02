# Presentation Skill (OpenClaw Style)

> 프레젠테이션/PPT 생성 워크플로우. "PPT", "프레젠테이션", "발표", "슬라이드" 트리거.

## 프레젠테이션 구조

### 기본 구조 (10분 발표)
```
1. Hook (1슬라이드) - 주의 끌기
2. Problem (2슬라이드) - 문제 정의
3. Solution (3슬라이드) - 해결책
4. Demo/Proof (2슬라이드) - 증거
5. Call to Action (1슬라이드) - 행동 유도
6. Q&A (1슬라이드)
```

### 피치덱 구조
```
1. Cover - 로고, 한 줄 소개
2. Problem - 해결하려는 문제
3. Solution - 우리의 해결책
4. Product - 제품 스크린샷/데모
5. Market - 시장 규모
6. Business Model - 수익 모델
7. Traction - 성과 지표
8. Team - 팀 소개
9. Ask - 투자 요청
```

## 슬라이드 디자인 원칙

### 1. 하나의 메시지
```
❌ 한 슬라이드에 5가지 내용
✅ 한 슬라이드 = 한 가지 핵심 메시지
```

### 2. 텍스트 최소화
```
❌ 문단으로 된 긴 설명
✅ 키워드 + 시각 자료
```

### 3. 시각적 계층
```
- 제목: 큰 글씨, 굵게
- 핵심 포인트: 중간 글씨
- 부가 설명: 작은 글씨 (최소화)
```

## Reveal.js로 웹 프레젠테이션

### 설치
```bash
npm install reveal.js
```

### 기본 구조
```html
<div class="reveal">
  <div class="slides">
    <section>
      <h1>제목</h1>
      <p>부제목</p>
    </section>
    <section>
      <h2>슬라이드 2</h2>
      <ul>
        <li>포인트 1</li>
        <li>포인트 2</li>
      </ul>
    </section>
  </div>
</div>

<script>
  Reveal.initialize({
    hash: true,
    transition: 'slide'
  });
</script>
```

### 코드 하이라이팅
```html
<section>
  <pre><code data-trim data-noescape>
    const hello = 'world';
  </code></pre>
</section>
```

## Marp (Markdown → 슬라이드)

### 설치
```bash
npm install -g @marp-team/marp-cli
```

### 작성
```markdown
---
marp: true
theme: default
---

# 제목

---

## 슬라이드 2

- 포인트 1
- 포인트 2

---

## 이미지

![bg right:40%](image.jpg)

왼쪽 텍스트
```

### 변환
```bash
marp presentation.md -o output.pdf
marp presentation.md -o output.html
marp presentation.md -o output.pptx
```

## 발표 팁

### 시작
- 질문으로 시작
- 충격적인 통계
- 스토리텔링

### 진행
- 아이 컨택
- 적절한 페이싱
- 청중 참여 유도

### 마무리
- 핵심 요약
- 명확한 CTA
- 여운 남기기

## 체크리스트
- [ ] 10초 안에 핵심 전달되는가
- [ ] 폰트 크기 충분한가 (최소 24pt)
- [ ] 색상 대비 충분한가
- [ ] 발표 시간 체크
- [ ] 백업 준비 (PDF)
