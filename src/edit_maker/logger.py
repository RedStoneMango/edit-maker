from tqdm import tqdm
from proglog import TqdmProgressBarLogger


class VideoWriteLogger(TqdmProgressBarLogger):
    def __init__(self):
        super().__init__(print_messages=False)

        self.audio_started = False
        self.video_started = False

    def callback(self, **changes):
        changes.pop("message", None)
        return super().callback(**changes)

    def bars_callback(self, bar, attr, value, old_value=None):
        if bar == "chunk" and not self.audio_started:
            self.audio_started = True
            tqdm.write("Exporting audio")
        elif bar == "frame_index" and not self.video_started:
            self.video_started = True
            tqdm.write("Rendering video")

        return super().bars_callback(bar, attr, value, old_value)