from .logger import VideoWriteLogger
from .audio import add_audio

from moviepy import concatenate_videoclips, VideoClip
from tqdm import tqdm

def render(clips, audio_clip, out):
    video = concatenate_videoclips(clips, method="compose")
    fvideo:VideoClip = add_audio(video, audio_clip)

    fvideo.write_videofile(
        out,
        fps=30,
        codec="libx264",
        audio_codec="aac",
        audio_bitrate="192k",
        logger=VideoWriteLogger()
    )

    tqdm.write("Done! Saved as '%s'" % (out))
