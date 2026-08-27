import time


class ResponseTimer:
    """音声認識からアクション開始までの時間を計測するクラス。"""

    def __init__(self):
        self.recognized_at = None

    def start(self):
        """音声認識結果を受け取った時点の時刻を記録する。"""
        self.recognized_at = time.perf_counter()

    def finish(self):
        """アクション開始時までの経過時間をミリ秒で返す。"""
        if self.recognized_at is None:
            return None

        elapsed_ms = (time.perf_counter() - self.recognized_at) * 1000
        self.recognized_at = None
        return elapsed_ms
