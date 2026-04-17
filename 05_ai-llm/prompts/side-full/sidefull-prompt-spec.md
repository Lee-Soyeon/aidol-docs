# 측면/전신 프롬프트 옵션 키 가이드

> 목적: side-full prompt option key의 최종 stable 형식과 각 key에 대응하는 프롬프트 문구를 정의한다.
> 범위: `side_profile`, `full_body`
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
| `scene`      | 촬영 구도/포즈 설정                 | 포즈 또는 각도 중심 명명       |
| `gaze`       | 시선 방향                           | 감정 표현 없이 방향 중심 명명  |
| `expression` | 표정/감정                           | 시선이나 구도 의미를 넣지 않음 |
| `outfit`     | 의상 archetype                      | 스타일 핵심만 식별             |
| `camera`     | 구도/앵글                           | shot size와 angle 중심 명명    |
| `atmosphere` | 조명/질감/무드 preset               | 조명 톤 중심, mood는 보조 정보 |

---

## 2. 상위 개념

### API / DB concept enum

| key            | 한국어           |
| -------------- | ---------------- |
| `SIDE_PROFILE` | 측면 프로필      |
| `FULL_BODY`    | 전신 스튜디오    |

### prompt module key

| key            | 한국어           |
| -------------- | ---------------- |
| `side`         | 측면 프로필      |
| `full_body`    | 전신 스튜디오    |

---

## 3. 고정 프롬프트

> `Prompt (EN)`은 런타임 프롬프트의 문장 순서를 그대로 적었고, 코드에서는 줄바꿈 문자열로 관리한다.

### 공통 base prompt

| stable key        | 한국어 라벨        | Prompt (EN) | 해석 (KR) | 적용 범위 |
| ----------------- | ------------------ | ----------- | --------- | --------- |
| `identity_lock`   | 인물 동일성 고정   | Keep the person's facial features exactly the same as the reference image.<br>This is the same person, not a look-alike or approximation.<br>Preserve the same skin tone and facial structure. Skin should look natural and smooth. | 레퍼런스 이미지와 얼굴 특징이 정확히 같아야 한다.<br>닮은 사람이 아니라 동일 인물이어야 한다.<br>같은 피부 톤과 얼굴 골격을 유지하고, 피부는 자연스럽고 매끈하게 보여야 한다. | 전체 공통 |
| `constraint_lock` | 해부학/프레임 제약 | Maintain natural, anatomically correct body proportions.<br>The head must not appear oversized relative to the shoulders and torso.<br>Prioritize natural human scale over stylized or exaggerated proportions.<br>Both eyes must be anatomically correct and natural-looking -- symmetrical eye shape, proper iris placement, natural eyelid coverage, and consistent pupil size. Both eyes must have the exact same iris color as the reference image. No crossed eyes, misaligned irises, distorted eye shapes, or heterochromia.<br>Both arms must be fully visible and anatomically complete -- no missing, truncated, or merged limbs. Each arm should have a natural, clearly separated form from shoulder to hand.<br>Each hand must have exactly five fingers with correct hand anatomy -- proper thumb placement, natural finger joints, and proportional hand size relative to the body. No extra digits, no fused fingers, no duplicate hands.<br>The subject must be the only person in the frame -- no other people, silhouettes, or partial figures visible in the background.<br>Both feet must appear grounded on a solid surface -- no floating, hovering, or ambiguous foot placement.<br>Do not place shelves, furniture, or any objects immediately next to the subject that obstruct or clutter the frame edges. | 자연스럽고 해부학적으로 올바른 신체 비율을 유지한다.<br>머리가 어깨와 몸통에 비해 과하게 크게 보이면 안 된다.<br>스타일화되거나 과장된 비율보다 자연스러운 사람 스케일을 우선한다.<br>양쪽 눈은 해부학적으로 자연스럽고 정확해야 한다. 사시, 어긋난 홍채, 찌그러진 눈 모양, 오드아이를 허용하지 않는다.<br>양팔은 완전히 보여야 하고 해부학적으로 완전해야 한다.<br>각 손은 정확히 다섯 손가락을 가져야 한다.<br>프레임 안에는 피사체 한 명만 있어야 한다.<br>양발은 단단한 표면 위에 접지해야 한다.<br>프레임 가장자리에 물체를 두어 화면을 막지 않는다. | 전체 공통 |

