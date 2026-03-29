# 콘텐츠 프롬프트 옵션 키 가이드

> 목적: photocard/content prompt option key의 최종 stable 형식과 각 key에 대응하는 프롬프트 문구를 정의한다.
> 범위: `daily`, `finger_heart`, `school_life`
> 원칙: 이 문서에는 앞으로 사용할 stable key와 프롬프트만 적는다.

---

## 1. 공통 규칙

- key는 영어 `lower_snake_case`를 사용한다.
- key는 UI 문구가 아니라 내부 식별자다.
- key는 가능한 한 한 축의 의미만 담는다.
- 한국어 라벨은 문서/UI용이고, 저장 및 코드 식별에는 stable key를 사용한다.
- key는 컨셉 범위 내에서 고유하며, 같은 key명이라도 컨셉이 다르면 프롬프트가 다를 수 있다

### 축 정의

| 축           | 의미                                | 네이밍 원칙                    |
| ------------ | ----------------------------------- | ------------------------------ |
| `scene`      | 장소 또는 장소 중심 scenario preset | 위치 중심 명명                 |
| `gaze`       | 시선 방향                           | 감정 표현 없이 방향 중심 명명  |
| `expression` | 표정/감정                           | 시선이나 구도 의미를 넣지 않음 |
| `outfit`     | 의상 archetype                      | 스타일 핵심만 식별             |
| `camera`     | 구도/앵글                           | shot size와 angle 중심 명명    |
| `atmosphere` | 조명/질감/무드 preset               | 조명 톤 중심, mood는 보조 정보 |

---

## 2. 상위 개념

### API / DB concept enum

| key            | 한국어      |
| -------------- | ----------- |
| `DAILY`        | 일상 스냅   |
| `FINGER_HEART` | 손가락 하트 |
| `SCHOOL_LIFE`  | 학교 생활   |

### prompt module key

| key            | 한국어      |
| -------------- | ----------- |
| `daily`        | 일상 스냅   |
| `finger_heart` | 손가락 하트 |
| `school_life`  | 학교 생활   |

---

## 3. 고정 프롬프트

> `Prompt (EN)`은 런타임 프롬프트의 문장 순서를 그대로 적었고, 코드에서는 줄바꿈 문자열로 관리한다.

### 공통 base prompt

| stable key        | 한국어 라벨        | Prompt (EN)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | 해석 (KR)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | 적용 범위 |
| ----------------- | ------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------- |
| `identity_lock`   | 인물 동일성 고정   | Keep the person's facial features exactly the same as the reference image.<br>This is the same person, not a look-alike or approximation.<br>Preserve the same skin tone and facial structure. Skin should look natural and smooth.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | 레퍼런스 이미지와 얼굴 특징이 정확히 같아야 한다.<br>닮은 사람이 아니라 동일 인물이어야 한다.<br>같은 피부 톤과 얼굴 골격을 유지하고, 피부는 자연스럽고 매끈하게 보여야 한다.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | 전체 공통 |
| `constraint_lock` | 해부학/프레임 제약 | Maintain natural, anatomically correct body proportions.<br>The head must not appear oversized relative to the shoulders and torso.<br>Frame the shot so the upper body including chest and shoulders is visible.<br>Prioritize natural human scale over stylized or exaggerated proportions.<br>Both eyes must be anatomically correct and natural-looking -- symmetrical eye shape, proper iris placement, natural eyelid coverage, and consistent pupil size. Both eyes must have the exact same iris color as the reference image. No crossed eyes, misaligned irises, distorted eye shapes, or heterochromia.<br>Both arms must be fully visible and anatomically complete -- no missing, truncated, or merged limbs. Each arm should have a natural, clearly separated form from shoulder to hand.<br>Each hand must have exactly five fingers with correct hand anatomy -- proper thumb placement, natural finger joints, and proportional hand size relative to the body. No extra digits, no fused fingers, no duplicate hands.<br>Do not place shelves, furniture, or any objects immediately next to the subject that obstruct or clutter the frame edges. | 자연스럽고 해부학적으로 올바른 신체 비율을 유지한다.<br>머리가 어깨와 몸통에 비해 과하게 크게 보이면 안 된다.<br>가슴과 어깨를 포함한 상반신이 보이도록 프레임을 잡는다.<br>스타일화되거나 과장된 비율보다 자연스러운 사람 스케일을 우선한다.<br>양쪽 눈은 해부학적으로 자연스럽고 정확해야 하며, 눈 모양은 대칭이고 홍채 위치와 눈꺼풀 덮임, 동공 크기가 일관되어야 한다. 양쪽 눈의 홍채 색은 레퍼런스 이미지와 정확히 같아야 한다. 사시, 어긋난 홍채, 찌그러진 눈 모양, 오드아이를 허용하지 않는다.<br>양팔은 완전히 보여야 하고 해부학적으로 완전해야 한다. 팔이 사라지거나 잘리거나 합쳐지면 안 되며, 각 팔은 어깨부터 손까지 자연스럽고 분리된 형태여야 한다.<br>각 손은 정확히 다섯 손가락을 가져야 하며, 엄지 위치와 관절 구조, 몸 대비 손 크기가 자연스러워야 한다. 추가 손가락, 붙은 손가락, 중복된 손을 허용하지 않는다.<br>선반, 가구, 기타 물체를 피사체 바로 옆 프레임 가장자리에 두어 화면을 막거나 복잡하게 만들지 않는다. | 전체 공통 |

