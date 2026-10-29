# dc_motor_controller.py

import time

from adafruit_pca9685 import PCA9685
from pca_controller import i2c

from dc_motor_config import (
    PCA_ADDRESS,
    PWM_FREQUENCY,
    PWM_CHANNEL,
    DIR_CHANNEL,
    INITIAL_SPEED,
    SPEED_STEP,
    MIN_SPEED,
    MAX_SPEED,
)


class DCMotorController:
    def __init__(self):
        self.pca = PCA9685(
            i2c,
            address=PCA_ADDRESS,
        )
        self.pca.frequency = PWM_FREQUENCY

        self.pwm = self.pca.channels[PWM_CHANNEL]
        self.direction = self.pca.channels[DIR_CHANNEL]

        self.speed = INITIAL_SPEED
        self.is_running = False
        self.is_forward = True

        self.pwm.duty_cycle = 0
        self.direction.duty_cycle = 0

    def _set_direction(self, forward):
        # 方向を切り替える前にPWMを止める
        self.pwm.duty_cycle = 0
        time.sleep(0.1)

        # 元のプログラムに合わせる
        # 正転：LOW、逆転：HIGH
        self.direction.duty_cycle = (
            0 if forward else 0xFFFF
        )
        self.is_forward = forward

    def _apply_speed(self):
        if not self.is_running:
            return

        duty = round(
            65535 * self.speed / 100
        )
        self.pwm.duty_cycle = duty

    def forward(self):
        self._set_direction(True)
        self.is_running = self.speed > 0
        self._apply_speed()
        print(f"DCモータ：正転、速度 {self.speed}%")

    def backward(self):
        self._set_direction(False)
        self.is_running = self.speed > 0
        self._apply_speed()
        print(f"DCモータ：逆転、速度 {self.speed}%")

    def stop(self):
        self.pwm.duty_cycle = 0
        self.is_running = False
        print("DCモータ：停止")

    def increase_speed(self):
        self.speed = min(
            MAX_SPEED,
            self.speed + SPEED_STEP,
        )
        self._apply_speed()
        print(f"DCモータ速度：{self.speed}%")

    def decrease_speed(self):
        self.speed = max(
            MIN_SPEED,
            self.speed - SPEED_STEP,
        )
        self._apply_speed()
        print(f"DCモータ速度：{self.speed}%")

    def close(self):
        try:
            self.stop()
        finally:
            self.pca.deinit()