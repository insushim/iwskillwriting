# Readability Metrics & Stylometry Reference

가독성 공식 7종 + 한국어 가독성 + 문체학(Stylometry) 지표 종합 참조.
NLP 리서치 기반 실용 가이드.

---

## 1. 가독성 공식 (Readability Formulas)

### 1-1. Flesch Reading Ease (FRE)

```
FRE = 206.835 - (1.015 × ASL) - (84.6 × ASW)

ASL = Average Sentence Length (평균 문장 길이, 단어 수)
ASW = Average Syllables per Word (단어당 평균 음절 수)
```

| 점수 | 난이도 | 학년 | 적합 장르 |
|------|--------|------|----------|
| 90-100 | 매우 쉬움 | 초등 5학년 | 동화, 아동 도서 |
| 80-89 | 쉬움 | 초등 6학년 | YA, 웹소설 |
| 70-79 | 보통 쉬움 | 중학생 | 대중 소설 |
| 60-69 | 표준 | 고등학생 | 일반 소설, 자기계발 |
| 50-59 | 약간 어려움 | 대학생 | 문학 소설, 비즈니스 |
| 30-49 | 어려움 | 대학원 | 학술, 전문 |
| 0-29 | 매우 어려움 | 전문가 | 법률, 의학 |

**장르별 목표 FRE:**
- 웹소설: 75-90
- 대중 소설: 60-80
- 문학 소설: 50-70
- 자기계발: 60-75
- 비즈니스: 50-65
- 동화: 85-100

### 1-2. Flesch-Kincaid Grade Level (FKGL)

```
FKGL = (0.39 × ASL) + (11.8 × ASW) - 15.59
```

결과: 미국 교육 학년 수준 (예: 9.3 = 9학년 = 고등학교 1학년)

**목표:**
- 대중 소설: 7-9학년
- 웹소설: 5-7학년
- 비소설: 8-12학년

### 1-3. Gunning Fog Index

```
Fog = 0.4 × (ASL + 복잡한 단어 비율 × 100)

복잡한 단어 = 3음절 이상 단어 (고유명사, 합성어, -ed/-es/-ing 제외)
```

| 점수 | 수준 | 해석 |
|------|------|------|
| 6 | 쉬움 | TV/라디오 |
| 8 | 보통 | 대중 잡지 |
| 10 | 약간 어려움 | 전문 잡지 |
| 12 | 어려움 | 고등학교 졸업 |
| 14+ | 매우 어려움 | 학술 |

### 1-4. Coleman-Liau Index

```
CLI = (0.0588 × L) - (0.296 × S) - 15.8

L = 100 단어당 평균 글자 수
S = 100 단어당 평균 문장 수
```

**장점:** 음절 계산 불필요, 문자 수 기반 — 한국어 적용 가능

### 1-5. Automated Readability Index (ARI)

```
ARI = (4.71 × 단어당 평균 문자 수) + (0.5 × ASL) - 21.43
```

### 1-6. SMOG Grade

```
SMOG = 3 + √(다음절 단어 수 × 30 / 전체 문장 수)

다음절 단어 = 3음절 이상
30개 문장 샘플링 (시작 10, 중간 10, 끝 10)
```

### 1-7. Dale-Chall Readability

```
Score = 0.1579 × (어려운 단어 비율 × 100) + 0.0496 × ASL
어려운 단어 비율 > 5%이면 + 3.6365

어려운 단어 = Dale-Chall 3000 단어 목록에 없는 단어
```

---

## 2. 한국어 가독성 지수

한국어는 영어와 달리 음절 기반 분석이 어려우므로 대체 지표를 사용합니다.

### 한국어 가독성 종합 점수 (Korean Readability Score)