### 컨셉 guide prompt

| stable key                   | 한국어 라벨             | Prompt (EN)                                                                                                                                                                                             | 해석 (KR)                                                                                                                                                                                        | 적용 범위      |
| ---------------------------- | ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------- |
| `daily_concept_guide`        | 일상 스냅 컨셉 가이드   | Create a candid daily-life photocard.<br>The image should feel casually captured on a smartphone, not like a posed studio portrait.<br>Prioritize believable everyday atmosphere over dramatic styling. | 자연스러운 일상 포토카드를 생성한다.<br>연출된 스튜디오 인물사진이 아니라 스마트폰으로 가볍게 찍은 듯한 느낌이어야 한다.<br>극적인 스타일링보다 설득력 있는 일상 분위기를 우선한다.              | `daily`        |
| `finger_heart_concept_guide` | 손가락 하트 컨셉 가이드 | Create an idol-style finger-heart photocard.<br>Show exactly one natural Korean finger heart gesture near the cheek.<br>The pose should feel shy and casual, not exaggerated or overly staged.          | 아이돌 스타일의 손가락 하트 포토카드를 생성한다.<br>볼 근처에 자연스러운 한국식 손가락 하트를 정확히 하나만 보여준다.<br>포즈는 과장되거나 지나치게 연출되지 않고 수줍고 캐주얼하게 보여야 한다. | `finger_heart` |
| `school_life_concept_guide`  | 학교 생활 컨셉 가이드   | Create a school-life photocard.<br>The image should feel like a candid break-time snapshot taken around school.<br>Keep the mood youthful, natural, and grounded rather than theatrical.                | 학교 생활 포토카드를 생성한다.<br>학교 주변에서 쉬는 시간에 자연스럽게 찍은 스냅처럼 보여야 한다.<br>연극적인 느낌보다 젊고 자연스럽고 현실적인 분위기를 유지한다.                               | `school_life`  |

---

## 4. Daily

### Scene

| stable key          | 한국어 라벨 | Prompt (EN)                                                                                                                                                                                                                                                                                                                                                                     | 해석 (KR)                                                                                                                                                                                                                                                                            |
| ------------------- | ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `convenience_store` | 편의점      | Holding a cold iced coffee with a straw in one hand, about to take a sip inside a convenience store at night. Fluorescent tubes on the ceiling cast even light across the space. The background is softly blurred with no prominent shelves or objects directly beside the subject.                                                                                             | 밤의 편의점 안에서 한 손에 아이스커피를 들고 빨대를 입에 가져가려는 순간. 천장 형광등이 공간 전체를 고르게 비추고, 배경은 부드럽게 흐려져 있으며 피사체 바로 옆에는 선반이나 물건이 두드러지지 않음.                                                                                 |
| `parking_lot`       | 지하 주차장 | Leaning back against a concrete pillar with weight on one leg, hands stuffed in pockets, standing in an underground parking lot. Concrete walls and exposed ceiling pipes in the background, with a nearby overhead light casting enough light to clearly illuminate the face.                                                                                                  | 지하 주차장에서 한쪽 다리에 무게를 싣고 콘크리트 기둥에 기대 선 자세. 손은 주머니에 넣고 있으며, 배경에는 콘크리트 벽과 노출 배관이 보이고 가까운 조명이 얼굴을 충분히 밝혀 줌.                                                                                                      |
| `bedroom`           | 침실        | Sitting on the bed or floor next to the bed, holding an iced coffee or absentmindedly scrolling a phone in a lived-in bedroom. K-pop posters and magazine cutouts cover the wall behind, clothes are casually scattered on the bed and floor. A ceiling light fills the room with moderate warm-white indoor light — the face and room are clearly visible but not overexposed. | 생활감 있는 침실에서 침대 위나 침대 옆 바닥에 앉아 아이스커피를 들고 있거나 멍하니 휴대폰을 스크롤하는 장면. 뒤 벽에는 K-pop 포스터와 잡지 스크랩이 붙어 있고, 침대와 바닥에는 옷이 자연스럽게 흩어져 있음. 천장등의 따뜻한 실내 조명으로 얼굴과 방이 분명히 보이되 과노출되지 않음. |

