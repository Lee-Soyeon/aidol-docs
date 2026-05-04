# 컴패니언 프로필 프롬프트 옵션 키 가이드

> 목적: companion profile prompt option key의 최종 stable 형식과 각 key에 대응하는 프롬프트 문구를 정의한다.

> 범위: 컴패니언 프로필 (K-pop 아이돌 캐스팅 헤드샷) 단일 모듈

> 원칙: 이 문서에는 앞으로 사용할 stable key와 프롬프트만 적는다.

> 소스 파일: `prompts/companion_profile/base.py`, `prompts/companion_profile/profile.py`

---

## 1. 공통 규칙

- key는 영어 `UPPER_SNAKE_CASE`를 사용한다 (Python `str, Enum` 호환).
- key는 UI 문구가 아니라 내부 식별자다.
- key는 가능한 한 한 축의 의미만 담는다.
- 한국어 라벨은 문서/UI용이고, 저장 및 코드 식별에는 stable key를 사용한다.
- 같은 key명이라도 모듈/축이 다르면 프롬프트가 다를 수 있다.

### 축 정의

| 축            | 의미                         | 네이밍 원칙                                             |
| ------------- | ---------------------------- | ------------------------------------------------------- |
| `gender`      | 성별                         | 단일 단어                                               |
| `ethnicity`   | 인종/혼혈 정체성             | 지역 또는 혼혈 조합 식별                                |
| `mood`        | 분위기 (표현 layer)          | 형용사 중심, 한 단어로 표현 가능한 것                   |
| `eye_color`   | 홍채 색                      | 색상 중심                                               |
| `face_shape`  | 얼굴 골격·형태               | 얼굴을 만드는 골격 신호 중심                            |
| `hair_color`  | 머리 색                      | 색상 중심                                               |
| `hair_style`  | 헤어스타일 (길이·형태)       | 성별별로 슬롯이 분리되며, 길이/형태/실루엣 중심         |
| `skin_detail` | 피부 디테일 (점·주근깨 등)   | 단일 디테일 단위                                        |

> 위 8개 축은 모두 사용자가 명시적으로 선택하는 입력이다. 별도로 매 생성 시 서버에서 균등 랜덤으로 채워지는 자동 가변 슬롯(마이크로 디테일)이 있다 — 6장 참고.

---

## 2. 상위 개념

### prompt module key

| key                 | 한국어            |
| ------------------- | ----------------- |
| `companion_profile` | 컴패니언 프로필   |

### API / DB 입력 컨텍스트

| 필드              | 타입   | 비고                                                        |
| ----------------- | ------ | ----------------------------------------------------------- |
| `gender_key`      | string | 4.1 표의 stable key                                         |
| `ethnicity_key`   | string | 4.2 표의 stable key                                         |
| `mood_key`        | string | 4.3 표의 stable key                                         |
| `eye_color_key`   | string | 4.4 표의 stable key                                         |
| `face_shape_key`  | string | 4.5 표의 stable key                                         |
| `hair_color_key`  | string | 4.6 표의 stable key                                         |
| `hair_style_key`  | string | `gender_key`에 따라 4.7 또는 4.8 표를 사용                  |
| `skin_detail_key` | string | 4.9 표의 stable key                                         |

---

## 3. 고정 프롬프트

> `Prompt (EN)`은 런타임 프롬프트의 문장 순서를 그대로 적었고, 코드에서는 줄바꿈 문자열로 관리한다.

### 3.1 장르 (genre) — 항상 적용, 첫 블록

| stable key                     | 한국어 라벨               | Prompt (EN)                                                                 | 해석 (KR)                                                            | 적용 범위 |
| ------------------------------ | ------------------------- | --------------------------------------------------------------------------- | -------------------------------------------------------------------- | --------- |
| `COMPANION_IMAGE_GENRE_PROMPT` | 캐스팅 헤드샷 장르 선언   | Photorealistic K-pop idol casting headshot in professional ID photo style. | 사실적인 K-pop 아이돌 캐스팅 헤드샷, 전문 증명사진 스타일.           | 전체 공통 |

### 3.2 품질·제약 (quality) — 항상 적용, 마지막 블록

