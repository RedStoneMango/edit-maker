from dataclasses import dataclass

import numpy as np
from moviepy import AudioFileClip, VideoClip

@dataclass
class RenderOptions:
    blur: bool
    vignette: float | None
    darken: float | None

@dataclass
class BaseEditData:
    graphics: list[str]
    beat_tightness: float
    clips_per_beat: float
    size: tuple[int, int]
    render_options: RenderOptions
    transitions:list[any] # Functions

@dataclass
class IntroData:
    graphic: str
    duration: float | None

@dataclass
class AudioData:
    clip_durations: list[float]
    duration: float
    clip: AudioFileClip

@dataclass
class GeneralData:
    audio: str
    out: str

@dataclass
class BaseEditResult:
    clips: list[VideoClip]
    audio: AudioData