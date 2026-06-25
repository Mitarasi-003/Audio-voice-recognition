import time
import time
from adafruit_motor import servo
from pca_controller import pca

#=============================================================================================
#モータの設定
#=============================================================================================
minp = 500
maxp = 2500

servo7 = servo.Servo(
    pca.channels[7],
    min_pulse=minp,
    max_pulse=maxp
)

servo7.angle = 90

#=============================================================================================
#モータの動作の定義
#=============================================================================================
def motor_forward():
    servo7.angle = 120
    print("前進")
    time.sleep(2)


def motor_backward():
    servo7.angle = 60
    print("後退")
    time.sleep(2)


def motor_right():
    servo7.angle = 0
    print("右")
    time.sleep(2)


def motor_left():
    servo7.angle = 180
    print("左")
    time.sleep(2)


def motor_stop():
    servo7.angle = 0
    print("停止")
    time.sleep(2)


def motor_default():
    servo7.angle = 90
    print("デフォルト位置")
    time.sleep(2)