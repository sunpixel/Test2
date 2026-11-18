import time

import httpx

from download_stats import DownloadStats


class SpeedTester:
    def __init__(self, url, request_count, on_progress):
        self.url = url
        self.request_count = request_count
        self.on_progress = on_progress

    # Sends requests one after another, waits for each full body, reports live progress
    async def run(self):
        stats = DownloadStats()
        last_report = 0.0
        async with httpx.AsyncClient(follow_redirects=True, timeout=30) as client:
            for index in range(self.request_count):
                finished_seconds = sum(stats.request_times)
                start = time.perf_counter()
                async with client.stream("GET", self.url) as response:
                    response.raise_for_status()
                    async for chunk in response.aiter_bytes():
                        stats.total_bytes += len(chunk)
                        now = time.perf_counter()
                        if now - last_report >= 0.1:
                            last_report = now
                            stats.total_seconds = finished_seconds + (now - start)
                            self.on_progress(stats, index + 1)
                stats.request_times.append(time.perf_counter() - start)
                stats.total_seconds = sum(stats.request_times)
                self.on_progress(stats, index + 1)
        return stats