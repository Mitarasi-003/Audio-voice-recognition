# dc_encoder.py

import struct
import threading
import time

from smbus2 import SMBus, i2c_msg

from dc_motor_config import (
    ENCODER_BUS_NUMBER,
    ENCODER_ADDRESS,
    REG_CVAL,
    REG_CRST,
    REG_ECONF,
    ECONF_VALUE,
)


def write_register(bus, address, register, value):
    msg = i2c_msg.write(
        address,
        [register, value],
    )
    bus.i2c_rdwr(msg)


def read_registers(bus, address, register, length):
    write_msg = i2c_msg.write(
        address,
        [register],
    )
    read_msg = i2c_msg.read(
        address,
        length,
    )

    bus.i2c_rdwr(write_msg, read_msg)
    return bytes(read_msg)


class DCEncoder:
    def __init__(self):
        self.bus = SMBus(ENCODER_BUS_NUMBER)

        self._monitor_thread = None
        self._monitoring = False

        try:
            write_register(
                self.bus,
                ENCODER_ADDRESS,
                REG_ECONF,
                ECONF_VALUE,
            )

            # 元のプログラムの初期化待ち時間
            time.sleep(4)

        except Exception:
            self.bus.close()
            raise

    def read_count(self):
        data = read_registers(
            self.bus,
            ENCODER_ADDRESS,
            REG_CVAL,
            4,
        )

        if len(data) != 4:
            raise IOError("エンコーダのデータ長が不正です")

        return struct.unpack("<i", data)[0]

    def reset_count(self):
        write_register(
            self.bus,
            ENCODER_ADDRESS,
            REG_CRST,
            1,
        )

    def _monitor_loop(self, interval):
        while self._monitoring:
            try:
                count = self.read_count()
                print(f"エンコーダカウント：{count}")

            except OSError as error:
                print(f"エンコーダ通信エラー：{error}")

            time.sleep(interval)

    def start_monitor(self, interval=0.1):
        if self._monitoring:
            return

        self._monitoring = True
        self._monitor_thread = threading.Thread(
            target=self._monitor_loop,
            args=(interval,),
            daemon=True,
        )
        self._monitor_thread.start()

    def stop_monitor(self):
        self._monitoring = False

        if self._monitor_thread is not None:
            self._monitor_thread.join(timeout=1)
            self._monitor_thread = None

    def close(self):
        self.stop_monitor()
        self.bus.close()