### Gaze

| stable key              | 한국어 라벨 | Prompt (EN)                                                                                                                                                 | 해석 (KR)                                                                                                         |
| ----------------------- | ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| `look_left_off_camera`  | 왼쪽 흘깃   | Both eyes looking in the same direction, glancing slightly to the left of the camera with a natural, composed expression. Not looking at the camera at all. | 양쪽 눈이 같은 방향으로 정렬된 채 카메라 왼쪽 바깥을 살짝 바라봄. 카메라는 전혀 보지 않고 자연스럽고 차분한 시선. |
| `look_right_off_camera` | 오른쪽 시선 | Staring blankly at something to the right, not looking at the camera at all — eyes clearly aimed away from the lens.                                        | 오른쪽 어딘가를 멍하니 바라보며 카메라는 전혀 보지 않는 상태. 시선은 분명히 렌즈 바깥을 향함.                     |

### Expression

| stable key   | 한국어 라벨   | Prompt (EN)                                                                                      | 해석 (KR)                                                                                                 |
| ------------ | ------------- | ------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------- |
| `neutral`    | 무표정        | Calm, resting face with lips gently closed and no tension anywhere.                              | 입술을 가볍게 다문 편안한 무표정. 얼굴 어디에도 힘이 들어가지 않은 상태.                                  |
| `tired`      | 피곤한 표정   | Slightly tired eyes with a calm, unbothered expression — not sleepy, just at ease late at night. | 살짝 피곤한 눈빛이지만 거슬리는 느낌 없이 차분한 표정. 졸린 것이 아니라 늦은 밤의 느슨한 편안함에 가까움. |
| `soft_smile` | 부드러운 미소 | A soft, natural smile — gentle and subtle, both corners of the mouth lifted just slightly.       | 양쪽 입꼬리가 아주 살짝 올라간 자연스럽고 부드러운 미소.                                                  |
| `vacant`     | 멍한 표정     | Completely empty expression, face showing nothing, as if the mind is somewhere else entirely.    | 얼굴에 아무 감정도 드러나지 않고, 생각이 완전히 다른 데 가 있는 듯한 텅 빈 표정.                          |
| `curious`    | 궁금한 표정   | One eyebrow slightly raised, a random thought suddenly crossing the mind.                        | 한쪽 눈썹이 아주 살짝 올라가며 문득 궁금한 생각이 스친 듯한 표정.                                         |

### Outfit

| stable key              | 한국어 라벨      | Prompt (EN)                                                                                                    | 해석 (KR)                                                                                     |
| ----------------------- | ---------------- | -------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| `oversized_graphic_tee` | 오버핏 그래픽 티 | Faded oversized graphic t-shirt with a barely visible washed-out print, paired with loose wrinkled sweatpants. | 흐릿하게 바랜 프린트가 들어간 오버사이즈 그래픽 티셔츠와 구김 있는 루즈한 스웨트팬츠.         |
| `washed_black_tee`      | 워시드 블랙 티   | Washed black oversized t-shirt with slightly stretched neckline, paired with wide-leg denim jeans.             | 목선이 살짝 늘어난 워시드 블랙 오버사이즈 티셔츠와 와이드 데님 진.                            |
| `hoodie_layered_tee`    | 후디 레이어드    | Unzipped hoodie layered over a plain white t-shirt, with loose relaxed-fit pants.                              | 기본 흰 티셔츠 위에 지퍼를 열어둔 후디를 레이어드하고, 루즈한 릴랙스 핏 팬츠를 매치한 스타일. |
| `chunky_knit_sweater`   | 청키 니트        | Oversized chunky knit sweater with dropped shoulders, paired with relaxed straight-leg pants.                  | 드롭 숄더의 오버사이즈 청키 니트 스웨터와 편안한 스트레이트 핏 팬츠.                          |

### Camera

