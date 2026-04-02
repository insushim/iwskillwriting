---
description: 데이터 분석 및 시각화. "데이터", "분석", "판다스", "Pandas", "통계", "차트", "시각화" 트리거.
---

# 데이터 분석 및 시각화

## 환경 설정
```bash
pip install pandas numpy matplotlib seaborn plotly scikit-learn jupyter
```

## Pandas 기본 작업

### 데이터 로딩
```python
import pandas as pd
import numpy as np

# CSV 로드
df = pd.read_csv('data.csv')

# Excel 로드
df = pd.read_excel('data.xlsx', sheet_name='Sheet1')

# JSON 로드
df = pd.read_json('data.json')

# SQL 쿼리
from sqlalchemy import create_engine
engine = create_engine('postgresql://user:pass@host/db')
df = pd.read_sql('SELECT * FROM table', engine)
```

### 데이터 탐색
```python
# 기본 정보
df.info()
df.describe()
df.head(10)
df.shape

# 컬럼별 분석
df['column'].value_counts()
df['column'].unique()
df['column'].nunique()

# 결측치 확인
df.isnull().sum()
df.isnull().sum() / len(df) * 100  # 비율

# 데이터 타입
df.dtypes
```

### 데이터 정제
```python
# 결측치 처리
df.dropna()                          # 결측치 행 삭제
df.fillna(0)                         # 0으로 채우기
df.fillna(df.mean())                 # 평균으로 채우기
df.fillna(method='ffill')            # 앞의 값으로 채우기

# 중복 제거
df.drop_duplicates()
df.drop_duplicates(subset=['col1', 'col2'])

# 타입 변환
df['date'] = pd.to_datetime(df['date'])
df['price'] = df['price'].astype(float)

# 이상치 제거 (IQR)
Q1 = df['column'].quantile(0.25)
Q3 = df['column'].quantile(0.75)
IQR = Q3 - Q1
df = df[(df['column'] >= Q1 - 1.5*IQR) & (df['column'] <= Q3 + 1.5*IQR)]
```

### 데이터 변환
```python
# 필터링
df[df['age'] > 30]
df[(df['age'] > 30) & (df['city'] == 'Seoul')]
df.query('age > 30 and city == "Seoul"')

# 정렬
df.sort_values('date', ascending=False)
df.sort_values(['col1', 'col2'], ascending=[True, False])

# 그룹화
df.groupby('category')['sales'].sum()
df.groupby(['year', 'month']).agg({
    'sales': 'sum',
    'quantity': 'mean',
    'customer_id': 'nunique'
})

# 피벗 테이블
pd.pivot_table(df, values='sales', index='month', columns='category', aggfunc='sum')

# 새 컬럼 생성
df['profit'] = df['revenue'] - df['cost']
df['profit_margin'] = df['profit'] / df['revenue'] * 100
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
```

## 시각화

### Matplotlib 기본
```python
import matplotlib.pyplot as plt

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 기본 라인 차트
plt.figure(figsize=(10, 6))
plt.plot(df['date'], df['sales'], label='매출')
plt.xlabel('날짜')
plt.ylabel('매출액')
plt.title('월별 매출 추이')
plt.legend()
plt.tight_layout()
plt.savefig('chart.png', dpi=300)
plt.show()
```

### Seaborn 차트
```python
import seaborn as sns

# 스타일 설정
sns.set_style('whitegrid')
sns.set_palette('husl')

# 바 차트
plt.figure(figsize=(10, 6))
sns.barplot(data=df, x='category', y='sales', hue='year')
plt.title('카테고리별 매출')
plt.show()

# 히트맵 (상관관계)
plt.figure(figsize=(10, 8))
sns.heatmap(df.corr(), annot=True, cmap='coolwarm', center=0)
plt.title('변수간 상관관계')
plt.show()

# 산점도
sns.scatterplot(data=df, x='price', y='sales', hue='category', size='quantity')

# 분포도
sns.histplot(df['age'], bins=20, kde=True)
sns.boxplot(data=df, x='category', y='price')
```

### Plotly 인터랙티브 차트
```python
import plotly.express as px
import plotly.graph_objects as go

# 인터랙티브 라인 차트
fig = px.line(df, x='date', y='sales', color='category',
              title='매출 추이')
fig.show()

# 파이 차트
fig = px.pie(df, values='sales', names='category',
             title='카테고리별 비중')
fig.show()

# 대시보드용 복합 차트
from plotly.subplots import make_subplots

fig = make_subplots(rows=2, cols=2,
                    subplot_titles=['매출 추이', '카테고리별 매출',
                                    '지역별 분포', '상관관계'])

fig.add_trace(go.Scatter(x=df['date'], y=df['sales']), row=1, col=1)
fig.add_trace(go.Bar(x=df['category'], y=df['sales']), row=1, col=2)
fig.update_layout(height=800, title_text="대시보드")
fig.show()
```

## 통계 분석

### 기술 통계
```python
from scipy import stats

# 기본 통계량
mean = df['column'].mean()
median = df['column'].median()
std = df['column'].std()
var = df['column'].var()

# 왜도, 첨도
skewness = df['column'].skew()
kurtosis = df['column'].kurtosis()
```

### 가설 검정
```python
# T-test (두 그룹 평균 비교)
group_a = df[df['group'] == 'A']['sales']
group_b = df[df['group'] == 'B']['sales']
t_stat, p_value = stats.ttest_ind(group_a, group_b)

# 카이제곱 검정 (범주형 변수 관계)
contingency_table = pd.crosstab(df['category'], df['purchased'])
chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)

# 상관분석
correlation, p_value = stats.pearsonr(df['x'], df['y'])
```

### 회귀 분석
```python
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error

# 데이터 준비
X = df[['feature1', 'feature2']]
y = df['target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# 모델 학습
model = LinearRegression()
model.fit(X_train, y_train)

# 예측 및 평가
y_pred = model.predict(X_test)
r2 = r2_score(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print(f'R²: {r2:.4f}')
print(f'RMSE: {rmse:.4f}')
print(f'계수: {model.coef_}')
```

## 분석 리포트 템플릿
```markdown
# 데이터 분석 리포트

## 1. 개요
- 분석 목적:
- 데이터 출처:
- 분석 기간:

## 2. 데이터 설명
- 총 레코드: X건
- 변수 수: Y개
- 결측치 비율: Z%

## 3. 주요 발견
### 3.1 [인사이트 1]
[차트]
[해석]

### 3.2 [인사이트 2]
...

## 4. 결론 및 제언
-
```

$ARGUMENTS
