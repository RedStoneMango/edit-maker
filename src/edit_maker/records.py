from dataclasses import dataclass
import numpy as np
from moviepy import AudioFileClip

@dataclass
class RenderOptions:
    blur: bool

@dataclass
class AudioData:
    beats: np.ndarray
    duration: float
    clip: AudioFileClip
    