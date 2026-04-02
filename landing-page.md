# Landing Page Skill (OpenClaw Style)

> 랜딩페이지 생성. "랜딩페이지", "랜딩", "LP", "마케팅 페이지" 트리거.

## 랜딩페이지 구조

### 1. Hero Section
```tsx
<section className="min-h-screen flex items-center">
  <div className="container mx-auto px-4">
    <h1 className="text-5xl font-bold mb-4">
      [핵심 가치 제안]
    </h1>
    <p className="text-xl text-gray-600 mb-8">
      [부가 설명 1-2문장]
    </p>
    <div className="flex gap-4">
      <Button size="lg">무료로 시작하기</Button>
      <Button variant="outline">데모 보기</Button>
    </div>
  </div>
</section>
```

### 2. Problem Section
```tsx
<section className="py-20 bg-gray-50">
  <h2>이런 문제 겪고 계신가요?</h2>
  <div className="grid md:grid-cols-3 gap-8">
    <ProblemCard icon="😫" title="문제1" description="설명" />
    <ProblemCard icon="😤" title="문제2" description="설명" />
    <ProblemCard icon="😰" title="문제3" description="설명" />
  </div>
</section>
```

### 3. Solution/Features
```tsx
<section className="py-20">
  <h2>[제품명]으로 해결하세요</h2>
  <div className="grid md:grid-cols-2 gap-12">
    <FeatureCard
      title="기능 1"
      description="설명"
      image="/feature1.png"
    />
    {/* 반복 */}
  </div>
</section>
```

### 4. Social Proof
```tsx
<section className="py-20 bg-gray-50">
  <h2>고객들의 이야기</h2>
  <div className="grid md:grid-cols-3 gap-8">
    <TestimonialCard
      quote="정말 좋아요!"
      author="김철수"
      role="스타트업 CEO"
      avatar="/avatar.jpg"
    />
  </div>
  {/* 로고 벽 */}
  <div className="flex justify-center gap-8 mt-12 opacity-50">
    <img src="/logo1.svg" />
    <img src="/logo2.svg" />
  </div>
</section>
```

### 5. Pricing
```tsx
<section className="py-20">
  <h2>심플한 가격 정책</h2>
  <PricingTable plans={plans} />
</section>
```

### 6. FAQ
```tsx
<section className="py-20 bg-gray-50">
  <h2>자주 묻는 질문</h2>
  <Accordion items={faqs} />
</section>
```

### 7. CTA (Call to Action)
```tsx
<section className="py-20 bg-primary text-white text-center">
  <h2 className="text-4xl font-bold mb-4">
    지금 시작하세요
  </h2>
  <p className="mb-8">14일 무료 체험. 카드 등록 없음.</p>
  <Button size="lg" variant="secondary">
    무료로 시작하기
  </Button>
</section>
```

## 전환 최적화

### A/B 테스트 요소
- 헤드라인 문구
- CTA 버튼 색상/문구
- 가격 표시 방식
- 이미지 vs 비디오

### 필수 요소
- [ ] 명확한 가치 제안
- [ ] 사회적 증거 (후기, 로고)
- [ ] 신뢰 요소 (보안 배지, 보장)
- [ ] 단일 CTA 집중
- [ ] 모바일 최적화
- [ ] 빠른 로딩 (< 3초)

## 분석 설정
```typescript
// 전환 추적
gtag('event', 'conversion', {
  send_to: 'AW-XXXXX/XXXXX',
  value: 1.0,
  currency: 'USD',
});

// 히트맵
// Hotjar, Microsoft Clarity 연동
```