### 컨셉 guide prompt

| stable key                    | 한국어 라벨              | Prompt (EN) | 해석 (KR) | 적용 범위      |
| ----------------------------- | ------------------------ | ----------- | --------- | -------------- |
| `side_profile_concept_guide`  | 측면 프로필 컨셉 가이드  | Create a high-end editorial side-profile close-up studio portrait.<br>The face must dominate the frame -- tight crop on head, neck, and top of shoulders only.<br>Do NOT show the chest, arms, or hands. Emphasize the subject's facial silhouette, jawline, and nose bridge with precise studio lighting.<br>Maintain natural, anatomically correct facial proportions.<br>The head must not appear oversized relative to the neck and shoulders.<br>Both eyes must be anatomically correct and natural-looking -- symmetrical eye shape, proper iris placement, natural eyelid coverage, and consistent pupil size. Both eyes must have the exact same iris color as the reference image. No crossed eyes, misaligned irises, distorted eye shapes, or heterochromia.<br>The subject must be the only person in the frame -- no other people, silhouettes, or partial figures visible in the background.<br>Do not place shelves, furniture, or any objects immediately next to the subject that obstruct or clutter the frame edges. | 하이엔드 에디토리얼 측면 프로필 클로즈업 스튜디오 인물사진을 생성한다.<br>얼굴이 프레임을 지배해야 한다 -- 머리, 목, 어깨 상단만 타이트하게 크롭한다.<br>가슴, 팔, 손은 보여주지 않는다. 정밀한 스튜디오 조명으로 안면 실루엣, 턱선, 콧대를 강조한다.<br>자연스럽고 해부학적으로 정확한 얼굴 비율을 유지한다. | `side_profile` |
| `full_body_concept_guide`     | 전신 스튜디오 컨셉 가이드 | Create a high-end editorial full-body studio portrait.<br>The image should capture the subject's entire body from head to toe in a clean studio setting,<br>emphasizing natural proportions and relaxed posture. | 하이엔드 에디토리얼 전신 스튜디오 인물사진을 생성한다.<br>깔끔한 스튜디오 환경에서 머리부터 발끝까지 피사체의 전신을 담아야 하며, 자연스러운 비율과 편안한 자세를 강조한다. | `full_body` |

---

## 4. Side Profile

### Scene

| stable key            | 한국어 라벨      | Prompt (EN) | 해석 (KR) |
| --------------------- | ---------------- | ----------- | --------- |
| `profile_right`       | 우측 프로필      | A captivating close-up studio portrait of a young Korean idol with naturally balanced proportions typical of an idol trainee. Presented in a crisp right-side profile, expertly positioned to accentuate the elegant sweep of the nose bridge, the sharply defined jawline, and a strong facial silhouette against a plain seamless studio background. Head held naturally upright, neck and jawline visible. Tightly cropped to head and neck only -- no chest, arms, or hands visible. | 아이돌 연습생 특유의 자연스럽게 균형 잡힌 비율을 가진 한국 아이돌의 매력적인 클로즈업 스튜디오 인물사진. 깨끗한 우측 프로필로 콧대, 턱선, 얼굴 실루엣을 강조. 머리와 목만 타이트하게 크롭. |
| `profile_left`        | 좌측 프로필      | A captivating close-up studio portrait of a young Korean idol with naturally balanced proportions typical of an idol trainee. Presented in a crisp left-side profile, expertly positioned to accentuate the elegant sweep of the nose bridge, the sharply defined jawline, and a strong facial silhouette against a plain seamless studio background. Head held naturally upright, neck and jawline visible. Tightly cropped to head and neck only -- no chest, arms, or hands visible. | 좌측 프로필로 촬영한 것 외에 `profile_right`와 동일. |
| `three_quarter_right` | 우측 쓰리쿼터    | A close-up studio portrait showcasing a young Korean idol with naturally balanced proportions typical of an idol trainee, in a distinct three-quarter profile view angled approximately 45 degrees to the right. Prominent facial features -- a perfectly defined nose bridge and a strong jawline -- rendered with exceptional detail, creating a sharply outlined silhouette against a plain seamless studio background. Both eyes partially visible, natural head position. Tightly cropped to head and neck only -- no chest, arms, or hands visible. | 오른쪽으로 약 45도 각도의 쓰리쿼터 프로필 뷰. 콧대와 턱선이 디테일하게 묘사되며 양쪽 눈이 부분적으로 보임. 머리와 목만 타이트하게 크롭. |
| `three_quarter_left`  | 좌측 쓰리쿼터    | A close-up studio portrait showcasing a young Korean idol with naturally balanced proportions typical of an idol trainee, in a distinct three-quarter profile view angled approximately 45 degrees to the left. Prominent facial features -- a perfectly defined nose bridge and a strong jawline -- rendered with exceptional detail, creating a sharply outlined silhouette against a plain seamless studio background. Both eyes partially visible, natural head position. Tightly cropped to head and neck only -- no chest, arms, or hands visible. | 왼쪽으로 약 45도 각도의 쓰리쿼터 프로필 뷰. 그 외 `three_quarter_right`와 동일. |

