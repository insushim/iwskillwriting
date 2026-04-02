---
name: seo-optimization
description: SEO optimization workflow. "SEO", "검색엔진", "메타태그", "검색 최적화" triggers this.
tools:
  - Read
  - Write
  - Edit
  - WebSearch
---

# SEO Optimization Skill

## Triggers
- "SEO", "검색엔진", "메타태그"
- "검색 최적화", "구글 순위", "sitemap"
- "search optimization", "keywords"

## Next.js SEO Setup

### Metadata API
```tsx
// app/layout.tsx
import { Metadata } from 'next';

export const metadata: Metadata = {
  metadataBase: new URL('https://example.com'),
  title: {
    default: 'Site Name',
    template: '%s | Site Name',
  },
  description: 'Your site description (150-160 chars)',
  keywords: ['keyword1', 'keyword2', 'keyword3'],
  authors: [{ name: 'Author Name' }],
  creator: 'Creator Name',
  openGraph: {
    type: 'website',
    locale: 'ko_KR',
    url: 'https://example.com',
    siteName: 'Site Name',
    title: 'Site Name',
    description: 'Your site description',
    images: [
      {
        url: '/og-image.png',
        width: 1200,
        height: 630,
        alt: 'Site preview',
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Site Name',
    description: 'Your site description',
    images: ['/twitter-image.png'],
    creator: '@username',
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
  verification: {
    google: 'google-verification-code',
    yandex: 'yandex-verification-code',
  },
};
```

### Page-Specific Metadata
```tsx
// app/blog/[slug]/page.tsx
import { Metadata } from 'next';

type Props = { params: { slug: string } };

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const post = await getPost(params.slug);

  return {
    title: post.title,
    description: post.excerpt,
    openGraph: {
      title: post.title,
      description: post.excerpt,
      type: 'article',
      publishedTime: post.publishedAt,
      authors: [post.author.name],
      images: [post.coverImage],
    },
  };
}
```

### Sitemap
```tsx
// app/sitemap.ts
import { MetadataRoute } from 'next';

export default async function sitemap(): MetadataRoute.Sitemap {
  const posts = await getAllPosts();

  const postUrls = posts.map((post) => ({
    url: `https://example.com/blog/${post.slug}`,
    lastModified: post.updatedAt,
    changeFrequency: 'weekly' as const,
    priority: 0.8,
  }));

  return [
    {
      url: 'https://example.com',
      lastModified: new Date(),
      changeFrequency: 'daily',
      priority: 1,
    },
    {
      url: 'https://example.com/about',
      lastModified: new Date(),
      changeFrequency: 'monthly',
      priority: 0.5,
    },
    ...postUrls,
  ];
}
```

### Robots.txt
```tsx
// app/robots.ts
import { MetadataRoute } from 'next';

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      {
        userAgent: '*',
        allow: '/',
        disallow: ['/api/', '/admin/', '/private/'],
      },
    ],
    sitemap: 'https://example.com/sitemap.xml',
  };
}
```

### JSON-LD Structured Data
```tsx
// components/JsonLd.tsx
export function ArticleJsonLd({ post }: { post: Post }) {
  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: post.title,
    description: post.excerpt,
    image: post.coverImage,
    datePublished: post.publishedAt,
    dateModified: post.updatedAt,
    author: {
      '@type': 'Person',
      name: post.author.name,
    },
    publisher: {
      '@type': 'Organization',
      name: 'Site Name',
      logo: {
        '@type': 'ImageObject',
        url: 'https://example.com/logo.png',
      },
    },
  };

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
    />
  );
}
```

## SEO Checklist
```yaml
technical:
  - [ ] HTTPS enabled
  - [ ] Mobile responsive
  - [ ] Fast loading (< 3s)
  - [ ] Valid HTML
  - [ ] sitemap.xml exists
  - [ ] robots.txt configured
  - [ ] Canonical URLs set
  - [ ] 404 page exists

on_page:
  - [ ] Unique title per page (50-60 chars)
  - [ ] Meta description (150-160 chars)
  - [ ] H1 tag (one per page)
  - [ ] Image alt text
  - [ ] Internal linking
  - [ ] Keyword in URL
  - [ ] Structured data

content:
  - [ ] Original, valuable content
  - [ ] Regular updates
  - [ ] Proper heading hierarchy
  - [ ] Readable (Flesch score > 60)
```

## Performance for SEO
```tsx
// next.config.js
module.exports = {
  images: {
    formats: ['image/avif', 'image/webp'],
    remotePatterns: [
      { protocol: 'https', hostname: '**.example.com' },
    ],
  },
  experimental: {
    optimizeCss: true,
  },
};
```
