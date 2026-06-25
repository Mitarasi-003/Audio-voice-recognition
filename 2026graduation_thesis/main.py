import sounddevice as sd
import json

from voice import recognizer

from actions import (
    forward,
    backward,
    right,
    left,
    stop,
    default
)

print("話しかけてください（Ctrl+Cで終了）")

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

                result = json.loads(
                    recognizer.Result()
                )

                text = result["text"]

                if text:
                    print("認識結果:", text)

                    if text == "前":
                        forward()

                    elif text == "後ろ":
                        backward()

                    elif text == "右":
                        right()

                    elif text == "左":
                        left()

                    elif text == "止まれ":
                        stop()

                    elif text == "戻れ":
                        default()

    except KeyboardInterrupt:
        pass