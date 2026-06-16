import time
import board
import busio
from adafruit_pca9685 import PCA9685

# --- 初期設定 ---
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)
pca.frequency = 50

def angle_to_duty_cycle(angle: float) -> int:
    # 0.5ms〜2.5ms を 50Hz の 16bit PWM に変換
    pulse_ms = 0.5 + (angle / 180.0) * 2.0
    duty_cycle = int((pulse_ms / 20.0) * 0xFFFF)
    return max(0, min(0xFFFF, duty_cycle))

try:
    while True:
        # 0度から180度へ
        for angle in range(0, 181, 10):
            pca.channels[0].duty_cycle = angle_to_duty_cycle(angle)
            print(f"servo angle: {angle}°")
            time.sleep(0.5)

        # 180度から0度へ
        for angle in range(180, -1, -10):
            pca.channels[0].duty_cycle = angle_to_duty_cycle(angle)
            print(f"servo angle: {angle}°")
            time.sleep(0.5)

except KeyboardInterrupt:
    pass
finally:
    pca.deinit()