"""Side-Profile Studio content image prompt."""

from dataclasses import dataclass
from typing import Literal, TypeAlias

from .base import (
    CONSTRAINT_LOCK,
    IDENTITY_LOCK,
    compose_prompt,
    resolve_option_text,
)

SIDE_PROFILE_CONCEPT_GUIDE = """Create a high-end editorial side-profile close-up studio portrait.
The face must dominate the frame — tight crop on head, neck, and top of shoulders only.
Do NOT show the chest, arms, or hands. Emphasize the subject's facial silhouette, jawline,
and nose bridge with precise studio lighting.
Maintain natural, anatomically correct facial proportions.
The head must not appear oversized relative to the neck and shoulders."""

# ── Literal type aliases ──

SideSceneKey: TypeAlias = Literal[
    "profile_right",
    "profile_left",
    "three_quarter_right",
    "three_quarter_left",
]
SideGazeKey: TypeAlias = Literal[
    "forward_past_camera",
    "slight_down",
    "over_shoulder",
    "upward",
    "closed_eyes",
]
SideExpressionKey: TypeAlias = Literal[
    "neutral_still",
    "vulnerable",
    "melancholic",
    "sharp_editorial",
    "confident_smile",
    "playful",
    "dreamy",
]
SideOutfitKey: TypeAlias = Literal[
    "white_tee",
    "cream_tee",
    "navy_tee",
    "black_turtleneck",
    "burgundy_turtleneck",
    "navy_turtleneck",
    "ivory_turtleneck",
    "camel_turtleneck",
    "forest_green_turtleneck",
]
SideCameraKey: TypeAlias = Literal[
    "tight_profile",
    "medium_profile",
]
SideAtmosphereKey: TypeAlias = Literal[
    "moody_editorial",
    "clean_minimal",
    "dramatic_side_lit",
    "dark_charcoal",
    "warm_peach",
]

# ── Option 1: Scene (Setting + Angle) ──

SCENE_OPTIONS: dict[SideSceneKey, str] = {
    "profile_right": "A captivating close-up studio portrait of a young Korean idol with naturally balanced proportions typical of an idol trainee. Presented in a crisp right-side profile, expertly positioned to accentuate the elegant sweep of the nose bridge, the sharply defined jawline, and a strong facial silhouette against a plain seamless studio background. Head held naturally upright, neck and jawline visible. Tightly cropped to head and neck only — no chest, arms, or hands visible.",
    "profile_left": "A captivating close-up studio portrait of a young Korean idol with naturally balanced proportions typical of an idol trainee. Presented in a crisp left-side profile, expertly positioned to accentuate the elegant sweep of the nose bridge, the sharply defined jawline, and a strong facial silhouette against a plain seamless studio background. Head held naturally upright, neck and jawline visible. Tightly cropped to head and neck only — no chest, arms, or hands visible.",
    "three_quarter_right": "A close-up studio portrait showcasing a young Korean idol with naturally balanced proportions typical of an idol trainee, in a distinct three-quarter profile view angled approximately 45 degrees to the right. Prominent facial features — a perfectly defined nose bridge and a strong jawline — rendered with exceptional detail, creating a sharply outlined silhouette against a plain seamless studio background. Both eyes partially visible, natural head position. Tightly cropped to head and neck only — no chest, arms, or hands visible.",
    "three_quarter_left": "A close-up studio portrait showcasing a young Korean idol with naturally balanced proportions typical of an idol trainee, in a distinct three-quarter profile view angled approximately 45 degrees to the left. Prominent facial features — a perfectly defined nose bridge and a strong jawline — rendered with exceptional detail, creating a sharply outlined silhouette against a plain seamless studio background. Both eyes partially visible, natural head position. Tightly cropped to head and neck only — no chest, arms, or hands visible.",
}

# ── Option 2: Gaze Direction ──

GAZE_OPTIONS: dict[SideGazeKey, str] = {
    "forward_past_camera": "Eyes looking straight ahead past the camera, not engaging the lens — gazing into the distance in the direction the face is turned.",
    "slight_down": "Eyes directed slightly downward, as if looking at something below eye level. Calm and unfocused.",
    "over_shoulder": "Head turned to profile but eyes glancing back toward the camera over the shoulder — a subtle look-back moment.",
    "upward": "Eyes gazing gently upward, as if looking at something above — a light, airy, open expression.",
    "closed_eyes": "Eyes softly closed, relaxed eyelids, as if savoring a quiet private moment. Serene and composed.",
}

# ── Option 3: Expression ──

EXPRESSION_OPTIONS: dict[SideExpressionKey, str] = {
    "neutral_still": "Neutral and still — jaw relaxed, lips gently closed, no tension in the face. A calm resting expression.",
    "vulnerable": "Quietly vulnerable — slightly open lips, soft unfocused eyes, as if caught in a private reflective moment.",
    "melancholic": "Slightly melancholic — calm sadness in the eyes, gentle downturn at the corners of the mouth, without dramatic tension.",
    "sharp_editorial": "Sharp and editorial — defined jawline, lips pressed together with intention, eyes focused and intense.",
    "confident_smile": "A confident, subtle smile — lips curved naturally, relaxed cheeks, warmth in the eyes without exaggeration.",
    "playful": "Playful and lighthearted — a slight smirk or raised brow, mischievous energy, spontaneous and natural.",
    "dreamy": "Dreamy and distant — slightly unfocused gaze, relaxed parted lips, a soft hazy quality to the expression.",
}