| stable key                       | 한국어 라벨                  | 적용 범위 |
| -------------------------------- | ---------------------------- | --------- |
| `COMPANION_IMAGE_QUALITY_PROMPT` | 캐스팅 헤드샷 품질·제약 블록 | 전체 공통 |

> 두 개의 산문 문단으로 구성된다. 1문단은 구도·배경·조명·카메라, 2문단은 품질 기준 + semantic negative (Do NOT 명령형 미사용).

Prompt (EN):

```
A tight professional headshot composition with the face filling the frame, centered in the upper two-thirds, front-facing with eyes at camera, wearing a plain white crew-neck t-shirt against a seamless single-color white paper studio backdrop free of gradient, objects, walls, windows, or environment. Soft butterfly lighting with gentle fill in pure white provides symmetrical even illumination and a soft shadow only under the chin. Shot on a Canon EOS R5 with an 85mm f/1.4 portrait lens, ultra-sharp focus on the eyes, 4K resolution.

The subject is extremely photogenic with perfect facial symmetry, harmonious golden-ratio proportions, smooth dewy youthful skin showing subtle fine pores and authentic natural texture, and a fresh-faced softness that reads unmistakably as a teenage idol trainee aged 17-19 rather than an adult. The iris stays natural with subtle striations, a soft limbal ring, and realistic depth, never colored-contact, oversaturated, glowing, glassy, or CGI-like. Hair color and length match the description exactly and the specified gender is preserved. The skin is clear of facial hair, forehead wrinkles, eye wrinkles, nasolabial folds, neck lines, and sagging. A single subject occupies the frame, free of additional faces, text, or watermark.
```

해석 (KR):

- 1문단: 얼굴이 프레임을 채우는 타이트 정면 헤드샷, 흰 크루넥 티셔츠, 단색 화이트 페이퍼 배경(그라데이션·소품·벽·창·환경 없음). 좌우 대칭 균일한 부드러운 버터플라이 + 필 라이팅, 턱 아래에만 옅은 그림자. Canon EOS R5 + 85mm f/1.4, 눈에 초점, 4K.
- 2문단(semantic negative 통합): 좌우 대칭 황금비, 매끈하고 윤기 있는 어린 피부, 17-19세 연습생으로 보이는 fresh-faced softness. 홍채는 자연스러운 striation·limbal ring·realistic depth 유지(컬러 콘택트·CGI 눈은 거론조차 평서형으로). 헤어 색/길이와 성별은 입력 그대로 유지. 피부에 수염·이마/눈가 주름·팔자주름·목 주름·처짐 없음. 1인 피사체, 추가 인물·텍스트·워터마크 없음.

---

## 4. 사용자 선택 옵션

### 4.1 Gender

| stable key | 한국어 라벨 | Prompt (EN) |
| ---------- | ----------- | ----------- |
| `FEMALE`   | 여자        | Female      |
| `MALE`     | 남자        | Male        |

### 4.2 Ethnicity

