# 무면허라이더 - AI 기반 운전면허 학습 도우미

## 팀원 소개
###  팀원 닮은꼴 소개 
|김원철|박규택|이주원|정재현|허지원|
|:---:|:---:|:---:|:---:|:---:|
|<img src="https://i.ytimg.com/vi/SVyVlHUMjSM/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLAYLstFr6SllE04oBlOw_eSSfScaQ"  width="150" height="150"/> |<img src="https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2F20150609_245%2Frmxtkfkd11de_1433841374678NOqpo_PNG%2Ff2.PNG&type=sc960_832"  width="150" height="150"/> |<img src="https://image.aladin.co.kr/product/31290/46/letslook/K512832670_t5.jpg"  width="150" height="150"/>  | <img src="https://i.namu.wiki/i/lwgo8HESi5bQw3QtjMzRmJIG-nca97WHdTrp6LybH74QbWlsyN8-KHP3Hd5SfAKOppzwyU5Es6PdUZifInC_mtauuH9T7NnrZXMpJHEWITMbUskPa6XD-pga2TCK8gmqK81llE2fb-a1gguWB5EkeA.webp"  width="150" height="150"/> |<img src="https://upload3.inven.co.kr/upload/2022/06/20/bbs/i14951952770.jpg?MW=800"  width="150" height="150"/>  |
| <center> 면허 있음 </center> | <center> 면허 없음 </center> | <center> 면허 없음 </center> | <center> 면허 있음(셀카임) </center> | <center> 면허 없음 </center> |
---

## 프로젝트 소개
AI 기술을 활용한 운전면허 필기시험 학습 도우미 서비스입니다. 사용자의 질문에 맞춤형 문제를 추천하고, 답변에 대한 상세 해설을 제공하며 교통 표지판 인식 기능을 포함합니다.

## 주요 기능

### 1. AI 기반 문제 추천 시스템
- Multilingual-E5-Large 모델을 활용한 텍스트 임베딩
- 코사인 유사도 기반 맞춤형 문제 추천
- 실시간 대화형 인터페이스

### 2. 지능형 답변 평가 시스템
- GPT-3.5 기반 답변 정확도 평가
- 맞춤형 오답 해설 생성
- 단계별 학습 가이드 제공

### 3. 교통 표지판 인식 시스템
- BLIP 모델 기반 이미지 캡셔닝
- GPT-4 활용 상세 설명 생성
- 실시간 이미지 처리

## 기술 스택

### Frontend
- Streamlit
- PIL (Python Imaging Library)

### Backend
- Python 3.8+
- OpenAI API
- Transformers Library

### AI/ML
- BLIP (이미지 캡셔닝)
- GPT-3.5/4 (텍스트 생성)
- Multilingual-E5-Large (텍스트 임베딩)

## 코드 리뷰 및 아키텍처 분석

### 주요 컴포넌트 분석

### 1. Core Components

#### app.py (메인 애플리케이션)
- Streamlit 기반 대화형 인터페이스 구현
- 상태 관리 패턴을 통한 사용자 세션 관리
- Chain 패턴을 활용한 모듈식 설계
```mermaid
flowchart TD
    A[사용자 입력] --> B{입력 타입 확인}
    B -->|질문| C[추천 체인 실행]
    B -->|답변| D[답변 체크 체인 실행]
    C --> E[상태 업데이트]
    D --> E
    E --> F[결과 표시]
    F --> G[대화 기록 저장]
```

#### chatbot_langchain.py (LangChain 통합)
- LangChain 기반 AI 에이전트 구현
- 문제 추천 및 답변 평가 통합
- 세션 기반 상태 관리
```mermaid
flowchart TD
    A[초기화] --> B[에이전트 생성]
    B --> C{사용자 입력}
    C -->|문제 요청| D[문제 추천]
    C -->|답변| E[답변 평가]
    D --> F[결과 표시]
    E --> F
```

#### car.py (이미지 처리)
- BLIP 모델 기반 이미지 캡셔닝
- GPT-4 통합 설명 생성
- 이미지-텍스트 멀티모달 처리
```mermaid
flowchart TD
    A[이미지 업로드] --> B[BLIP 처리]
    B --> C[캡션 생성]
    C --> D[GPT-4 설명 생성]
    D --> E[결과 표시]
```

### 2. Chain Components

#### wc_chain.py
- 문서 로딩 및 벡터화
- 임베딩 생성 및 저장
- 컨텍스트 기반 응답 생성

#### answer_check_chain.py
- 답변 정확도 평가
- 맞춤형 피드백 생성
- 오답 노트 관리

### 3. Utility Components

#### embedding.py
- 텍스트 임베딩 생성
- 모델 최적화
- 벡터 연산 처리

#### find_similar_question.py
- 코사인 유사도 계산
- 문제 추천 알고리즘
- 데이터 전처리

## 페이지별 플로우 차트

### save.py (틀린 문제 저장)
```mermaid
flowchart TD
    A[페이지 로드] --> B[세션 상태 확인]
    B --> C{저장된 대화 존재?}
    C -->|Yes| D[대화 내용 표시]
    C -->|No| E[경고 메시지 표시]
    D --> F[사용자 질문 및 AI 답변 페어링]
    F --> G{각 질문에 대해}
    G -->|Yes| H[질문 및 답변 표시]
    H --> I[💾 메모장에 저장 버튼]
    I --> J{이미 저장된 문제인가?}
    J -->|No| K[틀린 문제 저장]
    K --> L[성공 메시지 표시]
    J -->|Yes| M[이미 저장됨 메시지 표시]
    G -->|No| N[저장된 문제 목록 확인]
    N --> O{메모장에 틀린 문제 존재?}
    O -->|Yes| P[메모장에 질문 및 답변 표시]
    P --> Q[🗑️ 삭제 버튼]
    Q --> R[문제 삭제 및 새로고침]
    O -->|No| S[저장된 문제가 없음 메시지 표시]

```

### car.py (이미지 인식)
```mermaid
flowchart TD
    A[이미지 업로드] --> B{유효한 이미지?}
    B -->|Yes| C[BLIP 처리]
    B -->|No| D[에러 메시지]
    C --> E[GPT 설명 생성]
    E --> F[결과 표시]
```

### chatbot_langchain.py (AI 챗봇)
```mermaid
flowchart TD
    A[초기화] --> B[에이전트 생성]
    B --> C{사용자 입력}
    C --> D[입력 처리]
    D --> E[AI 응답 생성]
    E --> F[결과 표시]
    F --> C
```
