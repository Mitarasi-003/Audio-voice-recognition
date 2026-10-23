import time
import struct
import threading

from smbus2 import SMBus, i2c_msg
import board
import busio
from adafruit_pca9685 import PCA9685


# ==================================================
# 設定
# ==================================================

# ---------- Y2KB-034 ----------
ENCODER_I2C_BUS = 7
ENCODER_ADDR = 0x11

ECONF_REG_ADDR = 0x0B
CVAL_REG_ADDR = 0x03
CRST_REG_ADDR = 0x02

# int32, Count direction=Up, Multiply=x2_A, Phase=A,B
ECONF_VALUE = 0x07

# ---------- PCA9685 ----------
PCA_ADDR = 0x40

PWM_CH = 4
DIR_CH = 5

PWM_FREQUENCY = 1000

# ---------- モータ ----------
motor_speed = 50
motor_running = False
motor_forward = True

# ---------- エンコーダ表示 ----------
INTERVAL = 0.1

# ---------- スレッド ----------
running = True
motor_lock = threading.Lock()


# ==================================================
# Y2KB-034 I2C通信
# ==================================================

def write_register(bus, address, register, value):
    msg = i2c_msg.write(address, [register, value])
    bus.i2c_rdwr(msg)


def read_registers(bus, address, register, length):
    write_msg = i2c_msg.write(address, [register])
    read_msg = i2c_msg.read(address, length)

    bus.i2c_rdwr(write_msg, read_msg)

    return bytes(read_msg)


def read_encoder_count(bus):
    data = read_registers(
        bus,
        ENCODER_ADDR,
        CVAL_REG_ADDR,
        4
    )

    if len(data) != 4:
        raise IOError("Encoder data length error")

    return struct.unpack("<i", data)[0]


def reset_encoder_count(bus):
    """
    Y2KB-034のCRSTレジスタ仕様に従って
    カウントリセット指令を送信する。
    """

    write_register(
        bus,
        ENCODER_ADDR,
        CRST_REG_ADDR,
        1
    )


# ==================================================
# PCA9685初期化
# ==================================================

def initialize_pca9685():
    """
    PCA9685を初期化する。
    board.I2C()は環境によって既定のI2Cバスを使用する。
    """

    i2c = board.I2C()

    pca = PCA9685(
        i2c,
        address=PCA_ADDR
    )

    pca.frequency = PWM_FREQUENCY

    # PWM停止
    pca.channels[PWM_CH].duty_cycle = 0x0000

    # DIR初期値 LOW
    pca.channels[DIR_CH].duty_cycle = 0x0000

    return pca


# ==================================================
# DIR制御
# ==================================================

def set_dir(pca, high):
    """
    PCA9685 CH1からDIR信号を出力する。

    high=True  : HIGH
    high=False : LOW
    """

    if high:
        pca.channels[DIR_CH].duty_cycle = 0xFF
        print("DIR = HIGH", flush=True)

    else:
        pca.channels[DIR_CH].duty_cycle = 0x00
        print("DIR = LOW", flush=True)


# ==================================================
# PWM制御
# ==================================================

def set_pwm_speed(pca, speed):
    """
    speed: 0～100 (%)
    """

    speed = max(0, min(100, int(speed)))

    duty = int(speed * 65535 / 100)

    pca.channels[PWM_CH].duty_cycle = duty


# ==================================================
# モータ制御
# ==================================================

def motor_stop(pca):
    global motor_running

    with motor_lock:
        # PWMを0にして停止
        pca.channels[PWM_CH].duty_cycle = 0x0000

        motor_running = False

    print("MOTOR STOP", flush=True)


def motor_forward(pca):
    global motor_running, motor_forward, motor_speed

    with motor_lock:
        # 先にPWM停止
        pca.channels[PWM_CH].duty_cycle = 0x0000

        time.sleep(0.1)

        # DIR = LOW
        set_dir(pca, False)

        # PWM出力
        set_pwm_speed(pca, motor_speed)

        motor_forward = True
        motor_running = motor_speed > 0

    print(
        f"MOTOR FORWARD / SPEED={motor_speed}%",
        flush=True
    )


