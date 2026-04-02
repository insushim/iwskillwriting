# 시드 데이터 가이드

> 초기 데이터 구조 및 샘플 문제

## 교과 시드

```sql
INSERT INTO subjects (name, slug, icon, color, sort_order) VALUES
  ('수학', 'math', '🔢', '#3B82F6', 1),
  ('국어', 'korean', '📖', '#10B981', 2),
  ('영어', 'english', '🌍', '#F59E0B', 3),
  ('과학', 'science', '🔬', '#8B5CF6', 4);
```

## 단원 시드 (수학 1학년 예시)

```sql
-- 1학년 1학기
INSERT INTO units (subject_id, grade, semester, chapter, name, achievement_code, sort_order)
SELECT s.id, 1, 1, chapter, name, code, chapter
FROM subjects s,
(VALUES
  (1, '9까지의 수', '2수01-01'),
  (2, '여러 가지 모양', '2도01-01'),
  (3, '덧셈과 뺄셈', '2수01-02'),
  (4, '비교하기', '2측01-01'),
  (5, '50까지의 수', '2수01-03')
) AS data(chapter, name, code)
WHERE s.slug = 'math';

-- 1학년 2학기
INSERT INTO units (subject_id, grade, semester, chapter, name, achievement_code, sort_order)
SELECT s.id, 1, 2, chapter, name, code, chapter
FROM subjects s,
(VALUES
  (1, '100까지의 수', '2수01-04'),
  (2, '덧셈과 뺄셈(1)', '2수01-05'),
  (3, '여러 가지 모양', '2도01-02'),
  (4, '덧셈과 뺄셈(2)', '2수01-06'),
  (5, '시계 보기와 규칙 찾기', '2측01-02')
) AS data(chapter, name, code)
WHERE s.slug = 'math';
```

## 샘플 문제 (수학 1학년)

```sql
-- 9까지의 수 (easy)
INSERT INTO problems (unit_id, type, difficulty, question, options, correct_answer, solution, hint, xp_reward)
SELECT u.id,
  'multiple_choice', 'easy',
  '사과가 3개 있고, 2개를 더 받았습니다. 모두 몇 개일까요?',
  '[{"label":"A","text":"4개"},{"label":"B","text":"5개"},{"label":"C","text":"6개"},{"label":"D","text":"7개"}]'::jsonb,
  'B',
  '3 + 2 = 5이므로 사과는 모두 5개입니다.',
  '3에서 2만큼 더 세어보세요: 4, 5!',
  10
FROM units u WHERE u.name = '9까지의 수' AND u.grade = 1 AND u.semester = 1;

-- 9까지의 수 (medium)
INSERT INTO problems (unit_id, type, difficulty, question, options, correct_answer, solution, hint, xp_reward)
SELECT u.id,
  'short_answer', 'medium',
  '빈칸에 알맞은 수를 써넣으세요: 2 + ☐ = 7',
  NULL,
  '5',
  '7에서 2를 빼면 5입니다. 2 + 5 = 7',
  '7이 되려면 2에서 얼마를 더해야 할까요?',
  20
FROM units u WHERE u.name = '9까지의 수' AND u.grade = 1 AND u.semester = 1;

-- 덧셈과 뺄셈 (hard)
INSERT INTO problems (unit_id, type, difficulty, question, options, correct_answer, solution, hint, xp_reward)
SELECT u.id,
  'short_answer', 'hard',
  '☐ + 4 = 9, ☐에 들어갈 수는?',
  NULL,
  '5',
  '9 - 4 = 5이므로 ☐ = 5입니다.',
  '9에서 4를 빼보세요.',
  30
FROM units u WHERE u.name = '덧셈과 뺄셈' AND u.grade = 1 AND u.semester = 1;
```

## 뱃지 시드

```sql
INSERT INTO badges (id, name, description, icon, category, condition, xp_reward, coin_reward, sort_order) VALUES
  ('first_solve', '첫 발걸음', '첫 문제를 풀었어요!', '👣', 'milestone', '{"total_solved": 1}'::jsonb, 10, 5, 1),
  ('solver_10', '열 번째 도전', '10문제 풀기', '🎯', 'milestone', '{"total_solved": 10}'::jsonb, 30, 10, 2),
  ('solver_50', '반백 용사', '50문제 풀기', '⚡', 'milestone', '{"total_solved": 50}'::jsonb, 100, 30, 3),
  ('solver_100', '백전불태', '100문제 풀기', '💯', 'milestone', '{"total_solved": 100}'::jsonb, 200, 50, 4),
  ('solver_500', '오백 전사', '500문제 풀기', '🏆', 'milestone', '{"total_solved": 500}'::jsonb, 500, 100, 5),
  ('solver_1000', '천 문제 달인', '1000문제 풀기', '👑', 'milestone', '{"total_solved": 1000}'::jsonb, 1000, 200, 6),
  ('streak_3', '3일 연속', '3일 연속 학습', '🔥', 'streak', '{"streak": 3}'::jsonb, 30, 10, 10),
  ('streak_7', '일주일 전사', '7일 연속 학습', '🔥', 'streak', '{"streak": 7}'::jsonb, 100, 30, 11),
  ('streak_14', '2주 마라톤', '14일 연속 학습', '🌟', 'streak', '{"streak": 14}'::jsonb, 250, 70, 12),
  ('streak_30', '한 달 챔피언', '30일 연속 학습', '💎', 'streak', '{"streak": 30}'::jsonb, 500, 200, 13),
  ('streak_100', '100일 전설', '100일 연속 학습', '🏅', 'streak', '{"streak": 100}'::jsonb, 2000, 1000, 14),
  ('perfect_10', '완벽한 10문제', '10문제 연속 정답', '✨', 'accuracy', '{"consecutive_correct": 10}'::jsonb, 100, 30, 20),
  ('perfect_day', '완벽한 하루', '하루 문제 전부 정답', '🌞', 'accuracy', '{"daily_accuracy": 100}'::jsonb, 50, 20, 21),
  ('accuracy_90', '명사수', '전체 정답률 90%+', '🎯', 'accuracy', '{"overall_accuracy": 90}'::jsonb, 200, 50, 22),
  ('speed_demon', '번개 계산기', '10초 내 정답 5연속', '⚡', 'speed', '{"fast_correct": 5}'::jsonb, 150, 40, 30),
  ('chapter_clear', '단원 정복자', '한 단원 100% 완료', '📚', 'milestone', '{"chapters_completed": 1}'::jsonb, 300, 100, 40),
  ('grade_clear', '학년 마스터', '한 학년 전체 완료', '🎓', 'milestone', '{"grades_completed": 1}'::jsonb, 1000, 500, 41),
  ('midnight', '밤의 학자', '자정에 문제 풀기', '🦉', 'secret', '{"solved_at_midnight": true}'::jsonb, 50, 20, 50),
  ('early_bird', '아침형 학생', '오전 6시 전 학습', '🐦', 'secret', '{"solved_before_6am": true}'::jsonb, 50, 20, 51),
  ('weekend_warrior', '주말 전사', '토요일+일요일 연속 학습', '🏋️', 'secret', '{"weekend_streak": true}'::jsonb, 50, 20, 52);
```

