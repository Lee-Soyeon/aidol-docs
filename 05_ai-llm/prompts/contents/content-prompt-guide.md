# 콘텐츠 이미지 프롬프트 가이드

> **목적**: 콘텐츠 유형별(일상/손가락 하트/학교) 이미지 생성 프롬프트 구조 및 조합 정의
> **프롬프트 담당**: 채현
> **기획 참고**: `08_contents/콘텐츠_기획/`

---

## 1. 파일 구조 & 역할

| 파일                       | 경로 (repo 기준)              | 역할                                                             |
| -------------------------- | ----------------------------- | ---------------------------------------------------------------- |
| `base_content_prompt.py`   | `05_ai-llm/prompts/contents/` | 공통 고정 블록 (Identity Lock, Constraint Lock, build_prompt)    |
| `daily_prompt.py`          | `05_ai-llm/prompts/contents/` | 일상 스냅 콘텐츠 가변 옵션                                       |
| `finger_prompt.py`         | `05_ai-llm/prompts/contents/` | 손가락 하트 콘텐츠 가변 옵션                                     |
| `school_prompt.py`         | `05_ai-llm/prompts/contents/` | 학교 생활 콘텐츠 가변 옵션                                       |
| `daily_combinations.json`  | `05_ai-llm/prompts/contents/` | 일상 스냅 실험용 조합 (8개)                                      |
| `finger_combinations.json` | `05_ai-llm/prompts/contents/` | 손가락 하트 실험용 조합 (6개)                                    |
| `school_combinations.json` | `05_ai-llm/prompts/contents/` | 학교 생활 실험용 조합 (8개)                                      |
| `photocard-prompt-spec.md` | `05_ai-llm/prompts/contents/` | stable key, base/concept guide, option prompt, context 정책 문서 |

---

## 2. 프롬프트 조립 로직

```
최종 프롬프트 = Identity Lock
              + Scene (장소 + 행동)
              + Gaze (시선)
              + Expression (표정)
              + Outfit (의상)
              + Camera (구도)
              + Atmosphere (분위기)
              + Constraint Lock
```

### 공통 고정 블록 (`base_content_prompt.py`)

| 블록              | 역할                                                        |
| ----------------- | ----------------------------------------------------------- |
| `IDENTITY_LOCK`   | 레퍼런스 이미지와 동일한 얼굴 특징, 피부톤, 골격 유지       |
| `CONSTRAINT_LOCK` | 신체 비율, 눈 대칭, 팔/손 해부학적 정확성, 프레임 정리 제약 |

### 가변 블록 (콘텐츠별 `*_prompt.py`)

각 콘텐츠 모듈은 6개 가변 옵션(Scene, Gaze, Expression, Outfit, Camera, Atmosphere)을 딕셔너리로 정의하고, `base_content_prompt.build_prompt()`를 래핑합니다.

---

## 3. 콘텐츠별 옵션 요약

### 3.1 일상 스냅 (`daily_prompt.py`)

| 옵션       | 개수 | 값                                                               |
| ---------- | ---- | ---------------------------------------------------------------- |
| Scene      | 3    | 편의점, 주차장, 침실                                             |
| Gaze       | 2    | 왼쪽 흘깃, 오른쪽 멍하게                                         |
| Expression | 5    | 무표정, 피곤한, 부드러운 미소, 멍한, 궁금한                      |
| Outfit     | 4    | 그래픽티, 블랙티+와이드데님, 후디+흰티, 니트스웨터               |
| Camera     | 6    | 눈높이, 로우앵글, 하이앵글, 클로즈업, 미디엄와이드, 사이드프로필 |
| Atmosphere | 4    | 캔디드, 자연광, 로파이, 심야                                     |

### 3.2 손가락 하트 (`finger_prompt.py`)

| 옵션       | 개수 | 값                                                |
| ---------- | ---- | ------------------------------------------------- |
| Scene      | 1    | K팝 연습실 (고정)                                 |
| Gaze       | 4    | 살짝 아래, 옆으로 장난스럽게, 눈맞춤, 위로 몽환적 |
| Expression | 4    | 부드러운 미소, 수줍은, 밝은, 장난스러운           |
| Outfit     | 4    | 바시티자켓, 럭비폴로, 민소매캐주얼, 후드티+츄리닝 |
| Camera     | 4    | 클로즈업 정면, 허리 위, 가슴 위, 하이앵글         |
| Atmosphere | 1    | 아이돌 캐주얼 (고정)                              |

### 3.3 학교 생활 (`school_prompt.py`)

| 옵션       | 개수 | 값                                                       |
| ---------- | ---- | -------------------------------------------------------- |
| Scene      | 5    | 교실, 복도, 계단, 옥상, 편의점                           |
| Gaze       | 5    | 창밖, 옆 흘깃, 눈맞춤, 아래, 먼곳                        |
| Expression | 5    | 부드러운 미소, 웃참, 졸린, 멍한, 장난스러운              |
| Outfit     | 4    | 카디건+셔츠, 블레이저+셔츠, 카디건+티, 블레이저+티       |
| Camera     | 6    | 눈높이, 클로즈업, 하이앵글, 사이드앵글, 미디엄, 로우앵글 |
| Atmosphere | 4    | 스티커, 형광등 낙서, 골든아워, 흐린 날                   |

---

## 4. 조합 파일 (`*_combinations.json`) 구조

```json
{
  "meta": {
    "prompt_type": "finger",
    "prompt_file": "finger_prompt.py",
    "total_combinations": 6
  },
  "combinations": [
    {
      "id": "F-001",
      "label": "연습실 · 바시티자켓 · 눈맞춤 · 부드러운미소",
      "scene": "practice_room",
      "gaze": "eye_contact",
      "expression": "gentle_smile",
      "outfit": "varsity_jacket",
      "camera": "closeup_front",
      "atmosphere": "idol_casual"
    }
  ]
}
```

각 조합의 키워드 값은 해당 `*_prompt.py`의 OPTIONS 딕셔너리 키에 대응합니다.

---

## 5. 실험 결과 요약

| 실험                     | 모델             | 캐릭터 | 조합 | 생성 수   | 성공    | 실패  | 비용       |
| ------------------------ | ---------------- | ------ | ---- | --------- | ------- | ----- | ---------- |
| Daily (v4-6chars)        | gemini-3.1-flash | 6명    | 8개  | 48장      | 48      | 0     | $2.160     |
| Finger Heart (v3-6chars) | gemini-3.1-flash | 6명    | 6개  | 36장      | 36      | 0     | $1.620     |
| School (v1)              | gemini-3.1-flash | 5명    | 8개  | 40장      | 40      | 0     | $1.800     |
| **합계**                 |                  |        |      | **124장** | **124** | **0** | **$5.580** |

---

## 6. API 호출 파라미터

| 파라미터            | 값                               | 비고          |
| ------------------- | -------------------------------- | ------------- |
| 모델                | `gemini-3.1-flash-image-preview` | Nano Banana 2 |
| response_modalities | `["TEXT", "IMAGE"]`              |               |
| 비용                | ~$0.045/장                       | 512px 기준    |

---

## 7. 기획 문서 참고

| 콘텐츠      | 기획 문서                                           |
| ----------- | --------------------------------------------------- |
| 일상 스냅   | `08_contents/콘텐츠_기획/idol-daily-snap-plan.md`   |
| 손가락 하트 | `08_contents/콘텐츠_기획/idol-finger-heart-plan.md` |
| 학교 생활   | `08_contents/콘텐츠_기획/idol-school-life-plan.md`  |