| stable key        | 한국어 라벨 | Prompt (EN)                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| ----------------- | ----------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `EAST_ASIAN`      | 동아시아    | East Asian features — refined facial harmony with balanced almond-shaped double-eyelid eyes, clean straight nose bridge proportional to the face, smooth oval facial structure with elegant Korean/Japanese/Chinese proportions                                                                                                                                                                                                                              |
| `SOUTHEAST_ASIAN` | 동남아시아  | Southeast Asian features with K-pop idol refinement — large round expressive double-eyelid eyes with bright vivid gaze, gently rounded facial structure with softer volume, naturally fuller lips, softly defined nose with delicate slim proportions, warm-toned harmonious balance                                                                                                                                                                         |
| `EUROPEAN`        | 유럽        | European Caucasian features — high straight nose bridge with sharply defined ridge, deep-set large open eyes with prominent eyelid crease, sharply sculpted angular jawline and high cheekbones, dimensional facial depth and Western bone structure                                                                                                                                                                                                         |
| `SOUTH_AMERICAN`  | 남미        | South American Latin features with youthful K-pop trainee softness — Mediterranean-influenced facial structure with hints of Indigenous American heritage, expressive deep-set double-eyelid eyes with luminous bright youthful gaze, prominent straight nose bridge, softly defined cheekbones, balanced Latin facial structure with warm radiant aura, smooth dewy teen skin                                                                               |
| `KOR_JPN`         | 한-일 혼혈  | Korean-Japanese mixed heritage, refined East Asian features — straight clean nose bridge, large almond double-eyelid eyes, delicate oval face with elegant bone structure                                                                                                                                                                                                                                                                                    |
| `KOR_RUS`         | 한-러 혼혈  | Korean-Russian mixed heritage with Russian Slavic descent, distinctly visible hybrid identity balancing both ancestries — sharply chiseled high nose bridge with clearly defined ridge typical of Russian Slavic features, deep-set double-eyelid almond eyes with refined upturned outer corners, sharply sculpted high cheekbones with angular jawline, dimensional facial depth and angular bone structure typical of Russian Slavic heritage while retaining unmistakable Korean facial harmony and eye proportions — looks neither purely Korean nor purely Russian |
| `KOR_USA`         | 한-미 혼혈  | Korean-American mixed heritage with Western Caucasian descent — appearing unmistakably mixed-race rather than purely East Asian, with clearly Western-influenced features: high straight nose bridge with prominent dimensional ridge, deep-set double-eyelid eyes blending East Asian almond shape with Western depth, prominently dimensional cheekbones, sculpted Western-style jawline, dimensional facial depth typical of Caucasian bone structure while retaining Korean facial harmony — distinctly hybrid, neither purely Korean nor purely Western |
| `KOR_CAN`         | 한-캐 혼혈  | Korean-Canadian mixed heritage with Anglo-Canadian British Isles descent — appearing unmistakably mixed-race rather than purely East Asian, with clearly Western-influenced features: prominent high straight nose bridge with dimensional ridge, large round open double-eyelid eyes with Caucasian-leaning luminous depth and bright clear gaze, sharply dimensional high cheekbones, defined angular jawline, Anglo-Canadian British Isles bone structure while retaining Korean facial harmony — distinctly hybrid, neither purely Korean nor purely Western |

### 4.3 Mood

| stable key     | 한국어 라벨   | Prompt (EN)             |
| -------------- | ------------- | ----------------------- |
| `CHIC`         | 시크          | chic and charismatic    |
| `REFRESHING`   | 청량          | refreshing and youthful |
| `CONFIDENT`    | 자신감있는    | confident               |
| `PURE`         | 청순          | innocent and pure       |
| `DARK`         | 다크          | dark and mysterious     |
| `CUTE`         | 큐트          | cute                    |
| `PLAYFUL`      | 장난스러운    | playful                 |
| `ETHEREAL`     | 신비로운      | ethereal, mysterious    |
| `REFINED`      | 세련된        | polished and refined    |
| `AFFECTIONATE` | 다정한        | warm and affectionate   |
| `SHY`          | 수줍은        | shy and demure          |

### 4.4 Eye Color

| stable key   | 한국어 라벨 | Prompt (EN)                                                                                                                                                                                 |
| ------------ | ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `BROWN`      | 브라운      | warm natural brown eyes with realistic iris striations and a soft limbal ring                                                                                                               |
| `DARK_BROWN` | 다크 브라운 | natural dark brown eyes with a subtle warm undertone and soft realistic iris detail, calmly grounded gaze, distinguishable from pure black yet never glossy, dramatic, or contact-lens-like |
| `HAZEL`      | 헤이즐      | hazel eyes with a natural green-brown gradient and realistic iris detail                                                                                                                    |
| `AMBER`      | 앰버        | subtly amber-tinted dark brown eyes with a warm golden undertone visible only on close inspection, naturalistic and grounded, never yellow, glowing, or contact-lens-like                   |
| `BLACK`      | 블랙        | deep brown eyes (distinguishable from raven black, never void) with clearly visible warm brown iris striations, a soft limbal ring, and a naturally lit pupil                              |

### 4.5 Face Shape

> 구조적 identity. 얼굴 뼈대·눈/눈썹 형태처럼 얼굴을 만드는 골격 신호.