### Gaze

| stable key            | 한국어 라벨    | Prompt (EN) | 해석 (KR) |
| --------------------- | -------------- | ----------- | --------- |
| `forward_past_camera` | 정면 먼 시선   | Eyes looking straight ahead past the camera, not engaging the lens -- gazing into the distance in the direction the face is turned. | 카메라를 지나쳐 정면 먼 곳을 바라보는 시선. 렌즈와 눈을 맞추지 않고 얼굴이 향한 방향으로 먼 곳을 응시. |
| `slight_down`         | 아래 시선      | Eyes directed slightly downward, as if looking at something below eye level. Calm and unfocused. | 눈높이보다 약간 아래를 내려다보는 차분하고 초점 없는 시선. |
| `over_shoulder`       | 어깨너머 시선  | Head turned to profile but eyes glancing back toward the camera over the shoulder -- a subtle look-back moment. | 고개는 프로필 방향이지만 눈은 어깨 너머로 카메라를 향해 돌아보는 미묘한 순간. |
| `upward`              | 위 시선        | Eyes gazing gently upward, as if looking at something above -- a light, airy, open expression. | 위를 부드럽게 올려다보는 시선. 가볍고 열린 느낌의 표정. |
| `closed_eyes`         | 눈 감기        | Eyes softly closed, relaxed eyelids, as if savoring a quiet private moment. Serene and composed. | 눈을 부드럽게 감고 편안한 눈꺼풀. 고요하고 차분한 사적인 순간. |

### Expression

| stable key        | 한국어 라벨      | Prompt (EN) | 해석 (KR) |
| ----------------- | ---------------- | ----------- | --------- |
| `neutral_still`   | 차분한 무표정    | Neutral and still -- jaw relaxed, lips gently closed, no tension in the face. A calm resting expression. | 턱이 이완되고 입술은 가볍게 다문 채 얼굴에 긴장이 없는 차분한 무표정. |
| `vulnerable`      | 취약한 표정      | Quietly vulnerable -- slightly open lips, soft unfocused eyes, as if caught in a private reflective moment. | 조용히 취약한 표정. 살짝 벌어진 입술, 초점 없는 부드러운 눈빛. 사적인 회상의 순간에 포착된 듯한 느낌. |
| `melancholic`     | 멜랑콜리         | Slightly melancholic -- calm sadness in the eyes, gentle downturn at the corners of the mouth, without dramatic tension. | 눈에 잔잔한 슬픔이 담기고 입꼬리가 살짝 내려간 멜랑콜리한 표정. 극적인 긴장 없음. |
| `sharp_editorial` | 샤프 에디토리얼  | Sharp and editorial -- defined jawline, lips pressed together with intention, eyes focused and intense. | 선명한 턱선, 의도적으로 다문 입술, 집중적이고 강렬한 눈빛의 에디토리얼 표정. |
| `confident_smile` | 자신감 미소      | A confident, subtle smile -- lips curved naturally, relaxed cheeks, warmth in the eyes without exaggeration. | 입술이 자연스럽게 곡선을 그리고 볼은 이완되며 눈에 과장 없는 온기가 담긴 자신감 있는 미소. |
| `playful`         | 장난스러운 표정  | Playful and lighthearted -- a slight smirk or raised brow, mischievous energy, spontaneous and natural. | 살짝 올라간 입꼬리나 눈썹, 장난기 있는 에너지. 즉흥적이고 자연스러운 표정. |
| `dreamy`          | 몽환적 표정      | Dreamy and distant -- slightly unfocused gaze, relaxed parted lips, a soft hazy quality to the expression. | 약간 초점이 흐려진 시선, 편안하게 벌어진 입술. 부드럽고 몽환적인 느낌의 표정. |