| stable key        | 한국어 라벨   | Prompt (EN)                                                                                     | 해석 (KR)                                                                              |
| ----------------- | ------------- | ----------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| `eye_level`       | 눈높이        | Eye-level shot, slightly off-center framing with the subject not perfectly centered.            | 피사체를 정가운데 두지 않은 약간 비대칭의 눈높이 샷.                                   |
| `low_angle`       | 로우 앵글     | Slightly low angle, camera tilted up just a few degrees from below chin level.                  | 턱 아래보다 약간 낮은 위치에서 몇 도 올려다본 로우 앵글 샷.                            |
| `high_angle`      | 하이 앵글     | Slightly high angle, camera looking down gently from above eye level.                           | 눈높이보다 약간 위에서 부드럽게 내려다본 하이 앵글 샷.                                 |
| `cropped_closeup` | 크롭 클로즈업 | Close-up with partial face cropping, cutting off the top of the head.                           | 머리 윗부분이 일부 잘린 얼굴 중심 클로즈업 샷.                                         |
| `medium_wide`     | 미디엄 와이드 | Medium shot with generous empty space on one side, subject occupying only a third of the frame. | 화면 한쪽에 넉넉한 여백이 있고 피사체가 프레임의 1/3 정도만 차지하는 미디엄 와이드 샷. |
| `side_profile`    | 사이드 프로필 | Shot from the side, showing the subject almost in profile so only one eye is visible.           | 거의 측면에 가까운 각도에서 촬영되어 한쪽 눈만 보이는 사이드 프로필 샷.                |

### Atmosphere

| stable key          | 한국어 라벨 | Prompt (EN)                                                                                                                                                                                                                                                           | 해석 (KR)                                                                                                                                                                                        |
| ------------------- | ----------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `candid_snapshot`   | 캔디드 스냅 | Candid snapshot aesthetic, as if a friend casually took this photo on an iPhone without warning. No posing, no preparation. The subject looks like they were caught mid-moment in their everyday life, completely absorbed in what they were doing.                   | 친구가 갑자기 아이폰으로 찍은 듯한 캔디드 스냅 질감. 포즈를 잡지 않았고 준비되지 않은 일상 한순간이 포착된 느낌.                                                                                 |
| `warm_indoor_light` | 실내 조명   | Moderate indoor lighting from a ceiling light — warm-white tone, not too bright and not too dim. The face is clearly visible with natural soft shadows on one side. The overall look is like a typical room photographed on a smartphone at night with the lights on. | 너무 밝지도 어둡지도 않은 따뜻한 실내 천장등 조명. 얼굴은 선명히 보이고 한쪽에 부드러운 그림자가 생기며, 밤에 방 안을 스마트폰으로 찍은 자연스러운 느낌.                                         |
| `lo_fi_snapshot`    | 로파이 스냅 | Slight motion blur on the hands or edges as if the photographer's hand shifted during capture. Faint digital noise consistent with a smartphone camera. Imperfect framing: slightly tilted horizon, minor lens distortion at edges, not perfectly composed.           | 촬영 순간 손떨림이 생긴 듯 손이나 가장자리에 약한 모션 블러가 있고, 스마트폰 카메라 특유의 옅은 디지털 노이즈가 느껴짐. 수평이 약간 기울고 가장자리에 미세한 왜곡이 있는 완벽하지 않은 프레이밍. |
| `quiet_late_night`  | 고요한 심야 | A calm, quiet atmosphere. The subject is the only person in the frame, surrounded by empty space.                                                                                                                                                                     | 차분하고 고요한 분위기. 화면 안에는 인물이 혼자 있고 주변에는 여백이 감도는 느낌.                                                                                                                |

---

## 5. Finger Heart

### Scene

| stable key      | 한국어 라벨 | Prompt (EN)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | 해석 (KR)                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| --------------- | ----------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `practice_room` | 연습실      | K-pop practice room with wooden floor. Speakers or studio equipment visible in the background; slightly messy training environment. The mirror wall is off to the side, outside the camera frame or barely visible at the edge. The subject has exactly two arms and two hands, each hand with five distinct fingers. Only the right hand is raised near the cheek making a Korean finger heart — thumb tip and index finger tip gently touching to form a small heart shape, remaining three fingers curled naturally toward the palm. The left arm hangs relaxed at their side with the hand resting naturally against the thigh. No hand is touching the face or pressing against the cheek. Casual and a little shy, not exaggerated, as if someone snapped a quick photo during a break. | 나무 바닥이 있는 K-pop 연습실. 배경에는 스피커나 스튜디오 장비가 보이고, 약간 어수선한 연습 환경. 거울 벽은 카메라 프레임 밖이나 가장자리에서만 희미하게 보임. 인물은 정확히 두 팔과 두 손을 가지고 있고 각 손가락은 다섯 개가 분명히 보여야 함. 오른손만 볼 근처로 올라와 한국식 손가락 하트를 만들고, 왼팔은 허벅지 옆으로 자연스럽게 내려가 있음. 손이 얼굴을 누르지 않으며, 쉬는 시간에 누가 가볍게 찍은 듯한 수줍고 자연스러운 분위기. |