| stable key | 한국어 라벨 | Prompt (EN)                                                                                                |
| ---------- | ----------- | ---------------------------------------------------------------------------------------------------------- |
| `SHARP`    | 날카로운    | sharp features, an intense gaze, and a sculpted jawline                                                    |
| `SOFT`     | 부드러운    | soft features and gentle warm eyes                                                                         |
| `INTENSE`  | 강한 눈매   | intense sharp-angled almond eyes with upturned outer corners, thick defined eyebrows, and a piercing gaze  |
| `HEAVY`    | 무게감      | softly heavy-lidded eyes with composed refined presence and grounded bone structure carrying a youthful idol aura |
| `DEEP`     | 깊은 눈     | deep-set eyes with a thoughtful mysterious presence                                                        |

### 4.6 Hair Color

> hair_style 값에 이미 `hair` / `bob` / `ponytail` 같은 명사가 들어 있어 빌더가 그대로 공백 결합한다. 따라서 hair_color 값은 색 형용사만 담는다.

| stable key   | 한국어 라벨 | Prompt (EN)                                     |
| ------------ | ----------- | ----------------------------------------------- |
| `BLACK`      | 블랙        | black                                           |
| `DARK_BROWN` | 다크 브라운 | dark brown                                      |
| `CHESTNUT`   | 체스트넛    | chestnut                                        |
| `AUBURN`     | 어번        | auburn                                          |
| `BROWN`      | 브라운      | brown                                           |
| `RED`        | 레드        | red                                             |
| `BLONDE`     | 블론드      | blonde                                          |
| `PLATINUM`   | 플래티넘    | platinum                                        |
| `PINK`       | 핑크        | cool desaturated muted dusty pink               |
| `ASH_GRAY`   | 애쉬 그레이 | naturally desaturated cool-toned dark ash       |

### 4.7 Hair Style — Male

> `gender_key = MALE`일 때만 사용한다.

| stable key   | 한국어 라벨           | Prompt (EN)                                                                                |
| ------------ | --------------------- | ------------------------------------------------------------------------------------------ |
| `SHORT`      | 숏컷                  | short textured hair in K-pop idol styling                                                  |
| `MUSHROOM`   | 머쉬룸 컷             | modern textured mushroom cut with airy bangs in K-pop idol styling                         |
| `MEDIUM`     | 미디엄 레이어드       | medium layered hair in K-pop idol styling                                                  |
| `WAVY`       | 웨이브                | wavy hair in K-pop idol styling                                                            |
| `CURLY`      | 컬리                  | curly hair in K-pop idol styling                                                           |
| `BANGS`      | 볼륨 뱅스             | voluminous styled hair with airy textured bangs in K-pop idol styling                      |
| `TWO_BLOCK`  | 투블럭                | two-block cut with voluminous top and cropped sides in K-pop idol styling                  |
| `WOLF`       | 울프 컷               | edgy wolf cut with layered texture and a longer back in K-pop idol styling                 |
| `COMMA`      | 콤마 헤어             | polished comma-shaped side-swept fringe with glossy soft volume, the signature K-pop boy idol look |

### 4.8 Hair Style — Female

> `gender_key = FEMALE`일 때만 사용한다.

| stable key        | 한국어 라벨    | Prompt (EN)              |
| ----------------- | -------------- | ------------------------ |
| `LONG_STRAIGHT`   | 롱 스트레이트  | long straight hair       |
| `SHOULDER_LENGTH` | 어깨 길이      | shoulder-length hair     |
| `BOB`             | 뱅 밥컷        | bob with bangs           |
| `MEDIUM`          | 미디엄 레이어드 | medium layered hair      |
| `WAVY`            | 웨이브         | wavy hair                |
| `CURLY`           | 컬리           | curly hair               |
| `BRAIDED`         | 브레이드       | braided hair             |
| `PONYTAIL`        | 포니테일       | ponytail                 |
| `HIGH_PONYTAIL`   | 하이 포니테일  | high ponytail            |
| `BANGS`           | 뱅 헤어        | hair with bangs          |
| `FLOWING`         | 플로잉 루즈    | flowing loose hair       |

