import math

# ==============================
# アーム寸法 [mm]
# ==============================

L1 = 755.0   # 根本側 → 第2関節
L2 = 220.0   # 第2関節 → 手先


def inverse_kinematics(x, y):
    """
    目標座標 (x, y) [mm] から
    第1関節、第2関節の角度 [deg] を計算する。

    戻り値:
        theta1, theta2
    """

    # 原点から目標位置までの距離
    r2 = x ** 2 + y ** 2
    r = math.sqrt(r2)

    # ==============================
    # 到達可能範囲チェック
    # ==============================

    max_reach = L1 + L2
    min_reach = abs(L1 - L2)

    if r > max_reach:
        raise ValueError(
            f"目標位置が到達範囲外です: "
            f"r={r:.2f} mm / 最大={max_reach:.2f} mm"
        )

    if r < min_reach:
        raise ValueError(
            f"目標位置が機構的に到達できません: "
            f"r={r:.2f} mm / 最小={min_reach:.2f} mm"
        )

    # ==============================
    # 第2関節角度
    # ==============================

    cos_theta2 = (
        x ** 2
        + y ** 2
        - L1 ** 2
        - L2 ** 2
    ) / (2 * L1 * L2)

    # 浮動小数点誤差対策
    cos_theta2 = max(-1.0, min(1.0, cos_theta2))

    # 現在は「肘が上側」の解を使用
    theta2 = math.acos(cos_theta2)

    # ==============================
    # 第1関節角度
    # ==============================

    theta1 = math.atan2(y, x) - math.atan2(
        L2 * math.sin(theta2),
        L1 + L2 * math.cos(theta2)
    )

    # ラジアン → 度
    theta1 = math.degrees(theta1)
    theta2 = math.degrees(theta2)

    return theta1, theta2


if __name__ == "__main__":

    # テスト座標
    x = 200.0
    y = 200.0

    try:
        theta1, theta2 = inverse_kinematics(x, y)

        print("----------------------------")
        print("逆運動学テスト")
        print("----------------------------")
        print(f"目標座標 : ({x}, {y}) mm")
        print(f"theta1   : {theta1:.2f} deg")
        print(f"theta2   : {theta2:.2f} deg")

    except ValueError as e:
        print("エラー:", e)