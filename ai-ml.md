---
description: AI/ML 개발. "AI", "인공지능", "머신러닝", "ML", "딥러닝", "LLM", "모델" 트리거.
---

# AI/ML 개발

## 환경 설정
```bash
pip install numpy pandas scikit-learn tensorflow torch transformers langchain openai
```

## 머신러닝 기본

### 분류 (Classification)
```python
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# 데이터 준비
X = df.drop('target', axis=1)
y = df['target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 모델 학습
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 예측 및 평가
y_pred = model.predict(X_test)
print(f'Accuracy: {accuracy_score(y_test, y_pred):.4f}')
print(classification_report(y_test, y_pred))
```

### 회귀 (Regression)
```python
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score

model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print(f'RMSE: {np.sqrt(mean_squared_error(y_test, y_pred)):.4f}')
print(f'R²: {r2_score(y_test, y_pred):.4f}')
```

### 클러스터링 (Clustering)
```python
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# 스케일링
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# K-Means
kmeans = KMeans(n_clusters=5, random_state=42)
clusters = kmeans.fit_predict(X_scaled)

# 결과 시각화
import matplotlib.pyplot as plt
plt.scatter(X_scaled[:, 0], X_scaled[:, 1], c=clusters, cmap='viridis')
plt.title('K-Means Clustering')
plt.show()
```

## 딥러닝

### PyTorch 기본
```python
import torch
import torch.nn as nn
import torch.optim as optim

# 모델 정의
class NeuralNetwork(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(hidden_size, output_size)
        )

    def forward(self, x):
        return self.layers(x)

# 학습
model = NeuralNetwork(input_size=10, hidden_size=64, output_size=2)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

for epoch in range(100):
    model.train()
    optimizer.zero_grad()
    outputs = model(X_train_tensor)
    loss = criterion(outputs, y_train_tensor)
    loss.backward()
    optimizer.step()

    if epoch % 10 == 0:
        print(f'Epoch {epoch}, Loss: {loss.item():.4f}')
```

### TensorFlow/Keras
```python
import tensorflow as tf
from tensorflow import keras

model = keras.Sequential([
    keras.layers.Dense(64, activation='relu', input_shape=(input_size,)),
    keras.layers.Dropout(0.2),
    keras.layers.Dense(64, activation='relu'),
    keras.layers.Dropout(0.2),
    keras.layers.Dense(num_classes, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

history = model.fit(
    X_train, y_train,
    epochs=50,
    batch_size=32,
    validation_split=0.2,
    callbacks=[
        keras.callbacks.EarlyStopping(patience=5, restore_best_weights=True)
    ]
)
```

## LLM 활용

### OpenAI API
```python
from openai import OpenAI

client = OpenAI(api_key="your-api-key")

def chat_completion(prompt: str, model: str = "gpt-4") -> str:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1000
    )
    return response.choices[0].message.content

# 사용
result = chat_completion("Python으로 피보나치 수열 구현해줘")
print(result)
```

### LangChain
```python
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# 프롬프트 템플릿
template = """
당신은 {role}입니다.
질문: {question}
답변:
"""

prompt = PromptTemplate(
    input_variables=["role", "question"],
    template=template
)

# 체인 생성
llm = OpenAI(temperature=0.7)
chain = LLMChain(llm=llm, prompt=prompt)

# 실행
result = chain.run(role="Python 전문가", question="데코레이터 설명해줘")
print(result)
```

### Hugging Face Transformers
```python
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification

# 감성 분석
classifier = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")
result = classifier("이 제품 정말 좋아요!")
print(result)

# 텍스트 생성
generator = pipeline("text-generation", model="gpt2")
result = generator("Once upon a time", max_length=100)
print(result)

# 커스텀 모델 로드
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased")
```

## RAG (Retrieval-Augmented Generation)
```python
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA

# 문서 분할
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
documents = text_splitter.split_documents(docs)

# 벡터 저장소 생성
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(documents, embeddings)

# QA 체인
qa_chain = RetrievalQA.from_chain_type(
    llm=OpenAI(),
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
)

# 질문
answer = qa_chain.run("문서의 주요 내용은?")
print(answer)
```

## 모델 저장 및 배포

### 모델 저장
```python
# PyTorch
torch.save(model.state_dict(), 'model.pth')
model.load_state_dict(torch.load('model.pth'))

# Keras
model.save('model.keras')
model = keras.models.load_model('model.keras')

# Scikit-learn
import joblib
joblib.dump(model, 'model.pkl')
model = joblib.load('model.pkl')
```

### FastAPI 배포
```python
from fastapi import FastAPI
from pydantic import BaseModel
import joblib

app = FastAPI()
model = joblib.load('model.pkl')

class PredictionRequest(BaseModel):
    features: list[float]

@app.post("/predict")
def predict(request: PredictionRequest):
    prediction = model.predict([request.features])
    return {"prediction": prediction[0].tolist()}
```

$ARGUMENTS
