from dataclasses import dataclass

import numpy as np
from moviepy import AudioFileClip

@dataclass
class RenderOptions:
    blur: bool
    graphic_beats: int
    vignette: float | None
    darken: float | None

@dataclass
class AudioData:
    beats: np.ndarray
    duration: float
    clip: AudioFileClip
