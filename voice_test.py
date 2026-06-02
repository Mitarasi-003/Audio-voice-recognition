from vosk import Model, KaldiRecognizer
import sounddevice as sd
import queue
import json

# モデルの読み込み（パスは自分の環境に合わせて変更）
model = Model(r"C:\voskmodelsmall\vosk-model-small-ja-0.22")

#語彙の認識向上のため、特定の単語を指定
vocabulary = json.dumps(
    ["前","後ろ","右","左","止まれ"],
    ensure_ascii = False
)

# 認識器の初期化（第二引数はサンプリングレート：16000Hz固定）
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
            data = bytes(data)  # または data.tobytes()
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                if result["text"]:
                    print("認識結果:", result["text"])
    except KeyboardInterrupt:
        pass