```python
def korean_readability_score(text):
    """한국어 가독성 종합 점수 (0-100, 높을수록 읽기 쉬움)"""
    sentences = re.split(r'[.!?。]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]

    # 1. 평균 문장 길이 (자)
    avg_sent_len = sum(len(s) for s in sentences) / len(sentences)
    sent_score = max(0, 100 - (avg_sent_len - 30) * 2)  # 30자 기준

    # 2. 문장 종결 다양성
    endings = [s[-1] if s else '' for s in sentences]
    ending_variety = len(set(endings)) / len(endings) if endings else 0
    variety_score = ending_variety * 100

    # 3. 한자어/외래어 비율 (낮을수록 쉬움)
    foreign_ratio = len(re.findall(r'[a-zA-Z\u4e00-\u9fff]', text)) / len(text)
    foreign_score = max(0, 100 - foreign_ratio * 500)

    # 4. 평균 단락 길이
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    avg_para_len = sum(len(p) for p in paragraphs) / len(paragraphs) if paragraphs else 0
    para_score = max(0, 100 - (avg_para_len - 200) * 0.5)

    # 5. 의성어/의태어 밀도 (높을수록 생동감)
    onomatopoeia = len(re.findall(r'[가-힣]{2,3}[가-힣]{2,3}', text))  # 반복 패턴

    # 종합 (가중 평균)
    total = (sent_score * 0.35 + variety_score * 0.15 +
             foreign_score * 0.20 + para_score * 0.20 + min(100, onomatopoeia) * 0.10)
    return round(total, 1)
```

### 한국어 문장 적정 길이

| 장르 | 적정 문장 길이 | 적정 단락 길이 |
|------|-------------|-------------|
| 웹소설 | 15-35자 | 100-200자 |
| 대중 소설 | 20-50자 | 150-300자 |
| 문학 소설 | 25-80자 | 200-500자 |
| 자기계발 | 20-45자 | 150-250자 |
| 동화 | 10-25자 | 50-100자 |

---

## 3. 문체학 지표 (Stylometry Metrics)

### 3-1. 어휘 다양성 (Vocabulary Richness)

**TTR (Type-Token Ratio):**
```
TTR = 고유 단어 수 / 전체 단어 수
```
- 0.4 이하: 어휘 빈약 (반복 많음)
- 0.4-0.6: 보통
- 0.6 이상: 어휘 풍부

**Yule's K (대용량 텍스트용):**
```
K = 10000 × (M2 - N) / N²

N = 전체 단어 수
M2 = Σ(i² × Vi)  (Vi = i번 등장한 단어 종류 수)
```
- 값이 낮을수록 어휘 다양

**Hapax Legomena Ratio:**
```
Hapax Ratio = 1회만 등장한 단어 수 / 전체 고유 단어 수
```
- 0.4-0.6: 일반적
- 0.7+: 매우 다양한 어휘 (문학적)

### 3-2. 문장 복잡도

**평균 문장 길이 분포:**
```python
def sentence_complexity(sentences):
    lengths = [len(s) for s in sentences]
    return {
        "mean": sum(lengths) / len(lengths),
        "std_dev": statistics.stdev(lengths),
        "cv": statistics.stdev(lengths) / (sum(lengths) / len(lengths)),  # 변동계수
        "short_pct": sum(1 for l in lengths if l < 20) / len(lengths) * 100,
        "long_pct": sum(1 for l in lengths if l > 60) / len(lengths) * 100,
    }
```

**변동계수(CV) 해석:**
- 0.3 이하: 문장 길이 단조로움 (AI 패턴 의심)
- 0.3-0.6: 자연스러운 변화
- 0.6+: 매우 다양 (의식적 스타일)

### 3-3. 감정 분석 (Sentiment/Emotion)

**VADER 감정 분석 (영어):**
```python
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()
scores = analyzer.polarity_scores(text)
# compound: -1(매우 부정) ~ +1(매우 긍정)
```

**한국어 감정 분석:**
```python
# KNU Korean Sentiment Lexicon (14,843 어휘)
# 긍정(1~3), 부정(-1~-3), 중립(0)

POSITIVE_SENTIMENT = {
    "사랑": 3, "행복": 3, "기쁨": 3, "희망": 2, "감사": 2,
    "따뜻": 2, "설레": 2, "평화": 2, "용기": 2, "자유": 2,
    # ... 확장 가능
}

NEGATIVE_SENTIMENT = {
    "죽음": -3, "절망": -3, "증오": -3, "공포": -2, "분노": -2,
    "슬픔": -2, "배신": -2, "고통": -2, "외로": -2, "불안": -2,
    # ... 확장 가능
}
```

### 3-4. Perplexity & Burstiness (AI 탐지)

