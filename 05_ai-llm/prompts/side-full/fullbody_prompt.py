"""Full-Body Studio content image prompt."""

from dataclasses import dataclass
from typing import Literal, TypeAlias

from .base import (
    CONSTRAINT_LOCK,
    IDENTITY_LOCK,
    compose_prompt,
    resolve_option_text,
)

FULL_BODY_CONCEPT_GUIDE = """Create a high-end editorial full-body studio portrait.
The image should capture the subject's entire body from head to toe in a clean studio setting,
emphasizing natural proportions and relaxed posture."""

# ── Literal type aliases ──

FullBodySceneKey: TypeAlias = Literal[
    "studio_standing",
    "studio_seated",
]
FullBodyGazeKey: TypeAlias = Literal[
    "straight_ahead",
    "off_camera",
    "slight_down",
    "upward",
]
FullBodyExpressionKey: TypeAlias = Literal[
    "neutral_serious",
    "soft_gaze",
    "melancholic",
    "confident_smile",
    "playful",
    "dreamy",
]
FullBodyOutfitKey: TypeAlias = Literal[
    "white_tee",
    "dusty_pink_tee",
    "cream_tee",
    "navy_tee",
    "sky_blue_tee",
    "black_turtleneck",
    "burgundy_turtleneck",
    "navy_turtleneck",
    "ivory_turtleneck",
    "camel_turtleneck",
    "forest_green_turtleneck",
]
FullBodyCameraKey: TypeAlias = Literal[
    "eye_level_full",
    "low_angle_full",
]
FullBodyAtmosphereKey: TypeAlias = Literal[
    "studio_editorial",
    "studio_warm",
    "soft_peach",
    "studio_dark",
]

# ── Option 1: Scene (Location + Action) ──

SCENE_OPTIONS: dict[FullBodySceneKey, str] = {
    "studio_standing": "A full-body shot of a young Korean idol with a slim, lean build and naturally balanced proportions typical of an idol trainee. Standing upright in a plain seamless studio background with a relaxed posture, one hand loosely in pocket, the other relaxed at the side. Natural weight distribution on one leg with a slight body angle. Full body visible from head to toe, feet fully in frame, no cropping, space below the feet.",
    "studio_seated": "A full-body shot of a young Korean idol with a slim, lean build and naturally balanced proportions typical of an idol trainee. Seated on a simple low stool in a plain seamless studio background, legs slightly apart, hands resting on knees. Relaxed posture with a slight forward lean. Full body visible from head to toe, feet fully in frame, no cropping.",
}

# ── Option 2: Gaze Direction ──

GAZE_OPTIONS: dict[FullBodyGazeKey, str] = {
    "straight_ahead": "Looking straight ahead past the camera with a calm, distant gaze.",
    "off_camera": "Head facing slightly off-camera to the side with a natural, composed look.",
    "slight_down": "Eyes cast slightly downward with a contemplative, introspective look.",
    "upward": "Eyes gazing gently upward, as if looking at something above — a light, airy, open expression.",
}

# ── Option 3: Expression ──

EXPRESSION_OPTIONS: dict[FullBodyExpressionKey, str] = {
    "neutral_serious": "Neutral and composed, slightly serious with soft eyes.",
    "soft_gaze": "Soft, gentle gaze with relaxed brows and a barely-there warmth.",
    "melancholic": "Calm, slightly melancholic expression with quiet vulnerability in the eyes.",
    "confident_smile": "A confident, subtle smile — lips curved naturally, relaxed cheeks, warmth in the eyes without exaggeration.",
    "playful": "Playful and lighthearted — a slight smirk or raised brow, mischievous energy, spontaneous and natural.",
    "dreamy": "Dreamy and distant — slightly unfocused gaze, relaxed parted lips, a soft hazy quality to the expression.",
}

# ── Option 4: Outfit ──

