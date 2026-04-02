# UI Components Skill

> UI 컴포넌트 구현. "UI", "컴포넌트", "shadcn", "버튼", "폼" 트리거.

## shadcn/ui 설정

### 설치
```bash
npx shadcn@latest init
```

### 컴포넌트 추가
```bash
npx shadcn@latest add button card input form dialog table
```

## 필수 컴포넌트 패턴

### 버튼
```tsx
import { Button } from '@/components/ui/button';

// 변형
<Button>Default</Button>
<Button variant="destructive">Delete</Button>
<Button variant="outline">Outline</Button>
<Button variant="ghost">Ghost</Button>

// 로딩 상태
<Button disabled={isLoading}>
  {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
  저장
</Button>
```

### 폼 (React Hook Form + Zod)
```tsx
'use client';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';

const formSchema = z.object({
  email: z.string().email('유효한 이메일을 입력하세요'),
  name: z.string().min(2, '2자 이상 입력하세요'),
});

export function UserForm() {
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: { email: '', name: '' },
  });

  const onSubmit = async (values: z.infer<typeof formSchema>) => {
    // API 호출
  };

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <FormField
          control={form.control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>이메일</FormLabel>
              <FormControl>
                <Input placeholder="email@example.com" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="name"
          render={({ field }) => (
            <FormItem>
              <FormLabel>이름</FormLabel>
              <FormControl>
                <Input {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit" disabled={form.formState.isSubmitting}>
          저장
        </Button>
      </form>
    </Form>
  );
}
```

### 데이터 테이블
```tsx
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';

interface User {
  id: string;
  name: string;
  email: string;
}

export function UsersTable({ users }: { users: User[] }) {
  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>이름</TableHead>
          <TableHead>이메일</TableHead>
          <TableHead>액션</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {users.map((user) => (
          <TableRow key={user.id}>
            <TableCell>{user.name}</TableCell>
            <TableCell>{user.email}</TableCell>
            <TableCell>
              <Button variant="ghost" size="sm">편집</Button>
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
}
```

### 모달/다이얼로그
```tsx
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';

export function CreateUserDialog() {
  const [open, setOpen] = useState(false);

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button>사용자 추가</Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>새 사용자</DialogTitle>
          <DialogDescription>
            새로운 사용자를 추가합니다.
          </DialogDescription>
        </DialogHeader>
        <UserForm onSuccess={() => setOpen(false)} />
      </DialogContent>
    </Dialog>
  );
}
```

### 토스트 알림
```tsx
import { useToast } from '@/components/ui/use-toast';

export function Example() {
  const { toast } = useToast();

  const handleSave = async () => {
    try {
      await saveData();
      toast({ title: '저장 완료', description: '성공적으로 저장되었습니다.' });
    } catch {
      toast({ title: '오류', description: '저장에 실패했습니다.', variant: 'destructive' });
    }
  };
}
```

## 레이아웃 패턴

### 대시보드 레이아웃
```tsx
export default function DashboardLayout({ children }) {
  return (
    <div className="flex min-h-screen">
      <aside className="w-64 border-r bg-muted/40">
        <Sidebar />
      </aside>
      <main className="flex-1 p-6">
        {children}
      </main>
    </div>
  );
}
```

### 반응형 그리드
```tsx
<div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
  <Card>...</Card>
  <Card>...</Card>
  <Card>...</Card>
  <Card>...</Card>
</div>
```