def motor_reverse(pca):
    global motor_running, motor_forward, motor_speed

    with motor_lock:
        # 先にPWM停止
        pca.channels[PWM_CH].duty_cycle = 0x0000

        time.sleep(0.1)

        # DIR = HIGH
        set_dir(pca, True)

        # PWM出力
        set_pwm_speed(pca, motor_speed)

        motor_forward = False
        motor_running = motor_speed > 0

    print(
        f"MOTOR REVERSE / SPEED={motor_speed}%",
        flush=True
    )


# ==================================================
# 速度変更
# ==================================================

def change_speed(pca, delta):
    global motor_speed

    with motor_lock:
        motor_speed = max(
            0,
            min(100, motor_speed + delta)
        )

        if motor_running:
            set_pwm_speed(pca, motor_speed)

        print(
            f"MOTOR SPEED = {motor_speed}%",
            flush=True
        )


# ==================================================
# エンコーダ監視
# ==================================================

def encoder_monitor(bus):
    global running

    while running:
        try:
            count = read_encoder_count(bus)

            print(
                f"\rEncoder Count: {count}       ",
                end="",
                flush=True
            )

        except OSError as e:
            print(
                f"\nEncoder I2C ERROR: {e}",
                flush=True
            )

        time.sleep(INTERVAL)


# ==================================================
# メイン処理
# ==================================================

def main():
    global running

    pca = None
    encoder_bus = None
    monitor_thread = None

    try:
        print("======================================")
        print(" Jetson Orin Nano Motor Control")
        print(" PCA9685 + MD10C R3 + Y2KB-034")
        print("======================================")

        # ------------------------------------------
        # PCA9685初期化
        # ------------------------------------------

        pca = initialize_pca9685()

        print("PCA9685 initialized.")

        # ------------------------------------------
        # エンコーダ初期化
        # ------------------------------------------

        encoder_bus = SMBus(ENCODER_I2C_BUS)

        write_register(
            encoder_bus,
            ENCODER_ADDR,
            ECONF_REG_ADDR,
            ECONF_VALUE
        )

        print("Encoder configuration written.")
        print("Waiting for encoder reboot...")

        time.sleep(4)

        print("Encoder initialized.")

        # ------------------------------------------
        # エンコーダ監視スレッド開始
        # ------------------------------------------

        monitor_thread = threading.Thread(
            target=encoder_monitor,
            args=(encoder_bus,),
            daemon=True
        )

        monitor_thread.start()

        # ------------------------------------------
        # 操作説明
        # ------------------------------------------

        print("\nCommands:")
        print(" f : Forward  (DIR = LOW)")
        print(" r : Reverse  (DIR = HIGH)")
        print(" s : Stop")
        print(" + : Speed +10%")
        print(" - : Speed -10%")
        print(" c : Reset encoder count")
        print(" q : Quit")

        # ------------------------------------------
        # コマンド入力
        # ------------------------------------------

        while True:
            command = input("\nCommand: ").strip().lower()

            if command == "f":
                motor_forward(pca)

            elif command == "r":
                motor_reverse(pca)

            elif command == "s":
                motor_stop(pca)

            elif command == "+":
                change_speed(pca, 10)

            elif command == "-":
                change_speed(pca, -10)

            elif command == "c":
                reset_encoder_count(encoder_bus)
                print("Encoder reset command sent.")

            elif command == "q":
                print("Exiting...")
                break

            else:
                print("Unknown command.")

    finally:
        # ------------------------------------------
        # 終了処理
        # ------------------------------------------

        running = False

        if pca is not None:
            try:
                pca.channels[PWM_CH].duty_cycle = 0x0000
                pca.channels[DIR_CH].duty_cycle = 0x0000
                pca.deinit()

            except Exception as e:
                print(f"PCA9685 shutdown error: {e}")

        if encoder_bus is not None:
            encoder_bus.close()

        if monitor_thread is not None:
            monitor_thread.join(timeout=1)

        print("\nProgram terminated.")


# ==================================================
# プログラム開始
# ==================================================

if __name__ == "__main__":

    try:
        main()

    except KeyboardInterrupt:
        print("\nInterrupted by user.")

    except OSError as e:
        print(f"\nI2C communication error: {e}")