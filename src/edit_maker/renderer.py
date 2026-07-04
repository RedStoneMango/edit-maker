from .dataholders import AudioData
from .logger import VideoWriteLogger

from moviepy import concatenate_videoclips, VideoClip
from tqdm import tqdm

def render(clips, audio_data:AudioData, out):
    video = concatenate_videoclips(clips, method="compose")
    fvideo:VideoClip = video.with_audio(audio_data.clip)

    fvideo.write_videofile(
        out,
        fps=30,
        codec="libx264",
        audio_codec="aac",
        audio_bitrate="192k",
        logger=VideoWriteLogger()
    )

    tqdm.write("Done! Saved as '%s'" % (out))