### Gaze

| stable key    | 한국어 라벨 | Prompt (EN)                                                                                                                      | 해석 (KR)                                                                                          |
| ------------- | ----------- | -------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| `look_down`   | 아래 시선   | looking almost straight ahead but with eyes tilted just a few degrees downward — irises should remain fully visible and centered | 거의 정면을 향하지만 시선만 몇 도 아래로 떨어진 상태. 홍채는 분명히 보이고 중심이 흐트러지지 않음. |
| `look_side`   | 옆 시선     | glancing to the side playfully                                                                                                   | 옆으로 장난스럽게 시선을 흘기는 상태.                                                              |
| `eye_contact` | 눈맞춤      | direct eye contact with the camera                                                                                               | 카메라를 정면으로 바라보는 눈맞춤.                                                                 |
| `look_up`     | 위 시선     | looking slightly upward with a soft, dreamy gaze                                                                                 | 위쪽을 향해 살짝 올려다보는 부드럽고 몽환적인 시선.                                                |

### Expression

| stable key     | 한국어 라벨      | Prompt (EN)                                 | 해석 (KR)                                   |
| -------------- | ---------------- | ------------------------------------------- | ------------------------------------------- |
| `gentle_smile` | 부드러운 미소    | soft, gentle smile                          | 잔잔하고 부드러운 미소.                     |
| `embarrassed`  | 수줍은 표정      | slightly embarrassed, lips pressed together | 입술을 살짝 다문 채 민망하고 부끄러운 표정. |
| `cheerful`     | 밝은 표정        | relaxed face with bright, cheerful eyes     | 편안한 얼굴과 밝고 생기 있는 눈빛.          |
| `playful_grin` | 장난기 있는 웃음 | playful grin with a hint of mischief        | 장난기와 약간의 짓궂음이 섞인 grin.         |

### Outfit

| stable key            | 한국어 라벨          | Prompt (EN)                                                                                                                                      | 해석 (KR)                                                                                                                               |
| --------------------- | -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------- |
| `varsity_jacket`      | 바시티 재킷          | Oversized varsity jacket with contrast sleeves, worn open over a simple crew-neck tee, paired with loose jogger pants and indoor training shoes. | 배색 소매가 들어간 오버사이즈 바시티 재킷을 심플한 크루넥 티 위에 오픈해 입고, 루즈한 조거 팬츠와 실내용 트레이닝 슈즈를 매치한 스타일. |
| `striped_rugby_shirt` | 스트라이프 럭비 셔츠 | Boxy striped rugby polo shirt with a wide collar, paired with relaxed-fit sweatpants and white crew socks.                                       | 넓은 칼라가 있는 박시한 스트라이프 럭비 폴로 셔츠와 릴랙스 핏 스웨트팬츠, 화이트 크루 삭스 조합.                                        |
| `sleeveless_casual`   | 민소매 캐주얼        | Simple sleeveless top in a neutral tone, paired with comfortable loose-fit shorts and indoor training shoes.                                     | 뉴트럴 톤의 심플한 민소매 상의와 편안한 루즈 핏 반바지, 실내용 트레이닝 슈즈 조합.                                                      |
| `training_hoodie`     | 트레이닝 후디        | Relaxed oversized hoodie in a soft tone, paired with straight-leg training pants and indoor training shoes.                                      | 부드러운 톤의 릴랙스 오버사이즈 후디와 스트레이트 핏 트레이닝 팬츠, 실내용 트레이닝 슈즈 조합.                                          |

### Camera

| stable key      | 한국어 라벨   | Prompt (EN)                                                                 | 해석 (KR)                                             |
| --------------- | ------------- | --------------------------------------------------------------------------- | ----------------------------------------------------- |
| `front_closeup` | 정면 클로즈업 | close-up with the face dominant and a slight crop                           | 얼굴 비중이 크고 약간 크롭된 정면 중심 클로즈업.      |
| `waist_up`      | 허리 위 샷    | waist-up shot showing the full upper body with some room around the subject | 허리 위까지 보이고 인물 주변에 약간의 공간이 남는 샷. |
| `medium_chest`  | 가슴 위 샷    | chest-up medium shot                                                        | 가슴 위까지 보이는 미디엄 샷.                         |
| `high_angle`    | 하이 앵글     | slight high-angle close shot                                                | 위에서 약간 내려다본 가까운 하이 앵글 샷.             |

### Atmosphere

