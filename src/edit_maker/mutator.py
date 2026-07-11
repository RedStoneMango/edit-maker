from .graphics import is_video
from .logger import VideoWriteLogger

from moviepy import VideoFileClip, AudioFileClip
import tempfile
import os
import shutil
from tqdm import tqdm

def subclip(input, start, end, save_as):
    _, ext = os.path.splitext(os.path.basename(input))
    ext = ext.lower()
    out = save_as or tempfile.mkstemp(suffix=ext)[1]

    video = is_video(input)
    clip = (
        VideoFileClip(input)
        if video else
        AudioFileClip(input)
    )

    sub:AudioFileClip = clip.subclipped(max(0, start), min(clip.duration, end))

    if video:
        sub.write_videofile(
            out,
            logger=VideoWriteLogger(export_only=True)
        )
    else:
        sub.write_audiofile(
            out,
            logger=VideoWriteLogger(print_substep=False)
        )

    if not save_as:
        # Overwrite input file
        shutil.move(out, input)

    tqdm.write("Saved as %s!" % save_as if save_as else "File subclipped!")
