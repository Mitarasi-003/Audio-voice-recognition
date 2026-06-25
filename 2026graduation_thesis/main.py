import sounddevice as sd
import json

from voice import recognizer

from motor import (
    motor_forward,
    motor_backward,
    motor_right,
    motor_left,
    motor_stop,
    motor_default
)

from motor8 import (
    motor2_forward,
    motor2_backward,
    motor2_right,
    motor2_left,
    motor2_stop,
    motor2_default
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
                        motor_forward()
                        motor2_forward()

                    elif text == "後ろ":
                        motor_backward()
                        motor2_backward()

                    elif text == "右":
                        motor_right()
                        motor2_right()

                    elif text == "左":
                        motor_left()
                        motor2_left()

                    elif text == "止まれ":
                        motor_stop()
                        motor2_stop()

                    elif text == "戻れ":
                        motor_default()
                        motor2_default()

    except KeyboardInterrupt:
        pass