| stable key             | 한국어 라벨        | Prompt (EN)                                                                                                                                                                                                                                                                                                                                                                 | 해석 (KR)                                                                                                                                                                                                          |
| ---------------------- | ------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `idol_casual_snapshot` | 아이돌 캐주얼 스냅 | Indoor fluorescent or soft studio lighting with slightly uneven exposure and soft shadows. Natural Korean Gen Z daily look — effortlessly stylish, no heavy styling. Light, shy, and playful idol-style moment. Slight softness from a smartphone camera; no harsh grain or excessive noise. The overall image should feel like a real casual moment captured on an iPhone. | 형광등이나 부드러운 스튜디오 조명 아래 노출이 약간 고르지 않고 그림자는 부드러운 상태. 꾸민 티가 과하지 않은 한국 Gen Z의 자연스러운 일상 스타일. 가볍고 수줍고 장난스러운 아이돌 순간이 스마트폰으로 포착된 느낌. |

---

## 6. School Life

### Scene

| stable key                      | 한국어 라벨    | Prompt (EN)                                                                                                         | 해석 (KR)                                                                           |
| ------------------------------- | -------------- | ------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| `classroom`                     | 교실           | Korean high school classroom during break time. The subject is sitting casually at the desk with a relaxed posture. | 쉬는 시간의 한국 고등학교 교실. 인물은 책상에 편안하게 앉아 자연스러운 자세를 취함. |
| `hallway`                       | 복도           | School hallway lined with windows. The subject is leaning lightly against the wall.                                 | 창문이 이어진 학교 복도. 인물은 벽에 가볍게 기대어 서 있음.                         |
| `stairway`                      | 계단           | Stairway inside a school building. The subject is sitting on the steps with elbows resting on the knees.            | 학교 건물 안 계단. 인물은 계단에 앉아 팔꿈치를 무릎에 자연스럽게 올리고 있음.       |
| `rooftop`                       | 옥상           | School rooftop. The subject is standing with weight shifted slightly to one side.                                   | 학교 옥상에서 한쪽으로 무게를 조금 실은 채 서 있는 자세.                            |
| `near_school_convenience_store` | 학교 앞 편의점 | Convenience store near school. The subject is holding a drink casually.                                             | 학교 근처 편의점에서 음료를 자연스럽게 들고 있는 장면.                              |

### Gaze

| stable key        | 한국어 라벨     | Prompt (EN)                                   | 해석 (KR)                                                     |
| ----------------- | --------------- | --------------------------------------------- | ------------------------------------------------------------- |
| `look_down`       | 아래 시선       | looking slightly down with a small smile      | 살짝 아래를 내려다보며 작은 미소를 띠는 상태.                 |
| `look_side`       | 옆 시선         | glancing to the side playfully                | 옆으로 장난스럽게 시선을 흘기는 상태.                         |
| `look_off_camera` | 카메라 밖 시선  | reacting to something off-camera              | 카메라 바깥 어딘가를 보고 반응하는 상태.                      |
| `look_away`       | 시선 회피       | looking away from the camera with a shy smile | 카메라를 피해서 다른 방향을 바라보며 수줍은 미소를 짓는 상태. |
| `eye_contact`     | 부드러운 눈맞춤 | soft eye contact with the camera              | 카메라와 부드럽게 눈을 맞추는 상태.                           |

### Expression

| stable key     | 한국어 라벨   | Prompt (EN)                   | 해석 (KR)                                    |
| -------------- | ------------- | ----------------------------- | -------------------------------------------- |
| `soft_smile`   | 부드러운 미소 | soft smile                    | 부드럽고 가벼운 미소.                        |
| `amused`       | 웃참 표정     | slightly amused expression    | 살짝 즐거워하며 웃음을 참는 듯한 표정.       |
| `shy_smile`    | 수줍은 미소   | shy smile                     | 부끄럽고 수줍은 미소.                        |
| `bright_eyed`  | 또렷한 눈빛   | relaxed face with bright eyes | 얼굴은 편안하지만 눈빛은 또렷하고 밝은 상태. |
| `subtle_laugh` | 은은한 웃음   | subtle laugh                  | 웃음기가 은은하게 번지는 표정.               |

### Outfit

