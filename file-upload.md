# File Upload Skill

> 파일 업로드. "파일 업로드", "이미지 업로드", "S3", "업로드" 트리거.

## Vercel Blob (간단한 경우)

### 설치
```bash
npm install @vercel/blob
```

### 업로드 API
```typescript
// app/api/upload/route.ts
import { put } from '@vercel/blob';
import { NextResponse } from 'next/server';

export async function POST(req: Request) {
  const formData = await req.formData();
  const file = formData.get('file') as File;

  if (!file) {
    return NextResponse.json({ error: 'No file' }, { status: 400 });
  }

  const blob = await put(file.name, file, {
    access: 'public',
  });

  return NextResponse.json(blob);
}
```

### 클라이언트
```tsx
'use client';

export function UploadForm() {
  const [uploading, setUploading] = useState(false);

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    const res = await fetch('/api/upload', {
      method: 'POST',
      body: formData,
    });

    const { url } = await res.json();
    console.log('Uploaded:', url);
    setUploading(false);
  };

  return (
    <input
      type="file"
      onChange={handleUpload}
      disabled={uploading}
    />
  );
}
```

## AWS S3

### 설치
```bash
npm install @aws-sdk/client-s3 @aws-sdk/s3-request-presigner
```

### 환경변수
```env
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=ap-northeast-2
AWS_S3_BUCKET=your-bucket
```

### S3 클라이언트
```typescript
// lib/s3.ts
import { S3Client, PutObjectCommand, GetObjectCommand } from '@aws-sdk/client-s3';
import { getSignedUrl } from '@aws-sdk/s3-request-presigner';

export const s3 = new S3Client({
  region: process.env.AWS_REGION,
  credentials: {
    accessKeyId: process.env.AWS_ACCESS_KEY_ID!,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY!,
  },
});

// Presigned URL 생성 (업로드용)
export async function getUploadUrl(key: string, contentType: string) {
  const command = new PutObjectCommand({
    Bucket: process.env.AWS_S3_BUCKET,
    Key: key,
    ContentType: contentType,
  });

  return getSignedUrl(s3, command, { expiresIn: 3600 });
}

// Presigned URL 생성 (다운로드용)
export async function getDownloadUrl(key: string) {
  const command = new GetObjectCommand({
    Bucket: process.env.AWS_S3_BUCKET,
    Key: key,
  });

  return getSignedUrl(s3, command, { expiresIn: 3600 });
}
```

### API Route
```typescript
// app/api/upload/presign/route.ts
import { getUploadUrl } from '@/lib/s3';
import { NextResponse } from 'next/server';
import { nanoid } from 'nanoid';

export async function POST(req: Request) {
  const { filename, contentType } = await req.json();

  const key = `uploads/${nanoid()}-${filename}`;
  const url = await getUploadUrl(key, contentType);

  return NextResponse.json({ url, key });
}
```

### 클라이언트 (Presigned URL 사용)
```tsx
async function uploadToS3(file: File) {
  // 1. Presigned URL 획득
  const res = await fetch('/api/upload/presign', {
    method: 'POST',
    body: JSON.stringify({
      filename: file.name,
      contentType: file.type,
    }),
  });
  const { url, key } = await res.json();

  // 2. S3에 직접 업로드
  await fetch(url, {
    method: 'PUT',
    body: file,
    headers: { 'Content-Type': file.type },
  });

  return `https://${process.env.NEXT_PUBLIC_S3_BUCKET}.s3.amazonaws.com/${key}`;
}
```

## 이미지 최적화

### Next.js Image
```tsx
import Image from 'next/image';

<Image
  src={uploadedUrl}
  alt="Uploaded"
  width={400}
  height={300}
  className="object-cover"
/>
```

### 업로드 전 리사이즈
```typescript
async function resizeImage(file: File, maxWidth: number): Promise<Blob> {
  return new Promise((resolve) => {
    const img = new window.Image();
    img.onload = () => {
      const canvas = document.createElement('canvas');
      const ratio = maxWidth / img.width;
      canvas.width = maxWidth;
      canvas.height = img.height * ratio;

      const ctx = canvas.getContext('2d')!;
      ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

      canvas.toBlob((blob) => resolve(blob!), 'image/jpeg', 0.8);
    };
    img.src = URL.createObjectURL(file);
  });
}
```

## 드래그 앤 드롭
```tsx
'use client';
import { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';

export function Dropzone({ onUpload }: { onUpload: (file: File) => void }) {
  const onDrop = useCallback((files: File[]) => {
    if (files[0]) onUpload(files[0]);
  }, [onUpload]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'image/*': ['.png', '.jpg', '.jpeg'] },
    maxSize: 5 * 1024 * 1024, // 5MB
  });

  return (
    <div
      {...getRootProps()}
      className={`border-2 border-dashed p-8 text-center cursor-pointer
        ${isDragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300'}`}
    >
      <input {...getInputProps()} />
      {isDragActive ? '여기에 놓으세요' : '클릭하거나 파일을 드래그하세요'}
    </div>
  );
}
```
