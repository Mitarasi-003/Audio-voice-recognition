import json
import sounddevice as sd

from voice import recognizer

from actions import (
    forward,
    backward,
    right,
    left,
    stop,
    default,
    move_to,
)

from response_time import ResponseTimer
from logger import save_response_time


# 音声コマンドとモータ動作の対応
COMMANDS = {
    "前": forward,
    "後ろ": backward,
    "右": right,
    "左": left,
    "止まれ": stop,
    "戻れ": default,
    "取る": lambda: move_to(500, 300),
}


timer = ResponseTimer()

print("話しかけてください（Ctrl+Cで終了）")
print("応答時間を response_times.csv に保存します。")

with sd.RawInputStream(
    samplerate=16000,
    blocksize=4000,
    dtype="int16",
    channels=1
) as stream:

    try:
        while True:
            data, overflowed = stream.read(4000)
            data = bytes(data)

            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result["text"]

                if text:
                    print("認識結果:", text)

                    # 認識結果を取得した時点を記録
                    timer.start()

                    action = COMMANDS.get(text)

                    if action is not None:
                        # モータ動作開始直前までを計測
                        response_time_ms = timer.finish()

                        print(
                            f"応答時間: {response_time_ms:.2f} ms"
                        )

                        save_response_time(
                            text,
                            response_time_ms
                        )

                        # 実際のモータ動作
                        action()

                    else:
                        timer.finish()
                        print("登録されていないコマンドです。")

    except KeyboardInterrupt:
        print("\n終了しました。")
