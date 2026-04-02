# Deployment Skill (OpenClaw Style)

> 프로덕션 배포 워크플로우. "배포", "deploy", "올려줘", "프로덕션" 트리거.

## 자동 실행 조건
- 배포 요청 시
- "production", "staging" 언급 시
- Vercel/Netlify/Railway 언급 시

## 배포 전 체크리스트

### 1. 코드 품질 검증
```bash
# 타입 체크
npm run typecheck || npx tsc --noEmit

# 린트
npm run lint

# 테스트
npm test
```

### 2. 빌드 검증
```bash
npm run build
```

### 3. 환경변수 확인
- .env.production 존재 확인
- 필수 변수 검증 (DATABASE_URL, API_KEY 등)

## 플랫폼별 배포

### Vercel
```bash
# 프리뷰 배포
vercel

# 프로덕션 배포
vercel --prod
```

### Netlify
```bash
netlify deploy --prod
```

### Railway
```bash
railway up
```

### Docker
```bash
docker build -t app:latest .
docker push registry/app:latest
```

## 배포 후 검증

### 1. 헬스체크
```bash
curl -f https://your-domain.com/api/health
```

### 2. 스모크 테스트
- 메인 페이지 로드 확인
- API 응답 확인
- 로그인/핵심 기능 테스트

## 롤백 절차
```bash
# Vercel 롤백
vercel rollback

# Git 기반 롤백
git revert HEAD && git push
```