# ── Option 4: Outfit ──

OUTFIT_OPTIONS: dict[SideOutfitKey, str] = {
    "white_tee": "Plain white oversized short-sleeve t-shirt, crew neck visible at the neckline, soft cotton texture.",
    "cream_tee": "Plain cream ivory oversized short-sleeve t-shirt, crew neck, warm-toned soft cotton texture.",
    "navy_tee": "Plain dark navy oversized short-sleeve t-shirt, crew neck, soft cotton texture.",
    "black_turtleneck": "Black slim turtleneck, fabric hugging the neck and jawline, clean silhouette emphasizing the profile.",
    "burgundy_turtleneck": "Deep burgundy slim turtleneck, rich warm tone hugging the neck and jawline, clean silhouette.",
    "navy_turtleneck": "Dark navy slim turtleneck, cool deep tone hugging the neck and jawline, refined silhouette.",
    "ivory_turtleneck": "Ivory cream slim turtleneck, soft warm tone hugging the neck and jawline, gentle silhouette.",
    "camel_turtleneck": "Warm camel-toned slim turtleneck, earthy neutral tone hugging the neck and jawline, elegant silhouette.",
    "forest_green_turtleneck": "Deep forest green slim turtleneck, muted natural tone hugging the neck and jawline, clean silhouette.",
}

# ── Option 5: Camera ──

CAMERA_OPTIONS: dict[SideCameraKey, str] = {
    "tight_profile": "Tight framing on the head and upper shoulders, captured with an 85mm portrait lens at f/1.8. Shallow depth of field with the background softly blurred. Sharp focus on the eye, nose bridge, and jawline, ensuring remarkable clarity and depth of the profile silhouette.",
    "medium_profile": "Close-up framing on the head, neck, and very top of the shoulders only — no chest, arms, or torso visible. Captured with an 85mm portrait lens at f/2.8. The face fills the majority of the frame. Moderate depth of field with the profile silhouette prominently defined and separated from the background. High-resolution editorial quality.",
}

# ── Option 6: Atmosphere ──

ATMOSPHERE_OPTIONS: dict[SideAtmosphereKey, str] = {
    "moody_editorial": "Moody editorial atmosphere with precise key and fill lighting designed to highlight every curve and line of the profile. Soft studio key light from the front-facing side sculpts the nose bridge and jawline. Subtle rim light on the back of the head and neck separates the subject from the background. Natural skin texture, detailed hair strands, high-resolution editorial quality. Light grey seamless background.",
    "clean_minimal": "Clean and minimal studio aesthetic. Even soft lighting from a large softbox, minimal shadows. Light grey seamless background. Natural skin tone, smooth complexion, high-resolution quality.",
    "dramatic_side_lit": "Dramatic Rembrandt lighting — a single hard key light sculpting the features from the direction the subject faces, casting the far side of the face into shadow. The silhouette is prominently defined, skin tone natural and smooth. Strong contrast highlighting the architectural profile silhouette. Cinematic, high-fashion editorial mood. Light grey seamless background.",
    "dark_charcoal": "Dark, cinematic studio atmosphere. Dramatic directional lighting sculpting the face against a dark charcoal grey seamless background. Strong contrast between lit and shadow areas. Natural skin texture with a subtle warm glow on the highlight side. Detailed hair strands, high-resolution editorial quality. Moody, high-fashion editorial mood.",
    "warm_peach": "Warm, soft studio atmosphere with gentle even lighting. Warm peach beige seamless background. Natural skin tone with a healthy warm glow, smooth complexion. Detailed hair strands, high-resolution editorial quality. Approachable, gentle mood.",
}


@dataclass(frozen=True, slots=True)
class SideProfilePromptContext:
    scene: SideSceneKey
    gaze: SideGazeKey
    expression: SideExpressionKey
    outfit: SideOutfitKey
    camera: SideCameraKey
    atmosphere: SideAtmosphereKey


def build_side_profile_prompt(context: SideProfilePromptContext) -> str:
    return compose_prompt(
        IDENTITY_LOCK,
        SIDE_PROFILE_CONCEPT_GUIDE,
        resolve_option_text(SCENE_OPTIONS, context.scene, "side scene"),
        resolve_option_text(GAZE_OPTIONS, context.gaze, "side gaze"),
        resolve_option_text(EXPRESSION_OPTIONS, context.expression, "side expression"),
        resolve_option_text(OUTFIT_OPTIONS, context.outfit, "side outfit"),
        resolve_option_text(CAMERA_OPTIONS, context.camera, "side camera"),
        resolve_option_text(ATMOSPHERE_OPTIONS, context.atmosphere, "side atmosphere"),
        CONSTRAINT_LOCK,
    )
