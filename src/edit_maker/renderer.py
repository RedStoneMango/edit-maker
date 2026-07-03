from .records import AudioData

from moviepy import concatenate_videoclips

def render(clips, audio_data:AudioData, out):
    video = concatenate_videoclips(clips, method="compose")
    fvideo = video.with_audio(audio_data.clip)

    fvideo.write_videofile(
        out,
        fps=30,
        codec="libx264",
        audio_codec="aac",
    audio_bitrate="192k"
)
