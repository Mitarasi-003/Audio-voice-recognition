# main.py

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

from dc_motor_controller import DCMotorController
from dc_encoder import DCEncoder


def main():
    dc_motor = None
    encoder = None

    try:
        # DCモータとエンコーダの初期化
        dc_motor = DCMotorController()
        encoder = DCEncoder()

        # エンコーダの監視を開始
        encoder.start_monitor(interval=0.1)

        # 音声コマンドと動作の対応
        COMMANDS = {
            # 既存のサーボ動作
            "前": forward,
            "後ろ": backward,
            "右": right,
            "左": left,
            "止まれ": stop,
            "戻れ": default,
            "取る": lambda: move_to(500, 300),

            # 追加するDCモータ動作
            "前進": dc_motor.forward,
            "後退": dc_motor.backward,
            "停止": dc_motor.stop,
            "速度上げて": dc_motor.increase_speed,
            "速度下げて": dc_motor.decrease_speed,
        }

        timer = ResponseTimer()

        print("話しかけてください（Ctrl+Cで終了）")
        print("応答時間を response_times.csv に保存します。")

        with sd.RawInputStream(
            samplerate=16000,
            blocksize=4000,
            dtype="int16",
            channels=1,
        ) as stream:

            while True:
                data, overflowed = stream.read(4000)
                data = bytes(data)

                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    recognized_text = result["text"]

                    if not recognized_text:
                        continue

                    print("認識結果:", recognized_text)

                    # 認識結果を取得した時点で計測開始
                    timer.start()

                    action = COMMANDS.get(recognized_text)

                    if action is None:
                        timer.finish()
                        print("登録されていないコマンドです。")
                        continue

                    # 動作開始直前までの応答時間
                    response_time_ms = timer.finish()

                    print(
                        f"応答時間: {response_time_ms:.2f} ms"
                    )

                    save_response_time(
                        recognized_text,
                        response_time_ms,
                    )

                    # 対応する動作を実行
                    action()

    except KeyboardInterrupt:
        print("\n終了しました。")

    finally:
        # エンコーダの監視と通信を終了
        if encoder is not None:
            try:
                encoder.close()
            except Exception as error:
                print(f"エンコーダ終了処理エラー: {error}")

        # DCモータを停止してリソースを解放
        if dc_motor is not None:
            try:
                dc_motor.close()
            except Exception as error:
                print(f"DCモータ終了処理エラー: {error}")


if __name__ == "__main__":
    main()