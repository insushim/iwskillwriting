# Data Analysis Skill

> 데이터 분석 전문가 - Python, SQL, 시각화, 머신러닝

## Triggers
- "데이터", "분석", "데이터분석"
- "판다스", "Pandas", "넘파이", "NumPy"
- "시각화", "차트", "그래프"
- "SQL", "쿼리", "데이터베이스 분석"
- "통계", "상관관계", "회귀분석"

## Capabilities

### 1. 데이터 처리 (Pandas)

```python
import pandas as pd
import numpy as np

# 데이터 로드
df = pd.read_csv('data.csv')
df = pd.read_excel('data.xlsx')
df = pd.read_json('data.json')

# 기본 탐색
df.head()           # 상위 5개
df.info()           # 데이터 타입
df.describe()       # 기술 통계
df.shape            # (행, 열)
df.columns          # 컬럼 목록
df.isnull().sum()   # 결측치 확인

# 데이터 정제
df.dropna()                          # 결측치 제거
df.fillna(0)                         # 결측치 채우기
df.drop_duplicates()                 # 중복 제거
df['col'] = df['col'].astype(int)    # 타입 변환

# 필터링
df[df['age'] > 30]
df.query('age > 30 and city == "Seoul"')
df.loc[df['status'] == 'active']

# 집계
df.groupby('category').agg({
    'sales': 'sum',
    'quantity': 'mean',
    'customer_id': 'nunique'
})

# 피벗 테이블
pd.pivot_table(df,
    values='sales',
    index='region',
    columns='month',
    aggfunc='sum'
)

# 병합
pd.merge(df1, df2, on='id', how='left')
pd.concat([df1, df2], axis=0)
```

### 2. 데이터 시각화

#### Matplotlib
```python
import matplotlib.pyplot as plt

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 라인 차트
plt.figure(figsize=(10, 6))
plt.plot(df['date'], df['sales'], label='매출')
plt.xlabel('날짜')
plt.ylabel('매출')
plt.title('월별 매출 추이')
plt.legend()
plt.savefig('chart.png', dpi=300)
plt.show()

# 막대 차트
plt.bar(categories, values)

# 파이 차트
plt.pie(sizes, labels=labels, autopct='%1.1f%%')

# 서브플롯
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
axes[0, 0].plot(x, y1)
axes[0, 1].bar(x, y2)
```

#### Seaborn
```python
import seaborn as sns

# 히트맵 (상관관계)
plt.figure(figsize=(10, 8))
sns.heatmap(df.corr(), annot=True, cmap='coolwarm')

# 박스플롯
sns.boxplot(x='category', y='value', data=df)

# 산점도
sns.scatterplot(x='x', y='y', hue='category', data=df)

# 분포도
sns.histplot(df['value'], kde=True)

# 페어플롯
sns.pairplot(df, hue='target')
```

#### Plotly (인터랙티브)
```python
import plotly.express as px

# 인터랙티브 라인 차트
fig = px.line(df, x='date', y='sales', color='category',
              title='카테고리별 매출 추이')
fig.show()

# 인터랙티브 막대 차트
fig = px.bar(df, x='region', y='sales', color='product')

# 지도 시각화
fig = px.scatter_geo(df, lat='lat', lon='lon',
                     size='population', color='region')
```

### 3. SQL 분석

```sql
-- 기본 집계
SELECT
    category,
    COUNT(*) as count,
    SUM(amount) as total_amount,
    AVG(amount) as avg_amount
FROM orders
WHERE order_date >= '2024-01-01'
GROUP BY category
HAVING SUM(amount) > 10000
ORDER BY total_amount DESC;

-- 윈도우 함수
SELECT
    order_id,
    customer_id,
    amount,
    SUM(amount) OVER (PARTITION BY customer_id ORDER BY order_date) as cumulative_amount,
    ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date) as order_rank,
    LAG(amount) OVER (PARTITION BY customer_id ORDER BY order_date) as prev_amount
FROM orders;

-- CTE (Common Table Expression)
WITH monthly_sales AS (
    SELECT
        DATE_TRUNC('month', order_date) as month,
        SUM(amount) as sales
    FROM orders
    GROUP BY 1
)
SELECT
    month,
    sales,
    sales - LAG(sales) OVER (ORDER BY month) as mom_change,
    (sales - LAG(sales) OVER (ORDER BY month)) / LAG(sales) OVER (ORDER BY month) * 100 as mom_pct
FROM monthly_sales;

-- 코호트 분석
WITH cohort AS (
    SELECT
        customer_id,
        DATE_TRUNC('month', MIN(order_date)) as cohort_month
    FROM orders
    GROUP BY customer_id
),
retention AS (
    SELECT
        c.cohort_month,
        DATE_TRUNC('month', o.order_date) as order_month,
        COUNT(DISTINCT o.customer_id) as customers
    FROM orders o
    JOIN cohort c ON o.customer_id = c.customer_id
    GROUP BY 1, 2
)
SELECT
    cohort_month,
    order_month,
    customers,
    EXTRACT(MONTH FROM AGE(order_month, cohort_month)) as months_since_first
FROM retention
ORDER BY 1, 2;
```