### Outfit

| stable key              | 한국어 라벨          | Prompt (EN) | 해석 (KR) |
| ----------------------- | -------------------- | ----------- | --------- |
| `white_tee`             | 화이트 티            | Plain white oversized short-sleeve t-shirt, crew neck visible at the neckline, soft cotton texture. | 크루넥이 보이는 순백색 오버사이즈 반팔 티셔츠. 부드러운 면 질감. |
| `cream_tee`             | 크림 티              | Plain cream ivory oversized short-sleeve t-shirt, crew neck, warm-toned soft cotton texture. | 크림 아이보리톤 오버사이즈 반팔 티셔츠. 따뜻한 톤의 면 질감. |
| `navy_tee`              | 네이비 티            | Plain dark navy oversized short-sleeve t-shirt, crew neck, soft cotton texture. | 다크 네이비 오버사이즈 반팔 티셔츠. 부드러운 면 질감. |
| `black_turtleneck`      | 블랙 터틀넥          | Black slim turtleneck, fabric hugging the neck and jawline, clean silhouette emphasizing the profile. | 목과 턱선을 감싸는 블랙 슬림 터틀넥. 프로필을 강조하는 깔끔한 실루엣. |
| `burgundy_turtleneck`   | 버건디 터틀넥        | Deep burgundy slim turtleneck, rich warm tone hugging the neck and jawline, clean silhouette. | 풍부한 따뜻한 톤의 딥 버건디 슬림 터틀넥. 목과 턱선을 감싸는 깔끔한 실루엣. |
| `navy_turtleneck`       | 네이비 터틀넥        | Dark navy slim turtleneck, cool deep tone hugging the neck and jawline, refined silhouette. | 쿨한 딥 톤의 다크 네이비 슬림 터틀넥. 세련된 실루엣. |
| `ivory_turtleneck`      | 아이보리 터틀넥      | Ivory cream slim turtleneck, soft warm tone hugging the neck and jawline, gentle silhouette. | 부드러운 따뜻한 톤의 아이보리 크림 슬림 터틀넥. 부드러운 실루엣. |
| `camel_turtleneck`      | 카멜 터틀넥          | Warm camel-toned slim turtleneck, earthy neutral tone hugging the neck and jawline, elegant silhouette. | 어시 뉴트럴 톤의 카멜 슬림 터틀넥. 우아한 실루엣. |
| `forest_green_turtleneck` | 포레스트그린 터틀넥 | Deep forest green slim turtleneck, muted natural tone hugging the neck and jawline, clean silhouette. | 뮤트된 자연 톤의 딥 포레스트 그린 슬림 터틀넥. 깔끔한 실루엣. |

### Camera

| stable key       | 한국어 라벨    | Prompt (EN) | 해석 (KR) |
| ---------------- | -------------- | ----------- | --------- |
| `tight_profile`  | 타이트 프로필  | Tight framing on the head and upper shoulders, captured with an 85mm portrait lens at f/1.8. Shallow depth of field with the background softly blurred. Sharp focus on the eye, nose bridge, and jawline, ensuring remarkable clarity and depth of the profile silhouette. | 머리와 상부 어깨를 타이트하게 프레이밍. 85mm 렌즈 f/1.8로 촬영. 얕은 심도로 배경이 부드럽게 블러 처리됨. 눈, 콧대, 턱선에 날카로운 초점. |
| `medium_profile` | 미디엄 프로필  | Close-up framing on the head, neck, and very top of the shoulders only -- no chest, arms, or torso visible. Captured with an 85mm portrait lens at f/2.8. The face fills the majority of the frame. Moderate depth of field with the profile silhouette prominently defined and separated from the background. High-resolution editorial quality. | 머리, 목, 어깨 최상단만 클로즈업 프레이밍. 가슴, 팔, 몸통은 보이지 않음. 85mm 렌즈 f/2.8. 얼굴이 프레임 대부분을 차지. 중간 심도. |

### Atmosphere

