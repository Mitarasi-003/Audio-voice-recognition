from vosk import Model, KaldiRecognizer
import sounddevice as sd
import queue
import json
import time
import busio
import board
from adafruit_motor import servo
from adafruit_pca9685 import PCA9685

#busio.I2C を使ってピンを指定
i2c = busio.I2C(board.SCL, board.SDA) 
# Create a simple PCA9685 class instance.
pca = PCA9685(i2c)

#周波数指定
pca.frequency = 60

#pca9685の7番ピンに接続されたサーボモータを制御するためのServoオブジェクト
servo7 = servo.Servo(pca.channels[7])


# ===== モータ制御関数 =====

def motor_forward():
    servo7.angle = 120
    print("前進")
    # モータ制御コード

def motor_backward():
    servo7.angle = 60
    print("後退")
    # モータ制御コード

def motor_right():
    servo7.angle = 90
    print("右")
    # モータ制御コード

def motor_left():
    servo7.angle = 30
    print("左")
    # モータ制御コード

def motor_stop():
    servo7.angle = 0
    print("停止")
    # モータ制御コード

# ===== Vosk設定 =====
# モデルの読み込み（パスは自分の環境に合わせて変更）
model = Model(r"C:\voskmodelsmall\vosk-model-small-ja-0.22")

#語彙の認識向上のため、特定の単語を指定
vocabulary = json.dumps(
    ["前","後ろ","右","左","止まれ"],
    ensure_ascii=False
)

recognizer = KaldiRecognizer(model, 16000, vocabulary)

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
                result = json.loads(recognizer.Result())
                text = result["text"]

                if text:
                    print("認識結果:", text)

                    if text == "前":
                        motor_forward()

                    elif text == "後ろ":
                        motor_backward()

                    elif text == "右":
                        motor_right()

                    elif text == "左":
                        motor_left()

                    elif text == "止まれ":
                        motor_stop()

    except KeyboardInterrupt:
        pass    