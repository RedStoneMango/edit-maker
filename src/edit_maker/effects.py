from .utils import zoom_in, zoom_out, rotate_in, rotate_out

from dataclasses import dataclass
from PIL import Image, ImageFilter
from moviepy import Effect, vfx
import numpy as np

@dataclass
class Blur(Effect):
    intensity: float = None

    def apply(self, clip):
        if self.intensity is None:
            self.intensity = 0

        def filter(gf, t):
            im = gf(t).copy()
            image = Image.fromarray(im)
            blurred = image.filter(ImageFilter.GaussianBlur(radius=self.intensity))
            return np.array(blurred)
        
        return clip.transform(filter)