| stable key          | 한국어 라벨        | Prompt (EN) | 해석 (KR) |
| ------------------- | ------------------ | ----------- | --------- |
| `moody_editorial`   | 무디 에디토리얼    | Moody editorial atmosphere with precise key and fill lighting designed to highlight every curve and line of the profile. Soft studio key light from the front-facing side sculpts the nose bridge and jawline. Subtle rim light on the back of the head and neck separates the subject from the background. Natural skin texture, detailed hair strands, high-resolution editorial quality. Light grey seamless background. | 프로필의 모든 곡선과 선을 부각하는 정밀한 키/필 조명의 무디 에디토리얼 분위기. 정면 측 소프트 키라이트가 콧대와 턱선을 조각하고, 뒤쪽 림라이트가 배경과 분리. 라이트 그레이 심리스 배경. |
| `clean_minimal`     | 클린 미니멀        | Clean and minimal studio aesthetic. Even soft lighting from a large softbox, minimal shadows. Light grey seamless background. Natural skin tone, smooth complexion, high-resolution quality. | 깔끔하고 미니멀한 스튜디오 미학. 대형 소프트박스의 균일하고 부드러운 조명, 그림자 최소화. 라이트 그레이 심리스 배경. |
| `dramatic_side_lit` | 드라마틱 사이드릿  | Dramatic Rembrandt lighting -- a single hard key light sculpting the features from the direction the subject faces, casting the far side of the face into shadow. The silhouette is prominently defined, skin tone natural and smooth. Strong contrast highlighting the architectural profile silhouette. Cinematic, high-fashion editorial mood. Light grey seamless background. | 렘브란트 조명 -- 단일 하드 키라이트가 피사체 방향에서 이목구비를 조각하고 반대편 얼굴을 그림자로 처리. 실루엣이 선명하게 정의됨. 시네마틱 하이패션 에디토리얼 무드. |
| `dark_charcoal`     | 다크 차콜          | Dark, cinematic studio atmosphere. Dramatic directional lighting sculpting the face against a dark charcoal grey seamless background. Strong contrast between lit and shadow areas. Natural skin texture with a subtle warm glow on the highlight side. Detailed hair strands, high-resolution editorial quality. Moody, high-fashion editorial mood. | 어둡고 시네마틱한 스튜디오 분위기. 다크 차콜 그레이 심리스 배경에 극적인 방향 조명. 밝은 면과 그림자의 강한 대비. 하이라이트 쪽에 은은한 따뜻한 광택. |
| `warm_peach`        | 웜 피치            | Warm, soft studio atmosphere with gentle even lighting. Warm peach beige seamless background. Natural skin tone with a healthy warm glow, smooth complexion. Detailed hair strands, high-resolution editorial quality. Approachable, gentle mood. | 부드럽고 고른 조명의 따뜻한 스튜디오 분위기. 웜 피치 베이지 심리스 배경. 건강한 따뜻한 광택의 자연스러운 피부톤. 다가가기 쉬운 부드러운 무드. |

---

## 5. Full Body

### Scene

| stable key        | 한국어 라벨    | Prompt (EN) | 해석 (KR) |
| ----------------- | -------------- | ----------- | --------- |
| `studio_standing` | 스탠딩         | A full-body shot of a young Korean idol with a slim, lean build and naturally balanced proportions typical of an idol trainee. Standing upright in a plain seamless studio background with a relaxed posture, one hand loosely in pocket, the other relaxed at the side. Natural weight distribution on one leg with a slight body angle. Full body visible from head to toe, feet fully in frame, no cropping, space below the feet. | 슬림하고 균형 잡힌 비율의 한국 아이돌 전신 샷. 심리스 스튜디오 배경에서 한 손은 주머니에 느슨하게, 다른 손은 옆에 편안하게. 한쪽 다리에 자연스럽게 무게를 싣고 약간의 바디 앵글. 머리부터 발끝까지 전신, 발 아래 여백 포함. |
| `studio_seated`   | 시티드         | A full-body shot of a young Korean idol with a slim, lean build and naturally balanced proportions typical of an idol trainee. Seated on a simple low stool in a plain seamless studio background, legs slightly apart, hands resting on knees. Relaxed posture with a slight forward lean. Full body visible from head to toe, feet fully in frame, no cropping. | 심리스 스튜디오 배경에서 낮은 스툴에 앉은 전신 샷. 다리를 살짝 벌리고 손은 무릎 위에. 약간 앞으로 기울인 편안한 자세. 머리부터 발끝까지 전신. |