OUTFIT_OPTIONS: dict[FullBodyOutfitKey, str] = {
    "white_tee": "Plain white oversized short-sleeve t-shirt with soft cotton texture, slightly loose fit. Straight-leg blue denim jeans with a relaxed fit. Barefoot — natural clean feet, relaxed toes, standing flat on the ground.",
    "dusty_pink_tee": "Plain dusty pink oversized short-sleeve t-shirt, soft matte cotton texture. Straight-leg light wash blue denim jeans with a relaxed fit. Barefoot — natural clean feet, relaxed toes, standing flat on the ground.",
    "cream_tee": "Plain cream ivory oversized short-sleeve t-shirt, warm-toned soft cotton texture. Wide-leg burgundy slacks with a relaxed, loose drape. Barefoot — natural clean feet, relaxed toes, standing flat on the ground.",
    "navy_tee": "Plain dark navy oversized short-sleeve t-shirt, soft cotton texture. Straight-leg black denim jeans with a relaxed fit. Barefoot — natural clean feet, relaxed toes, standing flat on the ground.",
    "sky_blue_tee": "Plain soft sky blue oversized short-sleeve t-shirt, light breathable cotton texture. Straight-leg black denim jeans with a relaxed fit. Barefoot — natural clean feet, relaxed toes, standing flat on the ground.",
    "black_turtleneck": "Black slim turtleneck, fabric hugging the neck and jawline, clean silhouette. Straight-leg dark indigo denim jeans with a relaxed fit. Barefoot — natural clean feet, relaxed toes, standing flat on the ground.",
    "burgundy_turtleneck": "Deep burgundy slim turtleneck, rich warm tone hugging the neck and jawline. Straight-leg black slacks with a relaxed fit. Barefoot — natural clean feet, relaxed toes, standing flat on the ground.",
    "navy_turtleneck": "Dark navy slim turtleneck, cool deep tone hugging the neck and jawline. Straight-leg beige cream soft-texture slacks with a relaxed fit. Barefoot — natural clean feet, relaxed toes, standing flat on the ground.",
    "ivory_turtleneck": "Ivory cream slim turtleneck, soft warm tone hugging the neck and jawline. Wide-leg black slacks with a relaxed, loose drape. Barefoot — natural clean feet, relaxed toes, standing flat on the ground.",
    "camel_turtleneck": "Warm camel-toned slim turtleneck, earthy neutral tone hugging the neck and jawline. Straight-leg black denim jeans with a relaxed fit. Barefoot — natural clean feet, relaxed toes, standing flat on the ground.",
    "forest_green_turtleneck": "Deep forest green slim turtleneck, muted natural tone hugging the neck and jawline. Straight-leg black denim jeans with a relaxed fit. Barefoot — natural clean feet, relaxed toes, standing flat on the ground.",
}

# ── Option 5: Camera ──

CAMERA_OPTIONS: dict[FullBodyCameraKey, str] = {
    "eye_level_full": "Eye-level angle, 50mm lens, realistic proportions. Wide full-body shot, subject centered with clear space around entire body including feet.",
    "low_angle_full": "Slightly low angle, 85mm lens, realistic proportions. Wide full-body shot, subject centered with clear space around entire body including feet.",
}

# ── Option 6: Atmosphere ──

ATMOSPHERE_OPTIONS: dict[FullBodyAtmosphereKey, str] = {
    "studio_editorial": "Soft studio lighting, diffused, minimal shadows. High-end fashion editorial, ultra realistic, minimalistic Korean idol photoshoot. High detail, ultra realistic, 8k, clean skin texture, studio photography. Plain light gray seamless studio background.",
    "studio_warm": "Warm-toned soft studio lighting with gentle fill, minimal shadows. High-end fashion editorial, ultra realistic, minimalistic Korean idol photoshoot. High detail, ultra realistic, 8k, clean skin texture, studio photography. Plain light gray seamless studio background.",
    "soft_peach": "Soft diffused studio lighting with a subtle warm fill. High-end fashion editorial, ultra realistic, minimalistic Korean idol photoshoot. High detail, 8k, clean skin texture. Muted soft peach seamless studio background.",
    "studio_dark": "Soft studio lighting with a key light and gentle fill, minimal shadows. High-end fashion editorial, ultra realistic, minimalistic Korean idol photoshoot. High detail, 8k, clean skin texture, studio photography. Plain dark charcoal seamless studio background.",
}


@dataclass(frozen=True, slots=True)
class FullBodyPromptContext:
    scene: FullBodySceneKey
    gaze: FullBodyGazeKey
    expression: FullBodyExpressionKey
    outfit: FullBodyOutfitKey
    camera: FullBodyCameraKey
    atmosphere: FullBodyAtmosphereKey


def build_full_body_prompt(context: FullBodyPromptContext) -> str:
    return compose_prompt(
        IDENTITY_LOCK,
        FULL_BODY_CONCEPT_GUIDE,
        resolve_option_text(SCENE_OPTIONS, context.scene, "fullbody scene"),
        resolve_option_text(GAZE_OPTIONS, context.gaze, "fullbody gaze"),
        resolve_option_text(EXPRESSION_OPTIONS, context.expression, "fullbody expression"),
        resolve_option_text(OUTFIT_OPTIONS, context.outfit, "fullbody outfit"),
        resolve_option_text(CAMERA_OPTIONS, context.camera, "fullbody camera"),
        resolve_option_text(ATMOSPHERE_OPTIONS, context.atmosphere, "fullbody atmosphere"),
        CONSTRAINT_LOCK,
    )
