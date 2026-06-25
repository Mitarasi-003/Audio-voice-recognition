from vosk import Model, KaldiRecognizer
import json

model = Model(
    "/home/hirano/Audiodevicerecognition/vosk-model/vosk-model-small-ja-0.22"
)

vocabulary = json.dumps(
    ["前", "後ろ", "右", "左", "止まれ", "戻れ"],
    ensure_ascii=False
)

recognizer = KaldiRecognizer(
    model,
    16000,
    vocabulary
)