### Gaze

| stable key      | 한국어 라벨    | Prompt (EN) | 해석 (KR) |
| --------------- | -------------- | ----------- | --------- |
| `straight_ahead`| 정면 시선      | Looking straight ahead past the camera with a calm, distant gaze. | 차분하고 먼 시선으로 카메라를 지나쳐 정면을 바라봄. |
| `off_camera`    | 오프 카메라    | Head facing slightly off-camera to the side with a natural, composed look. | 고개를 살짝 옆으로 돌려 카메라 바깥을 향한 자연스럽고 차분한 모습. |
| `slight_down`   | 아래 시선      | Eyes cast slightly downward with a contemplative, introspective look. | 살짝 아래를 내려다보는 사색적이고 내성적인 시선. |
| `upward`        | 위 시선        | Eyes gazing gently upward, as if looking at something above -- a light, airy, open expression. | 위를 부드럽게 올려다보는 시선. 가볍고 열린 느낌의 표정. |

### Expression

| stable key        | 한국어 라벨      | Prompt (EN) | 해석 (KR) |
| ----------------- | ---------------- | ----------- | --------- |
| `neutral_serious` | 진지한 무표정    | Neutral and composed, slightly serious with soft eyes. | 뉴트럴하고 차분하며, 부드러운 눈빛으로 살짝 진지한 표정. |
| `soft_gaze`       | 소프트 게이즈    | Soft, gentle gaze with relaxed brows and a barely-there warmth. | 이완된 눈썹과 겨우 느껴지는 온기의 부드럽고 젠틀한 시선. |
| `melancholic`     | 멜랑콜리         | Calm, slightly melancholic expression with quiet vulnerability in the eyes. | 눈에 조용한 취약함이 담긴 차분하고 살짝 멜랑콜리한 표정. |
| `confident_smile` | 자신감 미소      | A confident, subtle smile -- lips curved naturally, relaxed cheeks, warmth in the eyes without exaggeration. | 입술이 자연스럽게 곡선을 그리고 볼은 이완되며 눈에 과장 없는 온기가 담긴 자신감 있는 미소. |
| `playful`         | 장난스러운 표정  | Playful and lighthearted -- a slight smirk or raised brow, mischievous energy, spontaneous and natural. | 살짝 올라간 입꼬리나 눈썹, 장난기 있는 에너지. 즉흥적이고 자연스러운 표정. |
| `dreamy`          | 몽환적 표정      | Dreamy and distant -- slightly unfocused gaze, relaxed parted lips, a soft hazy quality to the expression. | 약간 초점이 흐려진 시선, 편안하게 벌어진 입술. 부드럽고 몽환적인 느낌의 표정. |

### Outfit