### 4.9 Skin Detail

| stable key       | 한국어 라벨       | Prompt (EN)                                                                                                                                                              |
| ---------------- | ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `FRECKLES`       | 주근깨            | clearly visible natural freckles densely scattered across the nose bridge and cheeks with realistic skin texture                                                         |
| `MOLE`           | 점                | one small distinct natural mole on the cheek                                                                                                                             |
| `DIMPLES`        | 양 볼 보조개      | natural clearly visible deep dimples on both cheeks, gently activated by a soft natural smile to reveal them prominently                                                 |
| `SINGLE_DIMPLE`  | 한쪽 보조개       | one natural clearly visible deep dimple on a single cheek, gently activated by a soft natural smile to reveal it prominently                                             |
| `CHEEKBONES`     | 도드라진 광대     | clearly defined high cheekbones with visible structural prominence                                                                                                       |
| `CLEAR_SKIN`     | 깨끗한 피부       | clear unmarked skin                                                                                                                                                      |

---

## 5. 프롬프트 조립 로직

> 빌더 함수: `build_companion_profile_prompt(context: CompanionProfilePromptContext)`
> 출력은 라벨/bullet 없는 narrative 문단들로 구성된다 (Gemini Image 가이드 권고).

### 5.1 블록 순서

```
[GENRE 한 줄]
        ↓
[Subject 문단 — 5 sentences narrative]
        ↓
[QUALITY 문단 — composition·lighting·camera + quality·semantic negative]
```

세 블록은 `\n\n`으로 결합한다 (`compose_prompt`). 각 블록 내부는 라벨이나 bullet 없이 일반 문장으로만 구성된다.

### 5.2 Subject 문단 템플릿 (5개 문장)

빌더는 8개 stable key 와 자동 가변 슬롯 1회 sampling 결과를 받아 다음 5개 문장을 정확히 이 순서로 출력한다.

```
A stunningly attractive late-teen {gender_lower} K-pop idol trainee aged 17-19 with {ethnicity}.
The face shows {face_shape}, with {eye_color}.
The expression reads {mood}.
The subject has {hairstyle} and {skin_detail}.
Subtle micro features include {eye_spacing} with {eye_opening}, {brow_shape} at {brow_pos}, {nose_tip}, {lip_shape} with {mouth_width}, {chin_length} with {chin_width}, and {midface}.
```

규칙:

- `{gender_lower}` — `Female`/`Male` 을 lowercase 한 값.
- `{hairstyle}` — `hair_color` + `' '` + `hair_style` 를 공백으로 결합. 예: `BLACK` + `BRAIDED` → `black braided hair`. `BLACK` + `TWO_BLOCK` → `black two-block cut with voluminous top and cropped sides in K-pop idol styling`. dict 값 자체가 결합용 fragment 형태 (색은 형용사만, 스타일은 선행 관사 없이) 라 별도 가공 없이 결합한다.
- 자동 가변 슬롯의 모든 값은 이미 article 포함 형태로 저장되어 있어 별도 가공 없이 슬롯 그대로 끼워 넣는다 (6장 참고).

### 5.3 GENRE / QUALITY 블록

`base.py` 의 다음 두 상수가 그대로 사용된다 (3.1, 3.2 참고).

- `COMPANION_IMAGE_GENRE_PROMPT` — 한 문장.
- `COMPANION_IMAGE_QUALITY_PROMPT` — 두 문단(구도/조명/카메라 + 품질/semantic negative).

---

## 6. 자동 가변 슬롯 (마이크로 디테일)

> 사용자가 선택하지 않는다. 매 생성 시 서버에서 슬롯별로 균등 랜덤 1개를 뽑아 5.2 의 마지막 문장 (`Subtle micro features include …`) 으로 끼워 넣는다. 같은 8개 입력에서도 결과가 미세하게 변주되도록 다양성을 부여하는 것이 목적이다.

### 6.1 슬롯 정의

> 모든 Prompt (EN) 값은 narrative 문장에 그대로 끼워 넣을 수 있도록 article 포함 noun phrase 형태로 저장된다. 슬롯 키는 `AUTO_VARIABLE_OPTIONS` dict 의 키와 1:1 매칭된다.