### 4. 통계 분석

```python
from scipy import stats
import statsmodels.api as sm

# 기술 통계
df['sales'].describe()
df['sales'].mean()      # 평균
df['sales'].median()    # 중앙값
df['sales'].std()       # 표준편차
df['sales'].var()       # 분산

# 상관관계
df.corr()                           # 피어슨 상관계수
stats.spearmanr(x, y)              # 스피어만 상관계수

# t-검정
stats.ttest_ind(group1, group2)    # 독립 표본
stats.ttest_rel(before, after)     # 대응 표본

# 카이제곱 검정
stats.chi2_contingency(contingency_table)

# 회귀 분석
X = sm.add_constant(df[['feature1', 'feature2']])
y = df['target']
model = sm.OLS(y, X).fit()
print(model.summary())

# A/B 테스트
def ab_test(control, treatment, alpha=0.05):
    t_stat, p_value = stats.ttest_ind(control, treatment)
    significant = p_value < alpha
    return {
        't_statistic': t_stat,
        'p_value': p_value,
        'significant': significant,
        'control_mean': control.mean(),
        'treatment_mean': treatment.mean(),
        'lift': (treatment.mean() - control.mean()) / control.mean() * 100
    }
```

### 5. 분석 리포트 템플릿

```markdown
# [분석 주제] 분석 보고서

## 1. Executive Summary
- 핵심 발견 사항 1
- 핵심 발견 사항 2
- 권장 사항

## 2. 분석 목적
[분석을 수행한 이유와 목적]

## 3. 데이터 개요
- **데이터 출처:** [출처]
- **기간:** [시작일] ~ [종료일]
- **레코드 수:** [N건]
- **주요 변수:**
  | 변수명 | 설명 | 데이터 타입 |
  |--------|------|-------------|
  | col1   | ...  | int         |

## 4. 분석 방법
[사용한 분석 기법 설명]

## 5. 주요 발견

### 5.1 [발견 1]
[시각화 + 해석]

### 5.2 [발견 2]
[시각화 + 해석]

## 6. 결론 및 제언
1. [제언 1]
2. [제언 2]

## 7. 한계점 및 향후 분석 방향
[한계점과 추가 분석 필요 사항]

## 부록
- 분석 코드
- 상세 데이터
```

### 6. 자동화 파이프라인

```python
class DataAnalysisPipeline:
    def __init__(self, data_path):
        self.df = pd.read_csv(data_path)

    def clean_data(self):
        """데이터 정제"""
        self.df = self.df.dropna()
        self.df = self.df.drop_duplicates()
        return self

    def analyze(self):
        """분석 수행"""
        self.summary = self.df.describe()
        self.correlations = self.df.corr()
        return self

    def visualize(self, output_dir='charts'):
        """시각화 생성"""
        import os
        os.makedirs(output_dir, exist_ok=True)

        # 각종 차트 생성
        for col in self.df.select_dtypes(include=[np.number]).columns:
            plt.figure()
            self.df[col].hist(bins=30)
            plt.title(f'{col} Distribution')
            plt.savefig(f'{output_dir}/{col}_dist.png')
            plt.close()

        return self

    def generate_report(self, output_path='report.html'):
        """HTML 리포트 생성"""
        from jinja2 import Template

        template = Template("""
        <html>
        <head><title>분석 보고서</title></head>
        <body>
            <h1>데이터 분석 보고서</h1>
            <h2>기술 통계</h2>
            {{ summary }}
            <h2>상관관계</h2>
            {{ correlations }}
        </body>
        </html>
        """)

        html = template.render(
            summary=self.summary.to_html(),
            correlations=self.correlations.to_html()
        )

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)

        return self
```
