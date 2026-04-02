# Refactoring Skill (OpenClaw Style)

> 코드 리팩토링. "리팩토링", "정리해줘", "클린코드", "refactor" 트리거.

## 리팩토링 원칙

1. **테스트 먼저** - 기존 동작 보장
2. **작은 단계** - 한 번에 하나씩
3. **커밋 자주** - 롤백 가능하게

## 코드 스멜 & 해결책

### 1. 긴 함수 → 추출
```typescript
// ❌ Before: 100줄 함수
function processOrder(order) {
  // 검증 로직 30줄
  // 계산 로직 30줄
  // 저장 로직 40줄
}

// ✅ After: 분리
function processOrder(order) {
  validateOrder(order);
  const total = calculateTotal(order);
  return saveOrder(order, total);
}
```

### 2. 중복 코드 → 통합
```typescript
// ❌ Before
function getUserName(user) { return user.name; }
function getProductName(product) { return product.name; }

// ✅ After
function getName<T extends { name: string }>(item: T) {
  return item.name;
}
```

### 3. 긴 매개변수 → 객체화
```typescript
// ❌ Before
function createUser(name, email, age, address, phone, role) {}

// ✅ After
interface CreateUserDTO {
  name: string;
  email: string;
  age: number;
  address?: string;
  phone?: string;
  role: 'user' | 'admin';
}
function createUser(data: CreateUserDTO) {}
```

### 4. 조건문 복잡도 → 전략 패턴
```typescript
// ❌ Before
function getPrice(type) {
  if (type === 'basic') return 10;
  if (type === 'pro') return 20;
  if (type === 'enterprise') return 50;
}

// ✅ After
const PRICES = {
  basic: 10,
  pro: 20,
  enterprise: 50,
} as const;

function getPrice(type: keyof typeof PRICES) {
  return PRICES[type];
}
```

### 5. 매직 넘버 → 상수화
```typescript
// ❌ Before
if (status === 1) {}
setTimeout(fn, 86400000);

// ✅ After
const STATUS = { ACTIVE: 1, INACTIVE: 0 } as const;
const ONE_DAY_MS = 24 * 60 * 60 * 1000;

if (status === STATUS.ACTIVE) {}
setTimeout(fn, ONE_DAY_MS);
```

## 구조적 리팩토링

### 파일 구조 정리
```
src/
├── components/     # UI 컴포넌트
├── hooks/          # 커스텀 훅
├── lib/            # 유틸리티
├── services/       # API/비즈니스 로직
├── types/          # 타입 정의
└── utils/          # 순수 함수
```

### 의존성 정리
```bash
# 사용하지 않는 의존성 찾기
npx depcheck

# 정리
npm uninstall unused-package
```

## 리팩토링 체크리스트
- [ ] 테스트 통과 확인
- [ ] 타입 에러 없음
- [ ] 린트 에러 없음
- [ ] 기능 동일하게 동작
- [ ] 성능 저하 없음
