import os
import sys
from pathlib import Path


class Tee:
    def __init__(self, *streams):
        self.streams = list(streams)

    def write(self, data):
        alive_streams = []
        for stream in self.streams:
            try:
                stream.write(data)
                stream.flush()
                alive_streams.append(stream)
            except Exception:
                # Ignore teardown-time stream errors during interpreter shutdown.
                continue
        self.streams = alive_streams

    def flush(self):
        alive_streams = []
        for stream in self.streams:
            try:
                stream.flush()
                alive_streams.append(stream)
            except Exception:
                continue
        self.streams = alive_streams


def should_write_output(path) -> bool:
    path = Path(path)
    return (not os.path.exists(path)) or os.path.getsize(path) == 0


def setup_output_capture(path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if should_write_output(path):
        output_file = open(path, "w", encoding="utf-8")
        sys.stdout = Tee(sys.stdout, output_file)
        sys.stderr = Tee(sys.stderr, output_file)
        return output_file
    return None
