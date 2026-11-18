from dataclasses import dataclass, field


class DownloadStats:
    def __init__(self):
        self.request_times = []
        self.total_bytes = 0
        self.total_seconds = 0.0

    @property
    def average_time(self):
        if not self.request_times:
            return 0.0
        return sum(self.request_times) / len(self.request_times)

    @property
    def bytes_per_second(self):
        if self.total_seconds <= 0:
            return 0.0
        return self.total_bytes / self.total_seconds

    @property
    def kb_per_second(self):
        return self.bytes_per_second / 1024

    @property
    def mb_per_second(self):
        return self.bytes_per_second / (1024 * 1024)

    @property
    def total_mb(self):
        return self.total_bytes / (1024 * 1024)