| stable key              | 한국어 라벨          | Prompt (EN) | 해석 (KR) |
| ----------------------- | -------------------- | ----------- | --------- |
| `white_tee`             | 화이트 티            | Plain white oversized short-sleeve t-shirt with soft cotton texture, slightly loose fit. Straight-leg blue denim jeans with a relaxed fit. Barefoot -- natural clean feet, relaxed toes, standing flat on the ground. | 부드러운 면 질감의 순백색 오버사이즈 반팔 티셔츠. 블루 데님 스트레이트 진. 맨발 -- 깨끗한 발, 편안한 발가락, 바닥에 평평하게 서 있음. |
| `dusty_pink_tee`        | 더스티핑크 티        | Plain dusty pink oversized short-sleeve t-shirt, soft matte cotton texture. Straight-leg light wash blue denim jeans with a relaxed fit. Barefoot -- natural clean feet, relaxed toes, standing flat on the ground. | 소프트 매트 면 질감의 더스티 핑크 오버사이즈 반팔 티셔츠. 라이트 워시 블루 데님 스트레이트 진. 맨발. |
| `cream_tee`             | 크림 티              | Plain cream ivory oversized short-sleeve t-shirt, warm-toned soft cotton texture. Wide-leg burgundy slacks with a relaxed, loose drape. Barefoot -- natural clean feet, relaxed toes, standing flat on the ground. | 따뜻한 톤의 크림 아이보리 오버사이즈 반팔 티셔츠. 와이드 레그 버건디 슬랙스. 맨발. |
| `sky_blue_tee`          | 스카이블루 티        | Plain soft sky blue oversized short-sleeve t-shirt, light breathable cotton texture. Straight-leg black denim jeans with a relaxed fit. Barefoot -- natural clean feet, relaxed toes, standing flat on the ground. | 가볍고 통기성 있는 면 질감의 스카이 블루 오버사이즈 반팔 티셔츠. 블랙 데님 스트레이트 진. 맨발. |
| `black_turtleneck`      | 블랙 터틀넥          | Black slim turtleneck, fabric hugging the neck and jawline, clean silhouette. Straight-leg dark indigo denim jeans with a relaxed fit. Barefoot -- natural clean feet, relaxed toes, standing flat on the ground. | 목과 턱선을 감싸는 블랙 슬림 터틀넥. 다크 인디고 데님 스트레이트 진. 맨발. |
| `burgundy_turtleneck`   | 버건디 터틀넥        | Deep burgundy slim turtleneck, rich warm tone hugging the neck and jawline. Straight-leg black slacks with a relaxed fit. Barefoot -- natural clean feet, relaxed toes, standing flat on the ground. | 딥 버건디 슬림 터틀넥. 블랙 슬랙스 스트레이트. 맨발. |
| `navy_turtleneck`       | 네이비 터틀넥        | Dark navy slim turtleneck, cool deep tone hugging the neck and jawline. Straight-leg beige cream soft-texture slacks with a relaxed fit. Barefoot -- natural clean feet, relaxed toes, standing flat on the ground. | 다크 네이비 슬림 터틀넥. 베이지 크림톤 소프트 슬랙스. 맨발. |
| `ivory_turtleneck`      | 아이보리 터틀넥      | Ivory cream slim turtleneck, soft warm tone hugging the neck and jawline. Wide-leg black slacks with a relaxed, loose drape. Barefoot -- natural clean feet, relaxed toes, standing flat on the ground. | 아이보리 크림 슬림 터틀넥. 와이드 레그 블랙 슬랙스. 맨발. |
| `camel_turtleneck`      | 카멜 터틀넥          | Warm camel-toned slim turtleneck, earthy neutral tone hugging the neck and jawline. Straight-leg black denim jeans with a relaxed fit. Barefoot -- natural clean feet, relaxed toes, standing flat on the ground. | 카멜톤 슬림 터틀넥. 블랙 데님 스트레이트 진. 맨발. |
| `forest_green_turtleneck` | 포레스트그린 터틀넥 | Deep forest green slim turtleneck, muted natural tone hugging the neck and jawline. Straight-leg black denim jeans with a relaxed fit. Barefoot -- natural clean feet, relaxed toes, standing flat on the ground. | 딥 포레스트 그린 슬림 터틀넥. 블랙 데님 스트레이트 진. 맨발. |

### Camera

| stable key       | 한국어 라벨    | Prompt (EN) | 해석 (KR) |
| ---------------- | -------------- | ----------- | --------- |
| `eye_level_full` | 아이레벨 전신  | Eye-level angle, 50mm lens, realistic proportions. Wide full-body shot, subject centered with clear space around entire body including feet. | 아이레벨 각도, 50mm 렌즈, 사실적 비율. 발을 포함한 전신 주변에 여백이 있는 와이드 전신 샷. |
| `low_angle_full` | 로우앵글 전신  | Slightly low angle, 85mm lens, realistic proportions. Wide full-body shot, subject centered with clear space around entire body including feet. | 살짝 로우 앵글, 85mm 렌즈, 사실적 비율. 발을 포함한 전신 주변에 여백이 있는 와이드 전신 샷. |

### Atmosphere

