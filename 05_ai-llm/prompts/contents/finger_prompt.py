"""Finger Heart content image prompt — 손가락 하트 콘텐츠.

Common context is provided by base_content_prompt.py.
"""

from .base_content_prompt import PromptCombination, build_prompt as _build

# ── Option 1: Scene (Location + Action) ──
SCENE_OPTIONS = {
    "practice_room": "K-pop practice room with wooden floor. Speakers or studio equipment visible in the background; slightly messy training environment. The mirror wall is off to the side, outside the camera frame or barely visible at the edge. The subject is standing upright with both feet on the floor, weight evenly distributed, shoulders level and relaxed — not leaning, sitting, crouching, or tilting to either side. The subject has exactly two arms and two hands, each hand with five distinct fingers. Only the right hand is raised near the cheek making a Korean finger heart — thumb tip and index finger tip gently touching to form a small heart shape, remaining three fingers curled naturally toward the palm. The left arm hangs relaxed at their side with the hand resting naturally against the thigh. No hand is touching the face or pressing against the cheek. Casual and a little shy, not exaggerated, as if someone snapped a quick photo during a break.",
}

# ── Option 2: Gaze Direction ──
GAZE_OPTIONS = {
    "look_down": "head facing the camera but eyes looking about 10 to 15 degrees below the camera lens, as if glancing at something on the ground nearby. The irises sit in the lower-center area of the eye opening, with a thin strip of sclera visible above each iris. Eyelids relaxed and slightly lowered. The head does not tilt down — only the eyes shift downward.",
    "look_side": "head facing the camera with an almost imperceptible gaze shift — eyes looking no more than 5 to 8 degrees to the right of the camera lens. The irises must stay nearly centered in the eye opening with only the slightest horizontal offset, as if the subject briefly noticed something just beside the camera. The head stays completely still and faces the camera directly; only the eyes shift by a tiny amount. Both pupils must point in the exact same direction. No visible sclera on the inner side of either eye. The gaze should still feel like the subject is mostly looking at the camera.",
    "eye_contact": "direct eye contact with the camera",
}

# ── Option 3: Expression ──
EXPRESSION_OPTIONS = {
    "gentle_smile": "soft, gentle smile with both corners of the mouth raised evenly. Both eyes open equally and relaxed.",
    "embarrassed": "slightly embarrassed expression, lips pressed together in a small closed-mouth smile. Both eyes open equally with a natural, shy look.",
    "cheerful": "relaxed face with bright, cheerful eyes and a natural open smile. Both eyes equally open and symmetrical.",
    "playful_grin": "small, natural closed-mouth smile with one corner of the mouth raised just slightly higher than the other — a subtle, easygoing smirk. Both eyes must remain equally open and symmetrical. No squinting, no winking, no exaggerated facial movement.",
}

# ── Option 4: Outfit ──
OUTFIT_OPTIONS = {
    "varsity_jacket": "Oversized varsity jacket with contrast sleeves, worn open over a simple crew-neck tee, paired with loose jogger pants and indoor training shoes.",
    "striped_rugby_shirt": "Boxy striped rugby polo shirt with a wide collar, paired with relaxed-fit sweatpants, white crew socks, and clean indoor training shoes.",
    "sleeveless_casual": "Unisex oversized boxy-fit sleeveless crew-neck top in black or white with a large vintage collegiate-style graphic print on the chest (such as bold block letters, numbers, or a university emblem). The sleeveless top has dropped armholes and falls loosely past the waist. Paired with matching relaxed-fit sweat shorts that sit above the knee in the same or similar color tone as the top, white crew socks, and clean white sneakers.",
    "training_hoodie": "Relaxed oversized hoodie in a soft tone, paired with straight-leg training pants and indoor training shoes.",
}

# ── Option 5: Camera ──
CAMERA_OPTIONS = {
    "front_closeup": "close-up with the face dominant and a slight crop",
    "waist_up": "waist-up shot showing the full upper body with some room around the subject",
    "medium_chest": "chest-up medium shot",
    "high_angle": "gentle high-angle shot taken from just slightly above eye level, about one step back from the subject. The camera tilts down no more than 10 to 15 degrees. The head and body must remain in natural proportion — no wide-angle perspective distortion or exaggerated foreshortening that makes the head appear larger than the torso.",
}

# ── Option 6: ATMOSPHERE ──
ATMOSPHERE_OPTIONS = {
    "idol_casual_snapshot": "Indoor fluorescent or soft studio lighting with slightly uneven exposure and soft shadows. Natural Korean Gen Z daily look — effortlessly stylish, no heavy styling. Light, shy, and playful idol-style moment. Slight softness from a smartphone camera; no harsh grain or excessive noise. The overall image should feel like a real casual moment captured on an iPhone.",
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
