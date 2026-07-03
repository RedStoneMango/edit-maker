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

transitions = [

    (
        lambda d: [
            vfx.FadeOut(d)
        ],
        lambda d: [
            vfx.FadeIn(d)
        ],
        "black_fade"
    ),

    (
        lambda d: [
            zoom_out(1.35, d),
            vfx.FadeOut(d)
        ],
        lambda d: [
            zoom_in(0.85, d),
            vfx.FadeIn(d)
        ],
        "pop_zoom"
    ),

    (
        lambda d: [
            rotate_out(8, d),
            vfx.FadeOut(d)
        ],
        lambda d: [
            rotate_in(-8, d),
            vfx.FadeIn(d)
        ],
        "rotate_fade"
    ),

    (
        lambda d: [
            vfx.Rotate(lambda t: 18 * (1 - min(t / d, 1))),
            vfx.Resize(lambda t: 1.2 - 0.2 * min(t / d, 1)),
            vfx.FadeOut(d)
        ],
        lambda d: [
            vfx.Rotate(lambda t: -18 * min(t / d, 1)),
            vfx.Resize(lambda t: 0.85 + 0.15 * min(t / d, 1)),
            vfx.FadeIn(d)
        ],
        "spin_zoom_fade"
    )
]