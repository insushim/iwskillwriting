# State Management Skill

> 상태 관리. "상태", "state", "zustand", "전역 상태" 트리거.

## Zustand (권장)

### 설치
```bash
npm install zustand
```

### 기본 스토어
```typescript
// store/user-store.ts
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface User {
  id: string;
  name: string;
  email: string;
}

interface UserStore {
  user: User | null;
  isLoading: boolean;
  setUser: (user: User | null) => void;
  logout: () => void;
}

export const useUserStore = create<UserStore>()(
  persist(
    (set) => ({
      user: null,
      isLoading: false,
      setUser: (user) => set({ user }),
      logout: () => set({ user: null }),
    }),
    { name: 'user-storage' }
  )
);
```

### 비동기 액션
```typescript
interface ProductStore {
  products: Product[];
  isLoading: boolean;
  error: string | null;
  fetchProducts: () => Promise<void>;
  addProduct: (product: Product) => void;
}

export const useProductStore = create<ProductStore>((set, get) => ({
  products: [],
  isLoading: false,
  error: null,

  fetchProducts: async () => {
    set({ isLoading: true, error: null });
    try {
      const res = await fetch('/api/products');
      const data = await res.json();
      set({ products: data, isLoading: false });
    } catch (error) {
      set({ error: 'Failed to fetch', isLoading: false });
    }
  },

  addProduct: (product) => {
    set({ products: [...get().products, product] });
  },
}));
```

### 컴포넌트에서 사용
```tsx
'use client';
import { useUserStore } from '@/store/user-store';

export function Header() {
  const { user, logout } = useUserStore();

  if (!user) return <LoginButton />;

  return (
    <div>
      <span>{user.name}</span>
      <button onClick={logout}>로그아웃</button>
    </div>
  );
}
```

## React Query (서버 상태)

### 설치
```bash
npm install @tanstack/react-query
```

### Provider 설정
```tsx
// app/providers.tsx
'use client';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const queryClient = new QueryClient();

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
}
```

### 데이터 페칭
```tsx
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

// 조회
export function useUsers() {
  return useQuery({
    queryKey: ['users'],
    queryFn: async () => {
      const res = await fetch('/api/users');
      return res.json();
    },
  });
}

// 생성/수정
export function useCreateUser() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (data: CreateUserDTO) => {
      const res = await fetch('/api/users', {
        method: 'POST',
        body: JSON.stringify(data),
      });
      return res.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
    },
  });
}
```

### 컴포넌트에서 사용
```tsx
export function UserList() {
  const { data: users, isLoading, error } = useUsers();
  const createUser = useCreateUser();

  if (isLoading) return <Skeleton />;
  if (error) return <Error />;

  return (
    <div>
      {users.map(user => <UserCard key={user.id} user={user} />)}
      <Button
        onClick={() => createUser.mutate({ name: 'New User' })}
        disabled={createUser.isPending}
      >
        추가
      </Button>
    </div>
  );
}
```

## 컨텍스트 (간단한 경우)

```tsx
'use client';
import { createContext, useContext, useState } from 'react';

interface ThemeContextType {
  theme: 'light' | 'dark';
  toggleTheme: () => void;
}

const ThemeContext = createContext<ThemeContextType | null>(null);

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');

  const toggleTheme = () => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light');
  };

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) throw new Error('useTheme must be used within ThemeProvider');
  return context;
}
```
