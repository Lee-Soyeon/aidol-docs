"""Daily content image prompt — 일상 스냅 콘텐츠.

Common context is provided by base_content_prompt.py.
"""

from .base_content_prompt import PromptCombination, build_prompt as _build

# ── Option 1: Scene (Location + Action) ──
SCENE_OPTIONS = {
    "convenience_store": "Holding a cold iced coffee with a straw in one hand, about to take a sip inside a convenience store at night. Fluorescent tubes on the ceiling cast even light across the space. The background is softly blurred with no prominent shelves or objects directly beside the subject.",
    "parking_lot": "Leaning back against a concrete pillar with weight on one leg, hands stuffed in pockets, standing in an underground parking lot. Concrete walls and exposed ceiling pipes in the background, with a nearby overhead light casting enough light to clearly illuminate the face.",
    "bedroom": "Sitting on the bed or floor next to the bed, holding an iced coffee or absentmindedly scrolling a phone in a lived-in bedroom. K-pop posters and magazine cutouts cover the wall behind, clothes are casually scattered on the bed and floor. A ceiling light fills the room with moderate warm-white indoor light — the face and room are clearly visible but not overexposed.",
}

# ── Option 2: Gaze Direction ──
GAZE_OPTIONS = {
    "glance_left": "Both eyes looking in the same direction, glancing slightly to the left of the camera with a natural, composed expression. Not looking at the camera at all.",
    "blank_right": "Staring blankly at something to the right, not looking at the camera at all — eyes clearly aimed away from the lens.",
}

# ── Option 3: Expression ──
EXPRESSION_OPTIONS = {
    "neutral": "Calm, resting face with lips gently closed and no tension anywhere.",
    "tired": "Slightly tired eyes with a calm, unbothered expression — not sleepy, just at ease late at night.",
    "soft_smile": "A soft, natural smile — gentle and subtle, both corners of the mouth lifted just slightly.",
    "blank": "Completely empty expression, face showing nothing, as if the mind is somewhere else entirely.",
    "curious": "One eyebrow slightly raised, a random thought suddenly crossing the mind.",
}

# ── Option 4: Outfit ──
OUTFIT_OPTIONS = {
    "graphic_tee": "Faded oversized graphic t-shirt with a barely visible washed-out print, paired with loose wrinkled sweatpants.",
    "black_tee": "Washed black oversized t-shirt with slightly stretched neckline, paired with wide-leg denim jeans.",
    "hoodie": "Unzipped hoodie layered over a plain white t-shirt, with loose relaxed-fit pants.",
    "knit_sweater": "Oversized chunky knit sweater with dropped shoulders, paired with relaxed straight-leg pants.",
}

# ── Option 5: Camera ──
CAMERA_OPTIONS = {
    "eye_level": "Eye-level shot, slightly off-center framing with the subject not perfectly centered.",
    "low_angle": "Slightly low angle, camera tilted up just a few degrees from below chin level.",
    "high_angle": "Slightly high angle, camera looking down gently from above eye level.",
    "closeup_crop": "Close-up with partial face cropping, cutting off the top of the head.",
    "medium_wide": "Medium shot with generous empty space on one side, subject occupying only a third of the frame.",
    "side_profile": "Shot from the side, showing the subject almost in profile so only one eye is visible.",
}

# ── Option 6: ATMOSPHERE ──
ATMOSPHERE_OPTIONS = {
    "candid": "Candid snapshot aesthetic, as if a friend casually took this photo on an iPhone without warning. No posing, no preparation. The subject looks like they were caught mid-moment in their everyday life, completely absorbed in what they were doing.",
    "ambient_light": "Moderate indoor lighting from a ceiling light — warm-white tone, not too bright and not too dim. The face is clearly visible with natural soft shadows on one side. The overall look is like a typical room photographed on a smartphone at night with the lights on.",
    "lo_fi": "Slight motion blur on the hands or edges as if the photographer's hand shifted during capture. Faint digital noise consistent with a smartphone camera. Imperfect framing: slightly tilted horizon, minor lens distortion at edges, not perfectly composed.",
    "late_night": "A calm, quiet atmosphere. The subject is the only person in the frame, surrounded by empty space.",
}


def build_prompt(combo: PromptCombination) -> str:
    return _build(
        combo,
        scene_options=SCENE_OPTIONS,
        gaze_options=GAZE_OPTIONS,
        expression_options=EXPRESSION_OPTIONS,
        outfit_options=OUTFIT_OPTIONS,
        camera_options=CAMERA_OPTIONS,
        atmosphere_options=ATMOSPHERE_OPTIONS,
    )