## 상점 아이템 시드

```sql
INSERT INTO shop_items (id, name, description, category, price, sort_order) VALUES
  ('avatar_default', '기본 아바타', '기본 프로필 이미지', 'avatar', 0, 1),
  ('avatar_ninja', '닌자 아바타', '멋진 닌자!', 'avatar', 100, 2),
  ('avatar_wizard', '마법사 아바타', '지혜로운 마법사', 'avatar', 100, 3),
  ('avatar_astronaut', '우주비행사 아바타', '우주를 탐험해요', 'avatar', 200, 4),
  ('avatar_robot', '로봇 아바타', '똑똑한 로봇', 'avatar', 200, 5),
  ('avatar_dragon', '드래곤 아바타', '전설의 드래곤', 'avatar', 500, 6),
  ('theme_light', '라이트 모드', '밝은 기본 테마', 'theme', 0, 10),
  ('theme_dark', '다크 모드', '눈이 편한 어두운 테마', 'theme', 50, 11),
  ('theme_ocean', '바다 테마', '시원한 바다 느낌', 'theme', 150, 12),
  ('theme_forest', '숲 테마', '자연 속 학습', 'theme', 150, 13),
  ('theme_space', '우주 테마', '우주 공간에서 학습', 'theme', 200, 14),
  ('theme_candy', '캔디 테마', '달콤한 사탕 나라', 'theme', 200, 15),
  ('effect_confetti', '폭죽 효과', '정답 시 폭죽이 터져요', 'effect', 100, 20),
  ('effect_fireworks', '불꽃놀이', '레벨업 시 불꽃놀이', 'effect', 150, 21),
  ('effect_sparkle', '반짝이 효과', '뱃지 획득 시 반짝반짝', 'effect', 100, 22),
  ('streak_freeze', '스트릭 프리즈', '하루 쉬어도 스트릭 유지 (1회)', 'utility', 50, 30),
  ('hint_token_3', '힌트 토큰 3개', '문제 힌트를 볼 수 있어요', 'utility', 30, 31),
  ('double_xp_1h', '2배 XP (1시간)', '1시간 동안 XP 2배!', 'utility', 100, 32);
```

## 문제 생성 가이드 (교과별)

### 수학 문제 자동 생성 패턴

```typescript
// 덧셈 문제 생성기 (1학년)
function generateAddition(grade: number): Problem {
  const maxNum = grade <= 2 ? 20 : grade <= 4 ? 1000 : 10000;
  const a = Math.floor(Math.random() * maxNum);
  const b = Math.floor(Math.random() * (maxNum - a));
  const answer = a + b;

  return {
    question: `${a} + ${b} = ?`,
    correct_answer: String(answer),
    difficulty: a + b < maxNum / 3 ? 'easy' : a + b < maxNum * 2 / 3 ? 'medium' : 'hard',
    type: 'short_answer',
  };
}

// 곱셈구구 문제 생성기 (2학년)
function generateMultiplication(): Problem {
  const a = Math.floor(Math.random() * 9) + 1;
  const b = Math.floor(Math.random() * 9) + 1;

  return {
    question: `${a} × ${b} = ?`,
    correct_answer: String(a * b),
    difficulty: (a <= 5 && b <= 5) ? 'easy' : 'medium',
    type: 'short_answer',
  };
}

// 분수 문제 생성기 (3~4학년)
function generateFraction(type: 'add' | 'subtract'): Problem {
  const denom = [2, 3, 4, 5, 6, 8, 10][Math.floor(Math.random() * 7)];
  const num1 = Math.floor(Math.random() * (denom - 1)) + 1;
  const num2 = type === 'add'
    ? Math.floor(Math.random() * (denom - num1)) + 1
    : Math.floor(Math.random() * num1) + 1;

  const answer = type === 'add' ? num1 + num2 : num1 - num2;

  return {
    question: `${num1}/${denom} ${type === 'add' ? '+' : '-'} ${num2}/${denom} = ?`,
    correct_answer: `${answer}/${denom}`,
    difficulty: 'medium',
    type: 'short_answer',
  };
}
```
