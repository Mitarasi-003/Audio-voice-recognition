import time
from adafruit_motor import servo
from pca_controller import pca

#=============================================================================================
#モータの設定
#=============================================================================================
minp = 500
maxp = 2500

servo8 = servo.Servo(
    pca.channels[6],
    min_pulse=minp,
    max_pulse=maxp
)

servo8.angle = 90

#=============================================================================================
#モータの動作の定義
#=============================================================================================
def motor2_forward():
    servo8.angle = 120
    print("前進")
    time.sleep(2)


def motor2_backward():
    servo8.angle = 60
    print("後退")
    time.sleep(2)


def motor2_right():
    servo8.angle = 0
    print("右")
    time.sleep(2)


def motor2_left():
    servo8.angle = 180
    print("左")
    time.sleep(2)


def motor2_stop():
    servo8.angle = 0
    print("停止")
    time.sleep(2)


def motor2_default():
    servo8.angle = 90
    print("デフォルト位置")
    time.sleep(2)