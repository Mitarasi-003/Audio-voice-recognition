#=============================================================================================
#モータを同時に制御するためのコード
#必要に応じてモータの動作の定義を追加してください
#=============================================================================================

import threading

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

def forward():

    t1 = threading.Thread(target=motor_forward)
    t2 = threading.Thread(target=motor2_forward)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

def backward():
    t1 = threading.Thread(target=motor_backward)
    t2 = threading.Thread(target=motor2_backward)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

def right():
    t1 = threading.Thread(target=motor_right)
    t2 = threading.Thread(target=motor2_right)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

def left():
    t1 = threading.Thread(target=motor_left)
    t2 = threading.Thread(target=motor2_left)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

def stop():
    t1 = threading.Thread(target=motor_stop)
    t2 = threading.Thread(target=motor2_stop)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

def default():
    t1 = threading.Thread(target=motor_default)
    t2 = threading.Thread(target=motor2_default)

    t1.start()
    t2.start()

    t1.join()
    t2.join()