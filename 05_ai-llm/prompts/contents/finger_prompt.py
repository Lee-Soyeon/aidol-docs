"""Finger Heart content image prompt — 손가락 하트 콘텐츠.

Common context is provided by base_content_prompt.py.
"""

from .base_content_prompt import PromptCombination, build_prompt as _build

# ── Option 1: Scene (Location + Action) ──
SCENE_OPTIONS = {
    "practice_room": "K-pop practice room with wooden floor. Speakers or studio equipment visible in the background; slightly messy training environment. The mirror wall is off to the side, outside the camera frame or barely visible at the edge. The subject has exactly two arms and two hands, each hand with five distinct fingers. Only the right hand is raised near the cheek making a Korean finger heart — thumb tip and index finger tip gently touching to form a small heart shape, remaining three fingers curled naturally toward the palm. The left arm hangs relaxed at their side with the hand resting naturally against the thigh. No hand is touching the face or pressing against the cheek. Casual and a little shy, not exaggerated, as if someone snapped a quick photo during a break.",
}

# ── Option 2: Gaze Direction ──
GAZE_OPTIONS = {
    "downward": "looking almost straight ahead but with eyes tilted just a few degrees downward — irises should remain fully visible and centered",
    "side_playful": "glancing to the side playfully",
    "eye_contact": "direct eye contact with the camera",
    "up_dreamy": "looking slightly upward with a soft, dreamy gaze",
}

# ── Option 3: Expression ──
EXPRESSION_OPTIONS = {
    "gentle_smile": "soft, gentle smile",
    "embarrassed": "slightly embarrassed, lips pressed together",
    "cheerful": "relaxed face with bright, cheerful eyes",
    "playful_grin": "playful grin with a hint of mischief",
}

# ── Option 4: Outfit ──
OUTFIT_OPTIONS = {
    "varsity_jacket": "Oversized varsity jacket with contrast sleeves, worn open over a simple crew-neck tee, paired with loose jogger pants and indoor training shoes.",
    "striped_rugby": "Boxy striped rugby polo shirt with a wide collar, paired with relaxed-fit sweatpants and white crew socks.",
    "sleeveless_casual": "Simple sleeveless top in a neutral tone, paired with comfortable loose-fit shorts and indoor training shoes.",
    "hoodie_training": "Relaxed oversized hoodie in a soft tone, paired with straight-leg training pants and indoor training shoes.",
}

# ── Option 5: Camera ──
CAMERA_OPTIONS = {
    "closeup_front": "close-up with the face dominant and a slight crop",
    "waist_up": "waist-up shot showing the full upper body with some room around the subject",
    "medium_chest": "chest-up medium shot",
    "high_angle": "slight high-angle close shot",
}

# ── Option 6: ATMOSPHERE ──
ATMOSPHERE_OPTIONS = {
    "idol_casual": "Indoor fluorescent or soft studio lighting with slightly uneven exposure and soft shadows. Natural Korean Gen Z daily look — effortlessly stylish, no heavy styling. Light, shy, and playful idol-style moment. Slight softness from a smartphone camera; no harsh grain or excessive noise. The overall image should feel like a real casual moment captured on an iPhone.",
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