| stable key               | 한국어 라벨          | Prompt (EN)                                                                                                                                                                                                       | 해석 (KR)                                                                                                                                                           |
| ------------------------ | -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `cardigan_uniform_shirt` | 카디건 + 교복 셔츠   | oversized long-sleeve cardigan over a school shirt, gray uniform pants, and a loosely worn tie                                                                                                                    | 교복 셔츠 위에 오버사이즈 긴소매 카디건을 걸치고, 회색 교복 바지와 느슨하게 맨 넥타이를 착용한 스타일.                                                              |
| `blazer_uniform_shirt`   | 블레이저 + 교복 셔츠 | school blazer over a school shirt, gray uniform pants, and a loosened tie                                                                                                                                         | 교복 셔츠 위 블레이저, 회색 교복 바지, 느슨하게 푼 넥타이 조합.                                                                                                     |
| `cardigan_casual_tee`    | 카디건 + 캐주얼 티   | oversized long-sleeve cardigan over an oversized short-sleeve t-shirt, uniform pants, and wired earphones hanging around the neck connected to a single phone held casually in one hand — the other hand is empty | 오버사이즈 반팔 티 위에 긴소매 카디건을 걸치고 교복 바지를 입은 스타일. 유선 이어폰이 목에 걸려 있고 한 손에는 휴대폰이 자연스럽게 들려 있으며 다른 손은 비어 있음. |
| `blazer_casual_tee`      | 블레이저 + 캐주얼 티 | school blazer over an oversized short-sleeve t-shirt, uniform pants, and wired earphones hanging around the neck connected to a single phone held casually in one hand — the other hand is empty                  | 오버사이즈 반팔 티 위에 블레이저를 걸치고 교복 바지를 입은 스타일. 유선 이어폰이 목에 걸려 있고 한 손에는 휴대폰이 자연스럽게 들려 있으며 다른 손은 비어 있음.      |

### Camera

| stable key          | 한국어 라벨   | Prompt (EN)                                       | 해석 (KR)                                 |
| ------------------- | ------------- | ------------------------------------------------- | ----------------------------------------- |
| `front_closeup`     | 정면 클로즈업 | close-up with the face dominant and a slight crop | 얼굴 중심의 약간 크롭된 정면 클로즈업.    |
| `angled_closeup`    | 사선 클로즈업 | close-up from a slight angle                      | 살짝 각도를 준 클로즈업 샷.               |
| `medium_chest`      | 가슴 위 샷    | chest-up medium shot                              | 가슴 위까지 보이는 미디엄 샷.             |
| `upper_body_medium` | 상반신 미디엄 | medium shot with the upper body visible           | 상반신이 보이는 미디엄 샷.                |
| `high_angle`        | 하이 앵글     | slight high-angle close shot                      | 위에서 살짝 내려다본 가까운 하이 앵글 샷. |
| `side_angle_medium` | 측면 미디엄   | slight side-angle medium shot                     | 측면 방향으로 각도를 준 미디엄 샷.        |

### Atmosphere

| stable key                 | 한국어 라벨         | Prompt (EN)                                                                                                                                                                                                                                        | 해석 (KR)                                                                                                                                                                                |
| -------------------------- | ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `daylight_playful_sticker` | 밝은 낮 + 스티커    | Bright natural daylight streaming through windows with clean, even exposure. A small sticker playfully placed on the cheek. Light, energetic, and cheerful mood — like a fun moment between classes. Clean smartphone-camera look.                 | 창문으로 들어오는 밝은 자연광이 고르게 비치고, 볼에 작은 스티커 포인트가 있는 상태. 수업 사이 장난스러운 순간 같은 밝고 경쾌한 분위기의 스마트폰 사진 느낌.                              |
| `fluorescent_calm_doodle`  | 형광등 + 낙서       | Flat indoor fluorescent lighting with a slightly cool tone and balanced shadows. A light doodle mark drawn on the back of the hand or wrist. Quiet, drowsy break-time atmosphere — calm and unhurried. Clean smartphone-camera look.               | 약간 차가운 형광등 실내 조명과 균형 잡힌 그림자. 손등이나 손목에 가벼운 낙서 포인트가 있고, 쉬는 시간의 조용하고 나른한 분위기.                                                          |
| `golden_hour_nostalgic`    | 골든아워 노스탤지어 | Warm golden afternoon light coming from behind, creating a soft backlit glow around the hair and shoulders. No playful details — just a natural, undecorated moment. Warm, sentimental, and slightly nostalgic mood. Clean smartphone-camera look. | 뒤에서 들어오는 따뜻한 골든아워 빛이 머리와 어깨 둘레에 부드러운 역광을 만들고, 장난스러운 장식 없이 자연스럽고 소박한 순간을 담음. 따뜻하고 감성적이며 약간 향수를 불러일으키는 분위기. |
| `overcast_relaxed`         | 흐린 날 편안함      | Overcast soft light with no harsh shadows, gentle and even across the face. Slightly messy or untucked uniform detail. Comfortable, laid-back atmosphere — like the end of a long school day. Clean smartphone-camera look.                        | 강한 그림자 없이 얼굴 전체에 부드럽고 고르게 퍼지는 흐린 날의 빛. 약간 흐트러진 교복 디테일과 함께 긴 하루가 끝나가는 듯한 편안하고 느슨한 분위기.                                       |

