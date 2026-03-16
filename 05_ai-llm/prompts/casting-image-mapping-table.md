# 캐스팅 이미지 프롬프트 — 백엔드 매핑 테이블

> **목적**: 한국어 UI 라벨 → 영어 프롬프트 값 자동 치환을 위한 매핑 정의
> **백엔드 담당**: 제형
> **프롬프트 담당**: 채현

---

## 1. 파일 구조 & 역할

| 파일 | 경로 (repo 기준) | 역할 | 로드 시점 |
|------|-----------------|------|----------|
| `casting_image_prompt.py` | `05_ai-llm/prompts/casting_image_prompt.py` | 고정 블록 (시스템 프롬프트) | 서버 시작 시 1회 |
| `casting_variable_blocks.json` | `05_ai-llm/prompts/casting_variable_blocks.json` | 가변 블록 매핑 테이블 (한국어→영어) | 서버 시작 시 1회 |
| `casting_combinations_sample.json` | `05_ai-llm/prompts/casting_combinations_sample.json` | 실험용 조합 샘플 (프로덕션 미사용) | 실험 노트북 전용 |

---

## 2. 프롬프트 조립 로직

```
최종 프롬프트 = 블록③ 가변(User Selection) + "\n\n" + 블록④ 고정(Quality)
```

### 블록③ User Selection (가변)
```python
# casting_variable_blocks.json에서 한국어 UI 값 → 영어 매핑
block_3 = f"{ethnicity_en} {gender}, {mood_en}, {impression_en}, {hairstyle_en}."
```

### 블록④ Quality (고정)
```python
from prompts.casting_image_prompt import CASTING_SYSTEM_PROMPT
block_4 = CASTING_SYSTEM_PROMPT
```

### 블록② Follow Reference (고정, 선택적)
```python
# reference image가 있을 때만 프롬프트 앞에 추가
from prompts.casting_image_prompt import BLOCK_FOLLOW_REF
if reference_image:
    prompt = f"{BLOCK_FOLLOW_REF}\n\n{block_3}\n\n{block_4}"
else:
    prompt = f"{block_3}\n\n{block_4}"
```

---

## 3. 가변 블록 매핑 상세

### 3.1 인종 (ethnicity)

| 한국어 UI | 영어 프롬프트 값       |
| ------ | --------------- |
| 동아시아   | East Asian      |
| 동남아시아  | Southeast Asian |
| 라틴계    | Latin American  |
| 혼혈     | Mixed ethnicity |
| 유럽     | European        |
| 남미     | South American  |

### 3.2 성별 (gender)

| 한국어 UI | 영어 프롬프트 값 |
| ------ | --------- |
| 여자     | Female    |
| 남자     | Male      |

### 3.3 분위기 (mood)

| 한국어 UI | 영어 프롬프트 값               |
| ------ | ----------------------- |
| 시크     | chic and charismatic    |
| 청량     | refreshing and youthful |
| 걸크러시   | confident woman         |
| 청순     | innocent and pure       |
| 다크     | dark                    |
| 큐트     | cute                    |
| 중성적    | androgynous             |

### 3.4 인상 (impression)

| 한국어 UI | 영어 프롬프트 값                                                     |
| ------ | ------------------------------------------------------------- |
| 날카로운   | sharp features, intense gaze, sculpted jawline                |
| 부드러운   | soft features, gentle warm eyes                               |
| 강한 눈매  | intense cat-like eyes, thick and defined eyebrows, sharp gaze |
| 묵직한    | eyes heavy with eyelids, distinct bone structure              |
| 동글동글   | round baby face, big bright eyes, dimples                     |
| 세련된    | clear bright eyes, graceful jawline, refined look             |
| 요정     | delicate face, large and sparkling eyes, pointed chin         |

### 3.5 헤어스타일 (hairstyle)

| 한국어 UI | 영어 프롬프트 값 |
|----------|----------------|
| 블랙 숏컷 | black short textured hair |
| 브라운 미디엄 | brown medium layered hair |
| 블론드 롱 | platinum blonde long straight hair |
| 블랙 롱 | black long straight hair |
| 실버 숏컷 | silver gray short buzzed hair |
| 핑크 밥컷 | pastel pink bob with bangs |
| 블랙 머쉬룸 | black mushroom cut with bangs |
| 다크브라운 웨이브 | dark brown soft wavy hair |
| 애쉬그레이 미디엄 | ash gray medium layered hair |
| 블랙 하이포니 | black hair high ponytail |

---

## 4. API 호출 파라미터

| 파라미터 | 값 | 비고 |
|---------|---|------|
| 모델 | `gemini-3.1-flash-image-preview` | Nano Banana 2 |
| response_modalities | `["IMAGE", "TEXT"]` | |
| image_size | `512` (실험) / `1024` (프로덕션) | |
| aspect_ratio | `9:16` | 세로형 프로필 |
| 비용 | ~$0.045/512px, ~$0.067/1K, ~$0.15/4K | |

---

## 5. 백엔드 통합 체크리스트

- [ ] `casting_image_prompt.py` import 확인
- [ ] `casting_variable_blocks.json` 로드 로직 추가
- [ ] 한국어 UI 값 → 영어 매핑 치환 함수 구현
- [ ] 블록 조립 함수 구현 (블록③ + 블록④)
- [ ] reference image 유무에 따른 블록② 조건부 추가
- [ ] Gemini API 호출 엔드포인트 연동
- [ ] 환경변수 `GOOGLE_API_KEY` 설정
- [ ] 에러 핸들링 (API 응답 지연, 이미지 없음 등)
