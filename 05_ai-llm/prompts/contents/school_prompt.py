"""School content image prompt — 학교 콘텐츠.

Common context is provided by base_content_prompt.py.
"""

from .base_content_prompt import PromptCombination, build_prompt as _build

# ── Option 1: Scene (Location + Action) ──
SCENE_OPTIONS = {
    "classroom": "Korean high school classroom during break time. The subject is sitting casually at the desk with a relaxed posture.",
    "hallway": "Korean high school hallway with white walls and windows on one side. The subject is the only person in the hallway — no other students or people visible anywhere in the frame. The subject is standing with back against the wall, hands in pockets.",
    "stairway": "Stairway inside a school building. The subject is sitting on the middle of a step with both hands resting on their own knees or lap. No hand is touching the railing or any surrounding surface.",
    "rooftop": "School rooftop with a clear sky and a low concrete railing visible behind. Distant cityscape or school buildings in the background. The subject is standing with weight shifted slightly to one side.",
    "convenience_store": "Standing upright in a convenience store near school. The subject is holding a drink casually in one hand.",
}

# ── Option 2: Gaze Direction ──
GAZE_OPTIONS = {
    "look_down": "looking slightly down",
    "look_side": "glancing to the side playfully",
    "look_off_camera": "reacting to something off-camera",
    "look_away": "looking away from the camera",
    "eye_contact": "soft eye contact with the camera",
}

# ── Option 3: Expression ──
EXPRESSION_OPTIONS = {
    "soft_smile": "soft smile",
    "amused": "slightly amused expression",
    "shy_smile": "shy smile",
    "bright_eyed": "relaxed face with bright eyes",
    "subtle_laugh": "subtle laugh",
}

# ── Option 4: Outfit ──
OUTFIT_OPTIONS = {
    "cardigan_uniform_shirt": "navy or dark gray oversized long-sleeve cardigan over a white school shirt, gray uniform pants, and a loosely worn tie",
    "blazer_uniform_shirt": "school blazer over a school shirt, gray uniform pants, and a loosened tie",
    "cardigan_casual_tee": "oversized long-sleeve cardigan over an oversized short-sleeve t-shirt, uniform pants, and wired earphones hanging around the neck connected to a single phone held casually in one hand — the other hand is empty",
    "blazer_casual_tee": "school blazer over an oversized short-sleeve t-shirt, uniform pants, and wired earphones hanging around the neck connected to a single phone held casually in one hand — the other hand is empty",
}

# ── Option 5: Camera ──
CAMERA_OPTIONS = {
    "front_closeup": "close-up with the face dominant and a slight crop",
    "angled_closeup": "close-up from a slight angle",
    "medium_chest": "chest-up medium shot",
    "upper_body_medium": "medium shot with the upper body visible",
    "high_angle": "gentle high-angle shot taken from just slightly above eye level, about one step back from the subject. The camera tilts down no more than 10 to 15 degrees. The head and body must remain in natural proportion — no wide-angle perspective distortion or exaggerated foreshortening that makes the head appear larger than the torso.",
    "side_angle_medium": "slight side-angle medium shot",
}

# ── Option 6: ATMOSPHERE ──
ATMOSPHERE_OPTIONS = {
    "daylight_playful_sticker": "Bright natural daylight streaming through windows with clean, even exposure. A tiny cute bear-shaped sticker, about 1cm, stuck on the cheek, slightly peeling at the edge, casting a tiny shadow on the skin. Light, energetic, and cheerful mood — like a fun moment between classes. Clean smartphone-camera look.",
    "fluorescent_drowsy": "Flat indoor fluorescent lighting with a slightly cool tone and balanced shadows. Quiet, drowsy break-time atmosphere — calm and unhurried. Clean smartphone-camera look.",
    "golden_hour_nostalgic": "Warm golden afternoon light coming from behind, creating a soft backlit glow around the hair and shoulders. No playful details — just a natural, undecorated moment. Warm, sentimental, and slightly nostalgic mood. Clean smartphone-camera look.",
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