| stable key         | 한국어 라벨          | Prompt (EN) | 해석 (KR) |
| ------------------ | -------------------- | ----------- | --------- |
| `studio_editorial` | 스튜디오 에디토리얼  | Soft studio lighting, diffused, minimal shadows. High-end fashion editorial, ultra realistic, minimalistic Korean idol photoshoot. High detail, ultra realistic, 8k, clean skin texture, studio photography. Plain light gray seamless studio background. | 부드럽고 확산된 스튜디오 조명, 그림자 최소화. 하이엔드 패션 에디토리얼, 미니멀리스틱 한국 아이돌 화보. 라이트 그레이 심리스 배경. |
| `studio_warm`      | 스튜디오 웜          | Warm-toned soft studio lighting with gentle fill, minimal shadows. High-end fashion editorial, ultra realistic, minimalistic Korean idol photoshoot. High detail, ultra realistic, 8k, clean skin texture, studio photography. Plain light gray seamless studio background. | 따뜻한 톤의 부드러운 스튜디오 조명과 젠틀한 필 라이트. 라이트 그레이 심리스 배경. |
| `soft_peach`       | 소프트 피치          | Soft diffused studio lighting with a subtle warm fill. High-end fashion editorial, ultra realistic, minimalistic Korean idol photoshoot. High detail, 8k, clean skin texture. Muted soft peach seamless studio background. | 은은한 따뜻한 필이 있는 부드럽게 확산된 스튜디오 조명. 뮤트 소프트 피치 심리스 배경. |
| `studio_dark`      | 스튜디오 다크        | Soft studio lighting with a key light and gentle fill, minimal shadows. High-end fashion editorial, ultra realistic, minimalistic Korean idol photoshoot. High detail, 8k, clean skin texture, studio photography. Plain dark charcoal seamless studio background. | 키라이트와 젠틀 필의 부드러운 스튜디오 조명. 다크 차콜 심리스 배경. |

---

## 6. 코드 적용 원칙

- prompt asset, context builder, snapshot 저장값은 이 문서의 stable key를 기준으로 맞춘다.
- 한국어 라벨은 별도 필드 또는 문서/UI에서만 사용한다.
- 실제 모델 입력 프롬프트는 `Prompt (EN)` 열을 기준으로 관리한다.
- key가 문서 기준으로 안정화되면 per-axis `str, Enum`으로 승격한다.

---

## 7. 콘텐츠 컨텍스트 선택 정책

> 이 섹션은 구현 규칙이 아니라 기획 기준이다. 현재 기준은 "컨셉이 정해진 뒤, 각 타입에서 key 1개를 랜덤 선택해 최종 prompt를 빌드한다"이다.

### 7.1 공통 선택 원칙

| 항목       | 정책                                                                                                                                                              |
| ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1차 기준   | 먼저 `concept`를 결정한다.                                                                                                                                        |
| 랜덤 방식  | 선택 대상 타입마다 허용된 key 중 1개를 랜덤 선택한다.                                                                                                             |
| 타입 단위  | 기본 타입은 `scene`, `gaze`, `expression`, `outfit`, `camera`, `atmosphere`다.                                                                                    |
| 고정 타입  | 컨셉에 따라 특정 타입은 랜덤이 아니라 고정값일 수 있다.                                                                                                           |
| 가중치     | 현재 기획에는 타입별 가중치나 우선순위 랜덤은 없다. 허용된 key 집합에서 균등 랜덤을 기본으로 본다.                                                                |
| 조합 방식  | 특별한 금지 규칙이 없는 한, 각 타입은 독립적으로 1개씩 뽑아 조합한다.                                                                                             |

### 7.2 컨셉별 랜덤 선택 규칙

| concept        | 랜덤 선택 타입                                                  | 고정 타입 | 비고                               |
| -------------- | --------------------------------------------------------------- | --------- | ---------------------------------- |
| `side_profile` | `scene`, `gaze`, `expression`, `outfit`, `camera`, `atmosphere` | 없음      | 모든 타입에서 1개씩 랜덤 선택한다. |
| `full_body`    | `scene`, `gaze`, `expression`, `outfit`, `camera`, `atmosphere` | 없음      | 모든 타입에서 1개씩 랜덤 선택한다. |

### 7.3 타입별 선택 단위

| 타입         | 선택 단위          |
| ------------ | ------------------ |
| `scene`      | 포즈/각도 1개      |
| `gaze`       | 시선 1개           |
| `expression` | 표정 1개           |
| `outfit`     | 의상 1개           |
| `camera`     | 구도/앵글 1개      |
| `atmosphere` | 조명/질감/무드 1개 |

### 7.4 빌드 규칙

1. `concept`를 기준으로 허용된 타입 집합을 결정한다.
2. 각 타입에서 key 1개를 랜덤 선택한다.
3. 고정 타입이 있는 컨셉은 해당 값을 그대로 넣는다.
4. 선택된 key 조합으로 최종 prompt를 빌드한다.
