from vosk import Model, KaldiRecognizer
import sounddevice as sd
import queue
import json

# 音声データ格納用
q = queue.Queue()

# マイク入力時に呼ばれる
def callback(indata, frames, time, status):
    q.put(bytes(indata))

# 日本語モデル読み込み
model = Model(r"C:\voskmodel\vosk-model-ja-0.22")

# 認識器
rec = KaldiRecognizer(model, 48000)

# マイク開始
with sd.RawInputStream( #sounddeviceのクラス名
        samplerate=48000,
        blocksize=8000,
        dtype='float32',
        channels=1,
        callback=callback):
    
    print("talking please")

    while True:

        data = q.get()

        if rec.AcceptWaveform(data):

            result = json.loads(rec.Result())

            text = result["text"]

            print("recognition:", text)

            # コマンド判定
            if "みぎ" in text:
                print("rigth")

            elif "ひだり" in text:
                print("left")

            elif "すすめ" in text:
                print("forward")

            elif "とまれ" in text:
                print("stop")