---

## 7. 코드 적용 원칙

- prompt asset, context builder, snapshot 저장값은 이 문서의 stable key를 기준으로 맞춘다.
- 한국어 라벨은 별도 필드 또는 문서/UI에서만 사용한다.
- 실제 모델 입력 프롬프트는 `Prompt (EN)` 열을 기준으로 관리한다.
- key가 문서 기준으로 안정화되면 per-axis `str, Enum`으로 승격한다.

---

## 8. 콘텐츠 컨텍스트 선택 정책

> 이 섹션은 구현 규칙이 아니라 기획 기준이다. 현재 기준은 "컨셉이 정해진 뒤, 각 타입에서 key 1개를 랜덤 선택해 최종 prompt를 빌드한다"이다.

### 8.1 공통 선택 원칙

| 항목       | 정책                                                                                                                                                              |
| ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1차 기준   | 먼저 `concept`를 결정한다.                                                                                                                                        |
| 랜덤 방식  | 선택 대상 타입마다 허용된 key 중 1개를 랜덤 선택한다.                                                                                                             |
| 타입 단위  | 기본 타입은 `scene`, `gaze`, `expression`, `outfit`, `camera`, `atmosphere`다.                                                                                    |
| scene 우선 | 일부 컨셉은 기획상 "장소를 먼저 정하고 행동을 맞춘다" 구조지만, 현재 stable key 체계에서는 행동이 scene prompt에 포함되어 있으므로 별도 action key는 두지 않는다. |
| 고정 타입  | 컨셉에 따라 특정 타입은 랜덤이 아니라 고정값일 수 있다.                                                                                                           |
| 가중치     | 현재 기획에는 타입별 가중치나 우선순위 랜덤은 없다. 허용된 key 집합에서 균등 랜덤을 기본으로 본다.                                                                |
| 조합 방식  | 특별한 금지 규칙이 없는 한, 각 타입은 독립적으로 1개씩 뽑아 조합한다.                                                                                             |
| 미래 확장  | 중복 회피, 최근 생성 제외, 가중치 부여 같은 운영 로직은 추후 별도 정책으로 추가할 수 있다.                                                                        |

### 8.2 컨셉별 랜덤 선택 규칙

| concept        | 랜덤 선택 타입                                                  | 고정 타입                                                | 비고                                  |
| -------------- | --------------------------------------------------------------- | -------------------------------------------------------- | ------------------------------------- |
| `daily`        | `scene`, `gaze`, `expression`, `outfit`, `camera`, `atmosphere` | 없음                                                     | 모든 타입에서 1개씩 랜덤 선택한다.    |
| `finger_heart` | `gaze`, `expression`, `outfit`, `camera`                        | `scene=practice_room`, `atmosphere=idol_casual_snapshot` | 기획상 연습실과 전체 무드는 고정이다. |
| `school_life`  | `scene`, `gaze`, `expression`, `outfit`, `camera`, `atmosphere` | 없음                                                     | 모든 타입에서 1개씩 랜덤 선택한다.    |

### 8.3 타입별 선택 단위

| 타입         | 선택 단위          |
| ------------ | ------------------ |
| `scene`      | 장소/상황 1개      |
| `gaze`       | 시선 1개           |
| `expression` | 표정 1개           |
| `outfit`     | 의상 1개           |
| `camera`     | 구도/앵글 1개      |
| `atmosphere` | 조명/질감/무드 1개 |

### 8.4 빌드 규칙

1. `concept`를 기준으로 허용된 타입 집합을 결정한다.
2. 각 타입에서 key 1개를 랜덤 선택한다.
3. 고정 타입이 있는 컨셉은 해당 값을 그대로 넣는다.
4. 선택된 key 조합으로 최종 prompt를 빌드한다.

### 8.5 현재 기획 해석 메모

- Daily와 School Life는 "타입별 랜덤 조합형" 컨셉으로 본다.
- Finger Heart는 "일부 타입 고정 + 일부 타입 랜덤" 구조로 본다.
- scene에 연결된 행동 의미는 현재 prompt asset 안에 포함되어 있으므로, 런타임 context에서 action 타입을 따로 분리하지 않는다.
- 따라서 현재 context 정책의 핵심은 "타입마다 key 1개 선택"이지, "우선순위 기반 수동 선택"이 아니다.
