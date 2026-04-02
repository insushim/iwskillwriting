-- ============================================
-- 교육 SaaS Supabase 스키마 템플릿
-- Next.js 15 + Supabase + Stripe
-- ============================================

-- 확장 활성화
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- ============================================
-- 1. 사용자 프로필
-- ============================================
CREATE TYPE user_role AS ENUM ('student', 'teacher', 'parent', 'admin');

CREATE TABLE profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  role user_role NOT NULL DEFAULT 'student',
  display_name TEXT NOT NULL,
  avatar_url TEXT,
  grade INTEGER CHECK (grade BETWEEN 1 AND 6),  -- 1~6학년
  semester INTEGER CHECK (semester IN (1, 2)),
  school_name TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 프로필 자동 생성 트리거
CREATE OR REPLACE FUNCTION handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO profiles (id, role, display_name)
  VALUES (
    NEW.id,
    COALESCE(NEW.raw_user_meta_data->>'role', 'student')::user_role,
    COALESCE(NEW.raw_user_meta_data->>'display_name', '학습자')
  );
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION handle_new_user();

-- ============================================
-- 2. 교과/단원/문제 구조
-- ============================================
CREATE TABLE subjects (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name TEXT NOT NULL,                -- 예: 수학, 국어, 영어, 과학
  slug TEXT NOT NULL UNIQUE,
  icon TEXT,                         -- 이모지 또는 아이콘 이름
  color TEXT,                        -- 테마 색상
  sort_order INTEGER NOT NULL DEFAULT 0,
  is_active BOOLEAN NOT NULL DEFAULT true,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE units (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  subject_id UUID NOT NULL REFERENCES subjects(id) ON DELETE CASCADE,
  grade INTEGER NOT NULL CHECK (grade BETWEEN 1 AND 6),
  semester INTEGER NOT NULL CHECK (semester IN (1, 2)),
  chapter INTEGER NOT NULL,          -- 단원 번호
  name TEXT NOT NULL,                -- 단원명
  description TEXT,
  achievement_code TEXT,             -- 성취기준 코드 (예: 2수01-01)
  sort_order INTEGER NOT NULL DEFAULT 0,
  is_active BOOLEAN NOT NULL DEFAULT true,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TYPE difficulty_level AS ENUM ('easy', 'medium', 'hard', 'challenge');
CREATE TYPE problem_type AS ENUM ('multiple_choice', 'short_answer', 'fill_blank', 'true_false', 'ordering');

CREATE TABLE problems (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  unit_id UUID NOT NULL REFERENCES units(id) ON DELETE CASCADE,
  type problem_type NOT NULL DEFAULT 'multiple_choice',
  difficulty difficulty_level NOT NULL DEFAULT 'medium',
  question TEXT NOT NULL,            -- 문제 본문 (마크다운 지원)
  options JSONB,                     -- 객관식 선택지 [{"label":"A","text":"..."}]
  correct_answer TEXT NOT NULL,      -- 정답
  solution TEXT,                     -- 풀이 설명
  hint TEXT,                         -- 힌트
  image_url TEXT,                    -- 문제 이미지 (선택)
  tags TEXT[],                       -- 태그 (예: ['덧셈', '받아올림'])
  time_limit INTEGER DEFAULT 60,    -- 제한 시간 (초)
  xp_reward INTEGER NOT NULL DEFAULT 10,
  created_by UUID REFERENCES profiles(id),
  is_active BOOLEAN NOT NULL DEFAULT true,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ============================================
-- 3. 학습 기록
-- ============================================
CREATE TABLE learning_sessions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  student_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  unit_id UUID NOT NULL REFERENCES units(id) ON DELETE CASCADE,
  total_problems INTEGER NOT NULL DEFAULT 10,
  correct_count INTEGER NOT NULL DEFAULT 0,
  wrong_count INTEGER NOT NULL DEFAULT 0,
  xp_earned INTEGER NOT NULL DEFAULT 0,
  coins_earned INTEGER NOT NULL DEFAULT 0,
  duration_seconds INTEGER,          -- 소요 시간
  completed_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE submissions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  session_id UUID NOT NULL REFERENCES learning_sessions(id) ON DELETE CASCADE,
  student_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  problem_id UUID NOT NULL REFERENCES problems(id) ON DELETE CASCADE,
  answer TEXT NOT NULL,              -- 학생 답안
  is_correct BOOLEAN NOT NULL,
  attempt_count INTEGER NOT NULL DEFAULT 1,  -- 시도 횟수
  time_taken INTEGER,                -- 소요 시간 (초)
  xp_earned INTEGER NOT NULL DEFAULT 0,
  hint_used BOOLEAN NOT NULL DEFAULT false,
  solution_viewed BOOLEAN NOT NULL DEFAULT false,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 오답 노트
CREATE TABLE mistake_notes (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  student_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  problem_id UUID NOT NULL REFERENCES problems(id) ON DELETE CASCADE,
  submission_id UUID NOT NULL REFERENCES submissions(id) ON DELETE CASCADE,
  wrong_answer TEXT NOT NULL,
  review_count INTEGER NOT NULL DEFAULT 0,
  mastered BOOLEAN NOT NULL DEFAULT false,
  last_reviewed_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ============================================
-- 4. 게이미피케이션
-- ============================================
CREATE TABLE student_stats (
  student_id UUID PRIMARY KEY REFERENCES profiles(id) ON DELETE CASCADE,
  total_xp INTEGER NOT NULL DEFAULT 0,
  level INTEGER NOT NULL DEFAULT 1,
  coins INTEGER NOT NULL DEFAULT 0,
  current_streak INTEGER NOT NULL DEFAULT 0,
  longest_streak INTEGER NOT NULL DEFAULT 0,
  total_problems_solved INTEGER NOT NULL DEFAULT 0,
  total_correct INTEGER NOT NULL DEFAULT 0,
  consecutive_correct INTEGER NOT NULL DEFAULT 0,
  last_active_date DATE,
  streak_freeze_count INTEGER NOT NULL DEFAULT 2,  -- 남은 프리즈 횟수
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE badges (
  id TEXT PRIMARY KEY,               -- 예: 'first_solve', 'streak_7'
  name TEXT NOT NULL,
  description TEXT NOT NULL,
  icon TEXT NOT NULL,                -- 이모지
  category TEXT NOT NULL,            -- 'milestone', 'streak', 'accuracy', 'speed', 'social', 'secret'
  condition JSONB NOT NULL,          -- 달성 조건 JSON
  xp_reward INTEGER NOT NULL DEFAULT 0,
  coin_reward INTEGER NOT NULL DEFAULT 0,
  sort_order INTEGER NOT NULL DEFAULT 0,
  is_active BOOLEAN NOT NULL DEFAULT true
);

CREATE TABLE student_badges (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  student_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  badge_id TEXT NOT NULL REFERENCES badges(id) ON DELETE CASCADE,
  earned_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(student_id, badge_id)
);

CREATE TABLE shop_items (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT,
  category TEXT NOT NULL,            -- 'avatar', 'theme', 'effect', 'utility'
  price INTEGER NOT NULL,            -- 코인 가격
  image_url TEXT,
  metadata JSONB,                    -- 추가 데이터
  is_active BOOLEAN NOT NULL DEFAULT true,
  sort_order INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE student_purchases (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  student_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  item_id TEXT NOT NULL REFERENCES shop_items(id) ON DELETE CASCADE,
  purchased_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(student_id, item_id)
);

CREATE TABLE student_equipped (
  student_id UUID PRIMARY KEY REFERENCES profiles(id) ON DELETE CASCADE,
  avatar_id TEXT REFERENCES shop_items(id),
  theme_id TEXT REFERENCES shop_items(id),
  effect_id TEXT REFERENCES shop_items(id)
);

-- 랭킹 (매터리얼라이즈드 뷰로 성능 최적화)
CREATE MATERIALIZED VIEW ranking_weekly AS
SELECT
  s.student_id,
  p.display_name,
  p.grade,
  p.school_name,
  s.total_xp,
  s.level,
  s.current_streak,
  RANK() OVER (ORDER BY s.total_xp DESC) as rank
FROM student_stats s
JOIN profiles p ON p.id = s.student_id
WHERE p.role = 'student';

-- ============================================
-- 5. 반/교사/학부모 관계
-- ============================================
CREATE TABLE classes (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  teacher_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  name TEXT NOT NULL,                -- 반 이름 (예: 3학년 2반)
  grade INTEGER NOT NULL CHECK (grade BETWEEN 1 AND 6),
  school_name TEXT,
  invite_code TEXT UNIQUE,           -- 초대 코드
  is_active BOOLEAN NOT NULL DEFAULT true,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE class_students (
  class_id UUID NOT NULL REFERENCES classes(id) ON DELETE CASCADE,
  student_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  joined_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  PRIMARY KEY (class_id, student_id)
);

CREATE TABLE parent_children (
  parent_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  child_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  PRIMARY KEY (parent_id, child_id)
);

-- 과제
CREATE TABLE assignments (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  class_id UUID NOT NULL REFERENCES classes(id) ON DELETE CASCADE,
  teacher_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  unit_id UUID NOT NULL REFERENCES units(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  description TEXT,
  problem_count INTEGER NOT NULL DEFAULT 10,
  difficulty difficulty_level DEFAULT 'medium',
  due_date TIMESTAMPTZ,
  is_active BOOLEAN NOT NULL DEFAULT true,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE assignment_submissions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  assignment_id UUID NOT NULL REFERENCES assignments(id) ON DELETE CASCADE,
  student_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  session_id UUID REFERENCES learning_sessions(id),
  status TEXT NOT NULL DEFAULT 'pending', -- 'pending', 'in_progress', 'completed'
  submitted_at TIMESTAMPTZ,
  UNIQUE(assignment_id, student_id)
);

-- ============================================
-- 6. 결제 (Stripe)
-- ============================================
CREATE TABLE subscriptions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  stripe_customer_id TEXT,
  stripe_subscription_id TEXT UNIQUE,
  plan_id TEXT NOT NULL,             -- 'free', 'premium', 'family', 'school'
  status TEXT NOT NULL DEFAULT 'active',  -- 'active', 'canceled', 'past_due'
  current_period_start TIMESTAMPTZ,
  current_period_end TIMESTAMPTZ,
  cancel_at_period_end BOOLEAN NOT NULL DEFAULT false,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ============================================
-- 7. RLS (Row Level Security) 정책
-- ============================================

-- 프로필: 본인만 수정, 모두 조회
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
CREATE POLICY "profiles_select" ON profiles FOR SELECT USING (true);
CREATE POLICY "profiles_update" ON profiles FOR UPDATE USING (auth.uid() = id);

-- 학습 세션: 본인만 접근
ALTER TABLE learning_sessions ENABLE ROW LEVEL SECURITY;
CREATE POLICY "sessions_student" ON learning_sessions FOR ALL
  USING (auth.uid() = student_id);

-- 풀이 기록: 본인만 접근
ALTER TABLE submissions ENABLE ROW LEVEL SECURITY;
CREATE POLICY "submissions_student" ON submissions FOR ALL
  USING (auth.uid() = student_id);

-- 오답 노트: 본인만 접근
ALTER TABLE mistake_notes ENABLE ROW LEVEL SECURITY;
CREATE POLICY "mistakes_student" ON mistake_notes FOR ALL
  USING (auth.uid() = student_id);

-- 학생 통계: 본인, 교사(같은 반), 학부모(연결된 자녀)
ALTER TABLE student_stats ENABLE ROW LEVEL SECURITY;
CREATE POLICY "stats_self" ON student_stats FOR SELECT
  USING (auth.uid() = student_id);
CREATE POLICY "stats_teacher" ON student_stats FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM class_students cs
      JOIN classes c ON c.id = cs.class_id
      WHERE cs.student_id = student_stats.student_id
      AND c.teacher_id = auth.uid()
    )
  );
CREATE POLICY "stats_parent" ON student_stats FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM parent_children pc
      WHERE pc.child_id = student_stats.student_id
      AND pc.parent_id = auth.uid()
    )
  );
CREATE POLICY "stats_update" ON student_stats FOR UPDATE
  USING (auth.uid() = student_id);

-- 문제: 모두 조회, 교사/관리자만 수정
ALTER TABLE problems ENABLE ROW LEVEL SECURITY;
CREATE POLICY "problems_select" ON problems FOR SELECT USING (is_active = true);
CREATE POLICY "problems_manage" ON problems FOR ALL
  USING (
    EXISTS (
      SELECT 1 FROM profiles
      WHERE id = auth.uid() AND role IN ('teacher', 'admin')
    )
  );

-- 반: 교사만 관리
ALTER TABLE classes ENABLE ROW LEVEL SECURITY;
CREATE POLICY "classes_teacher" ON classes FOR ALL
  USING (auth.uid() = teacher_id);
CREATE POLICY "classes_student" ON classes FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM class_students
      WHERE class_id = classes.id AND student_id = auth.uid()
    )
  );

-- 교과/단원: 모두 조회
ALTER TABLE subjects ENABLE ROW LEVEL SECURITY;
CREATE POLICY "subjects_select" ON subjects FOR SELECT USING (is_active = true);

ALTER TABLE units ENABLE ROW LEVEL SECURITY;
CREATE POLICY "units_select" ON units FOR SELECT USING (is_active = true);

-- 뱃지: 모두 조회
ALTER TABLE badges ENABLE ROW LEVEL SECURITY;
CREATE POLICY "badges_select" ON badges FOR SELECT USING (is_active = true);

ALTER TABLE student_badges ENABLE ROW LEVEL SECURITY;
CREATE POLICY "student_badges_self" ON student_badges FOR SELECT
  USING (auth.uid() = student_id);
CREATE POLICY "student_badges_insert" ON student_badges FOR INSERT
  WITH CHECK (auth.uid() = student_id);

-- 상점: 모두 조회, 본인만 구매
ALTER TABLE shop_items ENABLE ROW LEVEL SECURITY;
CREATE POLICY "shop_select" ON shop_items FOR SELECT USING (is_active = true);

ALTER TABLE student_purchases ENABLE ROW LEVEL SECURITY;
CREATE POLICY "purchases_self" ON student_purchases FOR ALL
  USING (auth.uid() = student_id);

-- 구독: 본인만 접근
ALTER TABLE subscriptions ENABLE ROW LEVEL SECURITY;
CREATE POLICY "subscriptions_self" ON subscriptions FOR ALL
  USING (auth.uid() = user_id);

-- ============================================
-- 8. 인덱스
-- ============================================
CREATE INDEX idx_problems_unit ON problems(unit_id) WHERE is_active = true;
CREATE INDEX idx_problems_difficulty ON problems(unit_id, difficulty) WHERE is_active = true;
CREATE INDEX idx_submissions_student ON submissions(student_id, created_at DESC);
CREATE INDEX idx_submissions_session ON submissions(session_id);
CREATE INDEX idx_sessions_student ON learning_sessions(student_id, created_at DESC);
CREATE INDEX idx_class_students_student ON class_students(student_id);
CREATE INDEX idx_parent_children_parent ON parent_children(parent_id);
CREATE INDEX idx_mistake_notes_student ON mistake_notes(student_id) WHERE mastered = false;
CREATE INDEX idx_units_grade ON units(subject_id, grade, semester) WHERE is_active = true;

-- ============================================
-- 9. 함수
-- ============================================

-- 스트릭 업데이트 함수
CREATE OR REPLACE FUNCTION update_streak(p_student_id UUID)
RETURNS void AS $$
DECLARE
  v_last_date DATE;
  v_today DATE := CURRENT_DATE;
BEGIN
  SELECT last_active_date INTO v_last_date
  FROM student_stats WHERE student_id = p_student_id;

  IF v_last_date IS NULL OR v_last_date < v_today - INTERVAL '1 day' THEN
    -- 스트릭 리셋 (프리즈 확인)
    IF v_last_date = v_today - INTERVAL '1 day' THEN
      UPDATE student_stats SET
        current_streak = current_streak + 1,
        longest_streak = GREATEST(longest_streak, current_streak + 1),
        last_active_date = v_today,
        updated_at = NOW()
      WHERE student_id = p_student_id;
    ELSE
      UPDATE student_stats SET
        current_streak = 1,
        last_active_date = v_today,
        updated_at = NOW()
      WHERE student_id = p_student_id;
    END IF;
  END IF;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- XP 추가 및 레벨업 체크
CREATE OR REPLACE FUNCTION add_xp(p_student_id UUID, p_xp INTEGER, p_coins INTEGER DEFAULT 0)
RETURNS JSONB AS $$
DECLARE
  v_stats student_stats%ROWTYPE;
  v_new_xp INTEGER;
  v_new_level INTEGER;
  v_required_xp INTEGER;
  v_leveled_up BOOLEAN := false;
BEGIN
  SELECT * INTO v_stats FROM student_stats WHERE student_id = p_student_id;

  v_new_xp := v_stats.total_xp + p_xp;
  v_new_level := v_stats.level;

  -- 레벨업 체크
  LOOP
    v_required_xp := FLOOR(100 * POWER(1.15, v_new_level - 1));
    EXIT WHEN v_new_xp < (SELECT SUM(FLOOR(100 * POWER(1.15, s - 1))) FROM generate_series(1, v_new_level) AS s);
    v_new_level := v_new_level + 1;
    v_leveled_up := true;
  END LOOP;

  UPDATE student_stats SET
    total_xp = v_new_xp,
    level = v_new_level,
    coins = coins + p_coins,
    updated_at = NOW()
  WHERE student_id = p_student_id;

  RETURN jsonb_build_object(
    'xp_added', p_xp,
    'total_xp', v_new_xp,
    'new_level', v_new_level,
    'leveled_up', v_leveled_up,
    'coins_added', p_coins
  );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- 랭킹 뷰 새로고침 (cron으로 5분마다)
-- SELECT cron.schedule('refresh_ranking', '*/5 * * * *', 'REFRESH MATERIALIZED VIEW CONCURRENTLY ranking_weekly');

-- ============================================
-- 10. 적응형 학습 (v2 추가)
-- ============================================

-- SM-2 간격반복 파라미터
CREATE TABLE student_problem_sm2 (
  student_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  problem_id UUID NOT NULL REFERENCES problems(id) ON DELETE CASCADE,
  ease_factor REAL NOT NULL DEFAULT 2.5,
  interval_days INTEGER NOT NULL DEFAULT 0,
  repetitions INTEGER NOT NULL DEFAULT 0,
  next_review_date DATE NOT NULL DEFAULT CURRENT_DATE,
  last_quality INTEGER CHECK (last_quality BETWEEN 0 AND 5),
  total_reviews INTEGER NOT NULL DEFAULT 0,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  PRIMARY KEY (student_id, problem_id)
);

-- 학생 능력치 (적응형 난이도)
CREATE TABLE student_ability (
  student_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  unit_id UUID NOT NULL REFERENCES units(id) ON DELETE CASCADE,
  theta REAL NOT NULL DEFAULT 0,              -- 능력치 (-3 ~ +3)
  mastery_level REAL NOT NULL DEFAULT 0,       -- 마스터리 (0~1)
  current_difficulty INTEGER NOT NULL DEFAULT 2, -- 1=easy, 4=challenge
  consecutive_correct INTEGER NOT NULL DEFAULT 0,
  consecutive_wrong INTEGER NOT NULL DEFAULT 0,
  total_attempts INTEGER NOT NULL DEFAULT 0,
  correct_attempts INTEGER NOT NULL DEFAULT 0,
  weak_tags TEXT[],                             -- 취약 태그
  status TEXT NOT NULL DEFAULT 'not_started',   -- not_started, in_progress, mastered, needs_review
  mastered_at TIMESTAMPTZ,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  PRIMARY KEY (student_id, unit_id)
);

-- SM-2 인덱스
CREATE INDEX idx_sm2_review_due ON student_problem_sm2(student_id, next_review_date)
  WHERE next_review_date <= CURRENT_DATE;
CREATE INDEX idx_ability_student ON student_ability(student_id, status);

-- SM-2 RLS
ALTER TABLE student_problem_sm2 ENABLE ROW LEVEL SECURITY;
CREATE POLICY "sm2_self" ON student_problem_sm2 FOR ALL USING (auth.uid() = student_id);

ALTER TABLE student_ability ENABLE ROW LEVEL SECURITY;
CREATE POLICY "ability_self" ON student_ability FOR ALL USING (auth.uid() = student_id);
CREATE POLICY "ability_teacher" ON student_ability FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM class_students cs
      JOIN classes c ON c.id = cs.class_id
      WHERE cs.student_id = student_ability.student_id
      AND c.teacher_id = auth.uid()
    )
  );

