from dataclasses import dataclass

import numpy as np
from moviepy import AudioFileClip

@dataclass
class RenderOptions:
    blur: bool
    vignette: float | None
    darken: float | None

@dataclass
class AudioData:
    clip_durations: list[float]
    duration: float
    clip: AudioFileClip
