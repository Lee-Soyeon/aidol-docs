# ── Block ② Follow Reference (고정) ──
# Week 1에서는 미사용 (reference image 없이 텍스트만 실험)
BLOCK_FOLLOW_REF = """Maintain the same facial structure, skin tone, eye shape, and natural expressions from the reference image with consistent identity."""

# ── Block ④ Quality (고정) ──
# 바이럴 프롬프트 기반 (MeiGen nanobanana-trending-prompts 참고)
BLOCK_QUALITY_VISUAL = """Photorealistic K-pop trainee profile photo.
Captivating idol face with refined features.
Smooth radiant skin, natural texture, subtle idol makeup, age 18."""

BLOCK_QUALITY_FRAMING = """Very tight chest-up portrait, head 58% of frame height, centered.
Front-facing, eyes at camera.
White crew-neck t-shirt."""

# 배경색
BLOCK_QUALITY_BACKDROP = """#9BB3C4 muted blue-gray studio backdrop.
Single solid color only, no gradient, no objects, no walls, no windows, no environment."""

BLOCK_QUALITY_LIGHTING = """Soft studio lighting, pure white light.
Symmetrical even illumination, soft shadow under chin only."""

BLOCK_QUALITY_CAMERA = """85mm f/1.8, sharp focus."""

# ── 조립된 고정 블록 전문 ──
CASTING_SYSTEM_PROMPT = f"""{BLOCK_QUALITY_VISUAL}

{BLOCK_QUALITY_FRAMING}

{BLOCK_QUALITY_BACKDROP}

{BLOCK_QUALITY_LIGHTING}

{BLOCK_QUALITY_CAMERA}"""

# ── 가변 블록 템플릿 ──
# build_prompt()에서 한국어 UI 값 → 영어 프롬프트 값으로 매핑 후 주입
VARIABLE_BLOCK_TEMPLATE = "{ethnicity} {gender}, {mood}, {impression}, {hairstyle}."
