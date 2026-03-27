"""School content image prompt — 학교 콘텐츠.

Common context is provided by base_content_prompt.py.
"""

from .base_content_prompt import PromptCombination, build_prompt as _build

# ── Option 1: Scene (Location + Action) ──
SCENE_OPTIONS = {
    "classroom": "Korean high school classroom during break time. The subject is sitting casually at the desk with a relaxed posture.",
    "hallway": "School hallway lined with windows. The subject is leaning lightly against the wall.",
    "stairway": "Stairway inside a school building. The subject is sitting on the steps with elbows resting on the knees.",
    "rooftop": "School rooftop. The subject is standing with weight shifted slightly to one side.",
    "convenience_store": "Convenience store near school. The subject is holding a drink casually.",
}

# ── Option 2: Gaze Direction ──
GAZE_OPTIONS = {
    "down_smile": "looking slightly down with a small smile",
    "side_playful": "glancing to the side playfully",
    "off_camera": "reacting to something off-camera",
    "away_shy": "looking away from the camera with a shy smile",
    "soft_contact": "soft eye contact with the camera",
}

# ── Option 3: Expression ──
EXPRESSION_OPTIONS = {
    "soft_smile": "soft smile",
    "amused": "slightly amused expression",
    "shy_smile": "shy smile",
    "bright_eyes": "relaxed face with bright eyes",
    "subtle_laugh": "subtle laugh",
}

# ── Option 4: Outfit ──
OUTFIT_OPTIONS = {
    "cardigan_shirt": "oversized long-sleeve cardigan over a school shirt, gray uniform pants, and a loosely worn tie",
    "blazer_shirt": "school blazer over a school shirt, gray uniform pants, and a loosened tie",
    "cardigan_tee": "oversized long-sleeve cardigan over an oversized short-sleeve t-shirt, uniform pants, and wired earphones hanging around the neck connected to a single phone held casually in one hand — the other hand is empty",
    "blazer_tee": "school blazer over an oversized short-sleeve t-shirt, uniform pants, and wired earphones hanging around the neck connected to a single phone held casually in one hand — the other hand is empty",
}

# ── Option 5: Camera ──
CAMERA_OPTIONS = {
    "closeup_front": "close-up with the face dominant and a slight crop",
    "closeup_angle": "close-up from a slight angle",
    "medium_chest": "chest-up medium shot",
    "medium_upper": "medium shot with the upper body visible",
    "high_angle": "slight high-angle close shot",
    "side_medium": "slight side-angle medium shot",
}

# ── Option 6: ATMOSPHERE ──
ATMOSPHERE_OPTIONS = {
    "bright_sticker": "Bright natural daylight streaming through windows with clean, even exposure. A small sticker playfully placed on the cheek. Light, energetic, and cheerful mood — like a fun moment between classes. Clean smartphone-camera look.",
    "fluorescent_doodle": "Flat indoor fluorescent lighting with a slightly cool tone and balanced shadows. A light doodle mark drawn on the back of the hand or wrist. Quiet, drowsy break-time atmosphere — calm and unhurried. Clean smartphone-camera look.",
    "golden_nostalgic": "Warm golden afternoon light coming from behind, creating a soft backlit glow around the hair and shoulders. No playful details — just a natural, undecorated moment. Warm, sentimental, and slightly nostalgic mood. Clean smartphone-camera look.",
    "overcast_relaxed": "Overcast soft light with no harsh shadows, gentle and even across the face. Slightly messy or untucked uniform detail. Comfortable, laid-back atmosphere — like the end of a long school day. Clean smartphone-camera look.",
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