-- ============================================
-- 11. 멀티테넌시 — 조직/학교 (v2 추가)
-- ============================================

CREATE TYPE org_type AS ENUM ('school', 'academy', 'individual', 'enterprise');

CREATE TABLE organizations (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name TEXT NOT NULL,
  slug TEXT NOT NULL UNIQUE,
  type org_type NOT NULL DEFAULT 'school',
  logo_url TEXT,
  settings JSONB DEFAULT '{}'::jsonb,    -- 커스텀 로고, 색상, 기능 on/off
  stripe_customer_id TEXT,
  plan_id TEXT NOT NULL DEFAULT 'free',
  is_active BOOLEAN NOT NULL DEFAULT true,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TYPE org_role AS ENUM ('owner', 'admin', 'teacher', 'student', 'parent');

CREATE TABLE organization_members (
  org_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  role org_role NOT NULL DEFAULT 'student',
  joined_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  PRIMARY KEY (org_id, user_id)
);

-- 반에 조직 연결
ALTER TABLE classes ADD COLUMN org_id UUID REFERENCES organizations(id) ON DELETE SET NULL;
CREATE INDEX idx_classes_org ON classes(org_id) WHERE org_id IS NOT NULL;

-- 조직 RLS
ALTER TABLE organizations ENABLE ROW LEVEL SECURITY;
CREATE POLICY "org_members" ON organizations FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM organization_members
      WHERE org_id = organizations.id AND user_id = auth.uid()
    )
  );

