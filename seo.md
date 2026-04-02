# SEO Skill (OpenClaw Style)

> SEO 최적화 워크플로우. "SEO", "검색엔진", "메타태그", "검색 최적화" 트리거.

## 기술적 SEO 체크리스트

### 1. 메타 태그
```html
<head>
  <title>주요 키워드 - 브랜드명</title>
  <meta name="description" content="155자 이내 설명, 키워드 포함, 행동 유도" />
  <meta name="robots" content="index, follow" />
  <link rel="canonical" href="https://example.com/page" />
</head>
```

### 2. Open Graph
```html
<meta property="og:title" content="제목" />
<meta property="og:description" content="설명" />
<meta property="og:image" content="https://example.com/image.jpg" />
<meta property="og:url" content="https://example.com/page" />
<meta property="og:type" content="website" />
```

### 3. Twitter Cards
```html
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="제목" />
<meta name="twitter:description" content="설명" />
<meta name="twitter:image" content="이미지URL" />
```

## Next.js SEO

### Metadata API
```typescript
// app/page.tsx
export const metadata: Metadata = {
  title: '페이지 제목',
  description: '페이지 설명',
  openGraph: {
    title: '제목',
    description: '설명',
    images: ['/og-image.jpg'],
  },
};
```

### 동적 메타데이터
```typescript
export async function generateMetadata({ params }): Promise<Metadata> {
  const post = await getPost(params.slug);
  return {
    title: post.title,
    description: post.excerpt,
  };
}
```

### Sitemap
```typescript
// app/sitemap.ts
export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const posts = await getPosts();

  return [
    { url: 'https://example.com', lastModified: new Date() },
    ...posts.map((post) => ({
      url: `https://example.com/blog/${post.slug}`,
      lastModified: post.updatedAt,
    })),
  ];
}
```

### robots.txt
```typescript
// app/robots.ts
export default function robots(): MetadataRoute.Robots {
  return {
    rules: { userAgent: '*', allow: '/', disallow: '/private/' },
    sitemap: 'https://example.com/sitemap.xml',
  };
}
```

## 구조화된 데이터 (JSON-LD)

```typescript
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "제목",
  "author": { "@type": "Person", "name": "작성자" },
  "datePublished": "2024-01-01",
  "image": "이미지URL"
}
</script>
```

## 성능 = SEO

### Core Web Vitals
- LCP < 2.5s
- FID < 100ms
- CLS < 0.1

### 최적화 방법
- 이미지: WebP, lazy loading
- 폰트: font-display: swap
- JS: 코드 스플리팅

## 검사 도구
```bash
# Lighthouse
npx lighthouse https://site.com

# 구조화된 데이터 테스트
https://search.google.com/test/rich-results
```
