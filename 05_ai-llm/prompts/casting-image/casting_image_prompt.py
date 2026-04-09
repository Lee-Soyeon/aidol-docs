# ── Block ② Follow Reference (고정) ──
# Week 1에서는 미사용 (reference image 없이 텍스트만 실험)
BLOCK_FOLLOW_REF = """Maintain the same facial structure, skin tone, eye shape, and natural expressions from the reference image with consistent identity."""

# ── Block ④ Quality (고정) ──
# 바이럴 프롬프트 기반 (MeiGen nanobanana-trending-prompts 참고)
BLOCK_QUALITY_VISUAL = """Photorealistic K-pop idol casting photo, editorial beauty photography.
Stunningly attractive, extremely photogenic face with perfect facial symmetry.
Harmonious golden-ratio proportions.
Flawless luminous dewy skin with subtle natural texture, healthy radiant glow, even skin tone, age 18."""

BLOCK_QUALITY_FRAMING = """Professional headshot, tight ID photo crop, face fills the frame, face centered in upper two-thirds of frame.
Front-facing, eyes at camera.
White crew-neck t-shirt."""

# 배경색
BLOCK_QUALITY_BACKDROP = """Seamless white paper studio backdrop.
Single solid color only, no gradient, no objects, no walls, no windows, no environment."""

BLOCK_QUALITY_LIGHTING = """Soft butterfly lighting with gentle fill light, pure white light.
Symmetrical even illumination, soft shadow under chin only."""

BLOCK_QUALITY_CAMERA = """Shot on Canon EOS R5, 85mm f/1.4, ultra-sharp focus on eyes, 4K resolution."""

BLOCK_CONSTRAINTS = """Do NOT change the specified gender.
Do NOT add glasses, accessories, earrings, or piercings.
Do NOT alter the hairstyle color or length from what is described.
One person only, no extra faces, no text, no watermark."""

# ── 조립된 고정 블록 전문 ──
CASTING_SYSTEM_PROMPT = f"""{BLOCK_QUALITY_VISUAL}

{BLOCK_QUALITY_FRAMING}

{BLOCK_QUALITY_BACKDROP}

{BLOCK_QUALITY_LIGHTING}

{BLOCK_QUALITY_CAMERA}

{BLOCK_CONSTRAINTS}"""

# ── 가변 블록 템플릿 ──
# build_prompt()에서 한국어 UI 값 → 영어 프롬프트 값으로 매핑 후 주입
VARIABLE_BLOCK_TEMPLATE = "Stunningly beautiful {gender} {ethnicity} person, {mood}, {impression}, {hairstyle}, idol-tier visual."