ALTER TABLE organization_members ENABLE ROW LEVEL SECURITY;
CREATE POLICY "org_members_self" ON organization_members FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM organization_members om
      WHERE om.org_id = organization_members.org_id AND om.user_id = auth.uid()
    )
  );

-- ============================================
-- 12. 알림 시스템 (v2 추가)
-- ============================================

CREATE TABLE push_subscriptions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  endpoint TEXT NOT NULL,
  p256dh TEXT NOT NULL,
  auth_key TEXT NOT NULL,
  device_info JSONB,
  is_active BOOLEAN NOT NULL DEFAULT true,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE notification_preferences (
  user_id UUID PRIMARY KEY REFERENCES profiles(id) ON DELETE CASCADE,
  streak_reminder BOOLEAN NOT NULL DEFAULT true,
  achievement_alerts BOOLEAN NOT NULL DEFAULT true,
  social_notifications BOOLEAN NOT NULL DEFAULT true,
  weekly_report BOOLEAN NOT NULL DEFAULT true,
  quiet_start TIME DEFAULT '21:00',
  quiet_end TIME DEFAULT '07:00',
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE notification_history (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  type TEXT NOT NULL,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  data JSONB,
  sent_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  opened_at TIMESTAMPTZ,
  clicked BOOLEAN NOT NULL DEFAULT false
);

CREATE INDEX idx_notifications_user ON notification_history(user_id, sent_at DESC);
CREATE INDEX idx_push_subs_user ON push_subscriptions(user_id) WHERE is_active = true;

ALTER TABLE push_subscriptions ENABLE ROW LEVEL SECURITY;
CREATE POLICY "push_self" ON push_subscriptions FOR ALL USING (auth.uid() = user_id);

ALTER TABLE notification_preferences ENABLE ROW LEVEL SECURITY;
CREATE POLICY "prefs_self" ON notification_preferences FOR ALL USING (auth.uid() = user_id);

ALTER TABLE notification_history ENABLE ROW LEVEL SECURITY;
CREATE POLICY "history_self" ON notification_history FOR SELECT USING (auth.uid() = user_id);

-- ============================================
-- 13. 실시간 퀴즈 (v2 추가)
-- ============================================

CREATE TABLE live_quizzes (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  host_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  class_id UUID NOT NULL REFERENCES classes(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'waiting',  -- waiting, active, finished
  current_problem_index INTEGER NOT NULL DEFAULT 0,
  problem_ids UUID[] NOT NULL,
  settings JSONB DEFAULT '{"timePerQuestion": 30, "showLeaderboard": true}'::jsonb,
  started_at TIMESTAMPTZ,
  finished_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE live_quiz_participants (
  quiz_id UUID NOT NULL REFERENCES live_quizzes(id) ON DELETE CASCADE,
  student_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  score INTEGER NOT NULL DEFAULT 0,
  correct_count INTEGER NOT NULL DEFAULT 0,
  answers JSONB DEFAULT '[]'::jsonb,
  joined_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  PRIMARY KEY (quiz_id, student_id)
);

ALTER TABLE live_quizzes ENABLE ROW LEVEL SECURITY;
CREATE POLICY "quiz_host" ON live_quizzes FOR ALL USING (auth.uid() = host_id);
CREATE POLICY "quiz_student" ON live_quizzes FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM class_students cs
      WHERE cs.class_id = live_quizzes.class_id AND cs.student_id = auth.uid()
    )
  );

ALTER TABLE live_quiz_participants ENABLE ROW LEVEL SECURITY;
CREATE POLICY "quiz_part_self" ON live_quiz_participants FOR ALL USING (auth.uid() = student_id);
CREATE POLICY "quiz_part_host" ON live_quiz_participants FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM live_quizzes lq
      WHERE lq.id = live_quiz_participants.quiz_id AND lq.host_id = auth.uid()
    )
  );

-- ============================================
-- 14. AI 튜터 대화 이력 (v2 추가)
-- ============================================

CREATE TABLE ai_conversations (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  student_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  context_type TEXT NOT NULL,    -- 'tutor', 'hint', 'explain'
  context_id UUID,               -- problem_id 또는 unit_id
  messages JSONB NOT NULL DEFAULT '[]'::jsonb,
  token_count INTEGER NOT NULL DEFAULT 0,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_ai_conv_student ON ai_conversations(student_id, created_at DESC);

ALTER TABLE ai_conversations ENABLE ROW LEVEL SECURITY;
CREATE POLICY "ai_conv_self" ON ai_conversations FOR ALL USING (auth.uid() = student_id);
