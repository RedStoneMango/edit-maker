from dataclasses import dataclass
from PIL import Image, ImageFilter
from moviepy import Effect, VideoClip
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

# ChatGPT math
def darken_clip(clip:VideoClip, intensity: float = 0.5):
    def darken_filter(get_frame, t):
        frame = get_frame(t)
        f = frame.astype(float)

        # Multiply overall brightness and square the pixels to deep-fry the shadows
        processed = (f * intensity) * (f / 255.0)
        return np.clip(processed, 0, 255).astype(np.uint8)

    return clip.transform(darken_filter)

# ChatGPT math
def vignette_clip(clip:VideoClip, base_brightness: float = 0.8):
    w, h = clip.w, clip.h
    
    # Pre-calculate the static 2D vignette meshgrid once to keep render speeds high
    X, Y = np.meshgrid(np.linspace(-1, 1, w), np.linspace(-1, 1, h))
    vignette_mask = np.clip(1.5 - (X**2 + Y**2), 0, 1)
    vignette_mask = np.expand_dims(vignette_mask, axis=2)

    def vignette_filter(get_frame, t):
        frame = get_frame(t)
        f = frame.astype(float) * base_brightness * vignette_mask
        return np.clip(f, 0, 255).astype(np.uint8)

    return clip.transform(vignette_filter)

