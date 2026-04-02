---
name: refactoring-workflow
description: Code refactoring. "리팩토링", "정리", "클린코드", "구조 개선" triggers this.
tools:
  - Read
  - Write
  - Edit
  - Grep
  - Bash
---

# Refactoring Workflow Skill

## Triggers
- "리팩토링", "정리해줘", "클린코드"
- "구조 개선", "코드 정리"
- "refactor", "clean up"

## CRITICAL: Minimal Change
Only refactor what's requested. Do NOT change other code.

## Refactoring Patterns

### Extract Function
```typescript
// Before
function process(data) {
  // validation
  if (!data.name || data.name.length < 2) throw new Error('Invalid name');
  if (!data.email || !data.email.includes('@')) throw new Error('Invalid email');
  // processing
  return { ...data, processed: true };
}

// After
function validateData(data) {
  if (!data.name || data.name.length < 2) throw new Error('Invalid name');
  if (!data.email || !data.email.includes('@')) throw new Error('Invalid email');
}

function process(data) {
  validateData(data);
  return { ...data, processed: true };
}
```

### Replace Conditional with Early Return
```typescript
// Before
function getPrice(user) {
  let price = 100;
  if (user) {
    if (user.isPremium) {
      price = 80;
    } else if (user.hasCoupon) {
      price = 90;
    }
  }
  return price;
}

// After
function getPrice(user) {
  if (!user) return 100;
  if (user.isPremium) return 80;
  if (user.hasCoupon) return 90;
  return 100;
}
```

### Remove Duplication
```typescript
// Before
const userCard = `<div class="card"><h2>${user.name}</h2><p>${user.bio}</p></div>`;
const productCard = `<div class="card"><h2>${product.name}</h2><p>${product.desc}</p></div>`;

// After
const createCard = (title, content) =>
  `<div class="card"><h2>${title}</h2><p>${content}</p></div>`;

const userCard = createCard(user.name, user.bio);
const productCard = createCard(product.name, product.desc);
```

## Verification
```bash
npx tsc --noEmit
npm run lint
npm run build
npm test
```