#### `eye_spacing` — 눈 사이 거리

| 한국어 라벨   | Prompt (EN)             | 해석 (KR)                              |
| ------------- | ----------------------- | -------------------------------------- |
| 좁은 눈 사이  | slightly close-set eyes | 두 눈 사이가 살짝 좁음                 |
| 표준 눈 사이  | balanced eye spacing    | 두 눈 사이가 균형 잡힘                 |
| 넓은 눈 사이  | slightly wide-set eyes  | 두 눈 사이가 살짝 넓음                 |

#### `eye_opening` — 눈 크기·열림

| 한국어 라벨 | Prompt (EN)                  | 해석 (KR)                |
| ----------- | ---------------------------- | ------------------------ |
| 좁게 뜬 눈  | a narrow eye opening         | 눈을 살짝 좁게 뜸        |
| 보통 눈     | a medium eye opening         | 표준 크기로 뜬 눈        |
| 동그란 눈   | a slightly round eye opening | 살짝 동그랗게 뜬 눈      |

#### `brow_shape` — 눈썹 모양

| 한국어 라벨        | Prompt (EN)              | 해석 (KR)                                 |
| ------------------ | ------------------------ | ----------------------------------------- |
| 일자 눈썹          | a straight brow          | 곡선 없이 평평한 눈썹                     |
| 부드러운 아치 눈썹 | a softly arched brow     | 완만하게 휘어진 아치형 눈썹               |
| 살짝 각진 눈썹     | a slightly angled brow   | 가운데 부분에 살짝 각이 들어간 눈썹       |

#### `brow_pos` — 눈썹 높이

| 한국어 라벨 | Prompt (EN)             | 해석 (KR)                       |
| ----------- | ----------------------- | ------------------------------- |
| 낮은 눈썹   | a lower brow position   | 눈과 가까운 낮은 위치           |
| 높은 눈썹   | a higher brow position  | 눈에서 떨어진 높은 위치         |

#### `nose_tip` — 코끝 모양

| 한국어 라벨        | Prompt (EN)               | 해석 (KR)                            |
| ------------------ | ------------------------- | ------------------------------------ |
| 작고 둥근 코끝     | a small rounded nose tip  | 코끝이 작고 둥글게 마무리됨          |
| 작고 날렵한 코끝   | a small sharper nose tip  | 코끝이 작고 살짝 날카롭게 마무리됨   |
| 작고 부드러운 코끝 | a small soft nose tip     | 코끝이 작고 부드럽게 마무리됨        |

#### `lip_shape` — 입술 라인

| 한국어 라벨         | Prompt (EN)        | 해석 (KR)                                                          |
| ------------------- | ------------------ | ------------------------------------------------------------------ |
| 부드러운 큐피드활   | a soft cupid's bow | 윗입술 가운데 큐피드활(M자) 모양이 부드럽게 잡힘                  |
| 부드러운 입술 라인  | a soft lip line    | 입술 윤곽선이 자연스럽고 부드럽게 흐름                            |

#### `mouth_width` — 입 너비

| 한국어 라벨   | Prompt (EN)             | 해석 (KR)                          |
| ------------- | ----------------------- | ---------------------------------- |
| 살짝 넓은 입  | a slightly wider mouth  | 입의 가로 폭이 살짝 넓음           |
| 작은 입       | a compact mouth         | 입의 가로 폭이 컴팩트함            |

#### `chin_length` — 턱 길이

| 한국어 라벨 | Prompt (EN)        | 해석 (KR)                   |
| ----------- | ------------------ | --------------------------- |
| 짧은 턱     | a shorter chin     | 턱 길이가 짧음              |
| 표준 턱     | a balanced chin    | 턱 길이가 표준 비율로 균형  |

#### `chin_width` — 턱 너비

| 한국어 라벨    | Prompt (EN)               | 해석 (KR)                |
| -------------- | ------------------------- | ------------------------ |
| 좁은 턱        | a narrow chin             | 턱 너비가 좁음           |
| 살짝 넓은 턱   | a slightly broader chin   | 턱 너비가 살짝 넓음      |

