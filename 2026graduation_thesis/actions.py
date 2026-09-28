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
    motor_default,
    motor_set_angle,
)
from motor8 import (
    motor2_forward,
    motor2_backward,
    motor2_right,
    motor2_left,
    motor2_stop,
    motor2_default,
    motor2_set_angle,
)

from inverse_kinematics import inverse_kinematics

from config import (
    SERVO7_CENTER,
    SERVO8_CENTER,
    SERVO7_DIRECTION,
    SERVO8_DIRECTION,
    SERVO_MIN,
    SERVO_MAX,
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



def move_to(x, y):
    """
    手先を目標座標 (x, y) [mm] に移動する。

    流れ:
        座標
         ↓
        逆運動学
         ↓
        theta1, theta2
         ↓
        サーボ角度
         ↓
        ch7 / ch6
    """

    print("----------------------------")
    print(f"目標座標: x={x} mm, y={y} mm")

    try:
        theta1, theta2 = inverse_kinematics(x, y)

    except ValueError as e:
        print("逆運動学エラー:", e)
        return False

    print(f"theta1 = {theta1:.2f} deg")
    print(f"theta2 = {theta2:.2f} deg")

    # =================================
    # 逆運動学角度 → サーボ角度
    # =================================

    servo7_angle = (
        SERVO7_CENTER
        + SERVO7_DIRECTION * theta1
    )

    servo8_angle = (
        SERVO8_CENTER
        + SERVO8_DIRECTION * theta2
    )

    # =================================
    # サーボ範囲チェック
    # =================================

    if not SERVO_MIN <= servo7_angle <= SERVO_MAX:
        print(
            f"ch7の角度が範囲外です: "
            f"{servo7_angle:.2f} deg"
        )
        return False

    if not SERVO_MIN <= servo8_angle <= SERVO_MAX:
        print(
            f"ch6の角度が範囲外です: "
            f"{servo8_angle:.2f} deg"
        )
        return False

    print(f"ch7 根本側: {servo7_angle:.2f} deg")
    print(f"ch6 手先側: {servo8_angle:.2f} deg")

    # =================================
    # 2つのサーボを同時に動かす
    # =================================

    t1 = threading.Thread(
        target=motor_set_angle,
        args=(servo7_angle,)
    )

    t2 = threading.Thread(
        target=motor2_set_angle,
        args=(servo8_angle,)
    )

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print("移動完了")

    return True

def move_to(x, y):
    theta1, theta2 = inverse_kinematics(x, y)

    servo7_angle = SERVO7_CENTER + SERVO7_DIRECTION * theta1
    servo8_angle = SERVO8_CENTER + SERVO8_DIRECTION * theta2

    t1 = threading.Thread(
        target=motor_set_angle,
        args=(servo7_angle,)
    )

    t2 = threading.Thread(
        target=motor2_set_angle,
        args=(servo8_angle,)
    )

    t1.start()
    t2.start()

    t1.join()
    t2.join()