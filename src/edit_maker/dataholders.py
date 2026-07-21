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
    beat_deviation: float
    clips_per_beat: float
    render_options: RenderOptions
    transitions:list[any] # Functions

@dataclass
class IntroData:
    graphic: str
    duration: float | None
    play_audio: bool
    audio_time_of_end: float | None
    apply_effects: bool

@dataclass
class AudioData:
    clip_durations: list[float]
    duration: float
    clip: AudioFileClip

@dataclass
class GeneralData:
    audio: str
    out: str
    size: tuple[int, int]

@dataclass
class BaseEditResult:
    clips: list[VideoClip]
    audio: AudioData
