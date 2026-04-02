# AI/ML Development Skill

> AI/머신러닝 개발 전문가 - 모델 학습, LLM 활용, 배포

## Triggers
- "AI", "인공지능", "머신러닝", "ML"
- "딥러닝", "모델", "학습"
- "LLM", "GPT", "Claude", "챗봇"
- "텐서플로우", "파이토치", "PyTorch"
- "예측", "분류", "추천"

## Capabilities

### 1. 머신러닝 기초

#### Scikit-learn
```python
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# 데이터 준비
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 전처리
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 모델 학습
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# 예측 및 평가
y_pred = model.predict(X_test_scaled)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print(classification_report(y_test, y_pred))
```

### 2. 딥러닝

#### PyTorch
```python
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

# 모델 정의
class NeuralNetwork(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(hidden_size, num_classes)
        )

    def forward(self, x):
        return self.layers(x)

# 학습 루프
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = NeuralNetwork(input_size=784, hidden_size=256, num_classes=10).to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

def train(model, train_loader, epochs=10):
    model.train()
    for epoch in range(epochs):
        total_loss = 0
        for batch_x, batch_y in train_loader:
            batch_x, batch_y = batch_x.to(device), batch_y.to(device)

            optimizer.zero_grad()
            outputs = model(batch_x)
            loss = criterion(outputs, batch_y)
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        print(f"Epoch {epoch+1}/{epochs}, Loss: {total_loss/len(train_loader):.4f}")

# 모델 저장/로드
torch.save(model.state_dict(), 'model.pth')
model.load_state_dict(torch.load('model.pth'))
```

### 3. LLM 활용

#### OpenAI API
```python
from openai import OpenAI

client = OpenAI(api_key="your-api-key")

def chat_completion(prompt: str, system_prompt: str = None) -> str:
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.7,
        max_tokens=1000
    )

    return response.choices[0].message.content

# 사용 예시
result = chat_completion(
    prompt="Python의 리스트 컴프리헨션을 설명해주세요",
    system_prompt="당신은 친절한 Python 튜터입니다."
)
```

#### Claude API
```python
import anthropic

client = anthropic.Anthropic(api_key="your-api-key")

def ask_claude(prompt: str, system_prompt: str = None) -> str:
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system=system_prompt or "",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return message.content[0].text

# 스트리밍
def stream_claude(prompt: str):
    with client.messages.stream(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
```

### 4. RAG (Retrieval-Augmented Generation)

```python
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

# 문서 분할
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
documents = text_splitter.split_documents(raw_documents)

# 벡터 저장소 생성
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(documents, embeddings)

# RAG 체인 생성
qa_chain = RetrievalQA.from_chain_type(
    llm=OpenAI(),
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3})
)

# 질의
answer = qa_chain.run("문서에서 중요한 내용은 무엇인가요?")
```

### 5. 컴퓨터 비전

```python
import torch
import torchvision.transforms as transforms
from torchvision.models import resnet50, ResNet50_Weights
from PIL import Image

# 사전 학습 모델 로드
model = resnet50(weights=ResNet50_Weights.DEFAULT)
model.eval()

# 이미지 전처리
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# 예측
def predict_image(image_path: str):
    image = Image.open(image_path)
    input_tensor = preprocess(image).unsqueeze(0)

    with torch.no_grad():
        output = model(input_tensor)

    probabilities = torch.nn.functional.softmax(output[0], dim=0)
    top5_prob, top5_idx = torch.topk(probabilities, 5)

    return list(zip(top5_idx.tolist(), top5_prob.tolist()))
```

### 6. 자연어 처리

```python
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification

# 감성 분석
sentiment_analyzer = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")
result = sentiment_analyzer("이 제품 정말 좋아요!")

# 텍스트 분류 (커스텀)
tokenizer = AutoTokenizer.from_pretrained("klue/bert-base")
model = AutoModelForSequenceClassification.from_pretrained("klue/bert-base", num_labels=3)

def classify_text(text: str):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    outputs = model(**inputs)
    predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
    return predictions.tolist()

# 개체명 인식
ner = pipeline("ner", model="monologg/koelectra-base-v3-discriminator")
entities = ner("삼성전자가 서울에서 신제품을 발표했습니다.")

# 질의응답
qa = pipeline("question-answering", model="monologg/koelectra-base-v3-finetuned-korquad")
answer = qa(question="회사 이름은?", context="삼성전자가 서울에서 신제품을 발표했습니다.")
```

### 7. 모델 배포

#### FastAPI 서빙
```python
from fastapi import FastAPI
from pydantic import BaseModel
import torch

app = FastAPI()

# 모델 로드
model = torch.load("model.pth")
model.eval()

class PredictionRequest(BaseModel):
    features: list[float]

class PredictionResponse(BaseModel):
    prediction: int
    probability: float

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    with torch.no_grad():
        input_tensor = torch.tensor([request.features])
        output = model(input_tensor)
        probs = torch.softmax(output, dim=1)
        prediction = torch.argmax(probs, dim=1).item()
        probability = probs[0][prediction].item()

    return PredictionResponse(
        prediction=prediction,
        probability=probability
    )
```

#### Docker 배포
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 8. MLOps

```yaml
# mlflow 실험 추적
import mlflow

mlflow.set_experiment("my-experiment")

with mlflow.start_run():
    mlflow.log_param("learning_rate", 0.001)
    mlflow.log_param("epochs", 100)

    # 학습...

    mlflow.log_metric("accuracy", 0.95)
    mlflow.log_metric("loss", 0.05)

    mlflow.sklearn.log_model(model, "model")
```