**Perplexity (복잡도):**
- 다음 단어 예측의 어려움 정도
- **인간 글**: 높은 perplexity (예측 어려움)
- **AI 글**: 낮은 perplexity (예측 용이)

**Burstiness (돌발성):**
- 문장 길이와 복잡성의 변화 정도
- **인간 글**: 높은 burstiness (변화 많음)
- **AI 글**: 낮은 burstiness (일정함)

```python
def burstiness_score(sentences):
    """문장 길이의 돌발성 측정 (0-1, 높을수록 인간적)"""
    lengths = [len(s) for s in sentences]
    if len(lengths) < 2:
        return 0

    mean = sum(lengths) / len(lengths)
    variance = sum((l - mean)**2 for l in lengths) / len(lengths)
    std = variance ** 0.5

    # 변동계수 기반 점수
    cv = std / mean if mean > 0 else 0
    return min(1.0, cv)  # 0-1 정규화
```

### 3-5. Distinct-n (다양성)

```python
def distinct_n(text, n=2):
    """n-gram 다양성 (0-1, 높을수록 반복 적음)"""
    words = text.split()
    if len(words) < n:
        return 0
    ngrams = [tuple(words[i:i+n]) for i in range(len(words)-n+1)]
    return len(set(ngrams)) / len(ngrams)
```

- Distinct-1: 단어 수준 다양성
- Distinct-2: 바이그램 다양성
- Distinct-3: 트라이그램 다양성

**목표:**
- Distinct-1: 0.7+ (좋음)
- Distinct-2: 0.85+ (좋음)

---

## 4. 주제 분석 (Topic Analysis)

### LDA 기반 챕터별 주제 추적

```python
from gensim import corpora, models

def track_chapter_topics(chapters, num_topics=5):
    """챕터별 주제 분포 추적"""
    # 형태소 분석 후 명사 추출
    texts = [extract_nouns(ch) for ch in chapters]
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]

    lda = models.LdaModel(corpus, num_topics=num_topics, id2word=dictionary)

    # 챕터별 주제 분포
    results = []
    for i, bow in enumerate(corpus):
        topic_dist = lda.get_document_topics(bow)
        results.append({
            "chapter": i + 1,
            "dominant_topic": max(topic_dist, key=lambda x: x[1])[0],
            "distribution": topic_dist,
        })
    return results
```

---

## 5. 캐릭터 추적 (NER for Fiction)

### 이름 빈도 추적

```python
def track_character_presence(chapters, character_names):
    """캐릭터 챕터별 등장 빈도 추적"""
    presence = {name: [] for name in character_names}

    for ch_num, content in enumerate(chapters, 1):
        for name in character_names:
            count = content.count(name)
            presence[name].append({
                "chapter": ch_num,
                "mentions": count,
            })

    return presence
```

### 대명사 비율 (Pronoun Ratio)

```python
def pronoun_ratio(text):
    """대명사 사용 비율 — 높으면 coreference 혼란 위험"""
    pronouns = ["그", "그녀", "그들", "이것", "그것", "그래서"]
    total_words = len(re.findall(r'[가-힣]+', text))
    pronoun_count = sum(text.count(p) for p in pronouns)
    return pronoun_count / total_words if total_words > 0 else 0
```

---

## 6. 자동화 통합 가이드

### style_analyzer.py에서 사용할 메트릭 우선순위

| 우선순위 | 메트릭 | 구현 난이도 | 효과 |
|---------|--------|-----------|------|
| 1 | 한국어 가독성 점수 | 쉬움 | 높음 |
| 2 | 문장 길이 CV (변동계수) | 쉬움 | 높음 |
| 3 | TTR (어휘 다양성) | 쉬움 | 중간 |
| 4 | Burstiness 점수 | 중간 | 높음 (AI 탐지) |
| 5 | 감정 극성 추적 | 중간 | 높음 |
| 6 | Distinct-2 | 쉬움 | 중간 |
| 7 | Hapax Legomena | 쉬움 | 낮음 |
| 8 | 캐릭터 등장 추적 | 중간 | 중간 |
| 9 | 대명사 비율 | 쉬움 | 낮음 |
| 10 | LDA 주제 추적 | 어려움 | 중간 |
