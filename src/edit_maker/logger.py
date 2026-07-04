from tqdm import tqdm
from proglog import TqdmProgressBarLogger, ProgressBarLogger


from tqdm import tqdm
from typing import List, Dict


class GlobalTeeLogger(ProgressBarLogger):
    def __init__(self, total_logger, stage_logger):
        ProgressBarLogger.__init__(self)
        self.total_logger = total_logger
        self.stage_logger = stage_logger

    def iter_bar(self, bar_prefix="", it=None, **kw):
        total_iter = self.total_logger.iter_bar(bar_prefix, it=it, **kw)
        stage_iter = self.stage_logger.iter_bar(bar_prefix, it=it, **kw)

        def synced():
            for t_val, s_val in zip(total_iter, stage_iter):
                yield s_val

        return synced()

    def bars_callback(self, bar, attr, value, old_value):
        self.total_logger.bars_callback(bar, attr, value, old_value)
        return self.stage_logger.bars_callback(bar, attr, value, old_value)

    def callback(self, **kw):
        self.total_logger.callback(**kw)
        return self.stage_logger.callback(**kw)

    def close(self):
        self.total_logger.close()
        return self.stage_logger.close()
    
    def set_stage_logger(self, stage_logger):
        self.stage_logger = stage_logger

    def close(self):
        self.stage_logger.close()


class TotalLogger(TqdmProgressBarLogger):
    def __init__(self, stages: List[str]):
        TqdmProgressBarLogger.__init__(self)
        self.stages = stages

        self.progress: Dict[str, float] = {s: 0.0 for s in stages}

        self.bar = tqdm(total=100, desc="Total", unit="%")
        self.last_percent = 0.0
        self.max_values = {}

    def bars_callback(self, bar, attr, value, old_value=None):
        if attr != "index":
            return

        if bar not in self.progress:
            return
        
        max_value = self.bars[bar].get("total")
        self.max_values[bar] = max_value

        normalized = 0.0
        if max_value > 0:
            normalized = min(1.0, value / max_value)

        self.progress[bar] = normalized
        percent = (sum(self.progress.values()) / len(self.stages)) * 100

        delta = percent - self.last_percent
        if delta >= 1:
            self.bar.update(delta)
            self.last_percent = percent

    def callback(self, **kw):
        kw.pop("message", None)
        super().callback(**kw)

    def close(self):
        self.bar.close()


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
            tqdm.write("[4/5]  Exporting audio")
        elif bar == "frame_index" and not self.video_started:
            self.video_started = True
            tqdm.write("[5/5]  Rendering video")

        return super().bars_callback(bar, attr, value, old_value)