#### `midface` — 중안부 길이 비율

| 한국어 라벨   | Prompt (EN)         | 해석 (KR)                                  |
| ------------- | ------------------- | ------------------------------------------ |
| 짧은 중안부   | a shorter midface   | 중안부 길이가 짧아 동안 비율에 가까움      |
| 균형 중안부   | a balanced midface  | 중안부가 표준 비율로 균형 잡힘             |

### 6.2 출력 형식

5.2 의 마지막 문장에 그대로 inline 으로 합류한다.

```
Subtle micro features include {eye_spacing} with {eye_opening}, {brow_shape} at {brow_pos}, {nose_tip}, {lip_shape} with {mouth_width}, {chin_length} with {chin_width}, and {midface}.
```

예시 (random.seed(42)):

```
Subtle micro features include slightly wide-set eyes with a narrow eye opening, a straight brow at a higher brow position, a small rounded nose tip, a soft cupid's bow with a slightly wider mouth, a shorter chin with a narrow chin, and a balanced midface.
```

---

## 7. 코드 적용 원칙

- prompt asset, context builder, snapshot 저장값은 이 문서의 stable key를 기준으로 맞춘다.
- 한국어 라벨은 별도 필드 또는 문서/UI에서만 사용한다.
- 실제 모델 입력 프롬프트는 `Prompt (EN)` 열을 기준으로 관리한다.
- key가 문서 기준으로 안정화되면 per-axis `str, Enum`으로 승격한다.
- `gender_key`에 따라 `hair_style_key`가 참조하는 dict가 달라지므로, API 입력 검증에서 `(gender_key, hair_style_key)` 페어를 함께 검증한다.
- 자동 가변 슬롯(6장)은 사용자 입력에 노출하지 않는다. 서버 내부 결정으로만 사용한다.

---

## 8. 컨텍스트 선택 정책

> 컴패니언 프로필은 photocard와 달리 "타입별 랜덤 조합형"이 아니라 "사용자가 8개 축을 모두 선택"하는 구조다. 다이버시티는 자동 가변 슬롯(6장)에서만 부여된다.

### 8.1 입력 정책

| 항목                | 정책                                                                                                                                                       |
| ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 사용자 입력 축      | `gender`, `ethnicity`, `mood`, `eye_color`, `face_shape`, `hair_color`, `hair_style`, `skin_detail` 8개                                          |
| 모든 축 필수        | 8개 축 모두 stable key가 입력되어야 한다. 빈 값/None은 허용하지 않는다.                                                                                    |
| `hair_style` 분기   | `gender_key`에 따라 4.7(MALE) 또는 4.8(FEMALE) 표를 사용한다. 잘못된 페어는 `ValueError`로 거절한다 (`resolve_option_text`).                               |

### 8.2 자동 가변 정책

| 항목       | 정책                                                                                                                          |
| ---------- | ----------------------------------------------------------------------------------------------------------------------------- |
| 생성 시점  | 매 prompt 빌드 시 1회 새로 샘플링 (`_roll_auto_variables`).                                                                   |
| 분포       | 슬롯별 선택지에서 균등 랜덤 1개.                                                                                              |
| 노출 여부  | 사용자/UI에 노출하지 않는다. 디버깅이나 재현이 필요하면 빌드 직후 snapshot으로만 보존한다.                                    |

### 8.3 빌드 규칙

1. `CompanionProfilePromptContext`로 8개 stable key를 받는다.
2. 각 축의 prompt 텍스트를 `resolve_option_text`로 해석한다 (잘못된 key는 `ValueError`).
3. `hair_color` (색 형용사) 와 `hair_style` 을 공백으로 결합해 헤어 문구를 만든다.
4. 자동 가변 슬롯을 균등 랜덤 샘플링한 뒤 5.2 의 마지막 문장에 그대로 끼워 넣는다.
5. 5.2 의 5개 문장으로 Subject 문단을 조립한다.
6. `[GENRE] → [Subject 문단] → [QUALITY 두 문단]` 순서로 `compose_prompt`를 호출해 최종 prompt를 빌드한다.
