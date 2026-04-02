# 빌드 검증 자동화 루프

> Godogen 방식: 빌드 → 에러 감지 → 자동 수정 → 재빌드 (에러 0까지 반복)

## 검증 프로세스

### Step 1: TypeScript 컴파일 체크
```bash
npx tsc --noEmit 2>&1
```

에러 파싱 패턴:
```
src/app/page.tsx(15,3): error TS2345: Argument of type 'string' is not assignable...
→ 파일: src/app/page.tsx, 라인: 15, 컬럼: 3, 에러코드: TS2345
```

### Step 2: ESLint 체크
```bash
npx next lint 2>&1
```

### Step 3: 빌드 체크
```bash
npm run build 2>&1
```

## 자동 수정 전략

### TypeScript 에러 유형별 수정

```yaml
TS2307 (모듈 없음):
  원인: import 경로 오류
  수정: 올바른 경로 찾아 수정

TS2345 (타입 불일치):
  원인: 함수 인자 타입 불일치
  수정: 타입 캐스팅 또는 인터페이스 수정

TS2339 (프로퍼티 없음):
  원인: 타입에 없는 프로퍼티 접근
  수정: 인터페이스에 프로퍼티 추가 또는 옵셔널 체이닝

TS2322 (타입 할당 불가):
  원인: 변수에 잘못된 타입 할당
  수정: 타입 정의 수정

TS7006 (암시적 any):
  원인: 타입 미지정
  수정: 명시적 타입 추가

TS2304 (이름 없음):
  원인: import 누락
  수정: 필요한 import 추가

TS6133 (미사용 변수):
  원인: 선언 후 미사용
  수정: 제거 또는 _ 접두사

TS2554 (인자 수 불일치):
  원인: 함수 호출 시 인자 수 불일치
  수정: 인자 추가/제거 또는 옵셔널 파라미터

TS18047 (null 가능성):
  원인: null 체크 없음
  수정: null 체크 추가 또는 non-null assertion
```

### Next.js 빌드 에러 유형별 수정

```yaml
"Module not found":
  원인: 패키지 미설치 또는 경로 오류
  수정: npm install 또는 import 경로 수정

"'use client' directive":
  원인: 서버 컴포넌트에서 클라이언트 API 사용
  수정: 파일 최상단에 "use client" 추가

"Hydration mismatch":
  원인: 서버/클라이언트 렌더링 불일치
  수정: useEffect로 클라이언트 전용 코드 감싸기

"Dynamic server usage":
  원인: 정적 페이지에서 동적 함수 사용
  수정: export const dynamic = 'force-dynamic' 추가

"Invalid src prop":
  원인: next/image에 잘못된 src
  수정: next.config.ts에 도메인 추가 또는 src 수정

"Metadata cannot be used in Client Components":
  원인: 'use client' 파일에서 metadata export
  수정: metadata를 서버 컴포넌트 layout.tsx로 이동
```

## 루프 실행 절차

```
반복 = 0
최대반복 = 10

WHILE 반복 < 최대반복:
  1. npm run build 실행
  2. IF 성공:
       PRINT "✅ 빌드 성공! 배포 준비 완료"
       BREAK
  3. 에러 목록 파싱
  4. EACH 에러:
       a. 에러 파일 읽기
       b. 에러 유형 분류
       c. 자동 수정 적용
  5. 반복 += 1
  6. IF 반복 === 최대반복:
       PRINT "❌ 최대 반복 도달. 수동 확인 필요"
       에러 목록 출력
```

## 빌드 후 최종 체크리스트

```yaml
코드 품질:
  - [ ] TypeScript 에러 0개
  - [ ] ESLint 경고 0개
  - [ ] 빌드 성공

보안:
  - [ ] .env.local에 시크릿 하드코딩 없음
  - [ ] RLS 정책 모든 테이블 적용
  - [ ] API 라우트 인증 체크

기능:
  - [ ] 모든 페이지 라우트 접근 가능
  - [ ] 인증 플로우 정상
  - [ ] 게이미피케이션 로직 동작
  - [ ] 결제 플로우 (Stripe 테스트 모드)

UI/UX:
  - [ ] 모바일 반응형 (320px~)
  - [ ] 다크모드 지원
  - [ ] 로딩 상태 표시
  - [ ] 에러 상태 표시
  - [ ] 빈 상태 표시
```
