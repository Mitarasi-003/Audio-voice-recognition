import csv
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt


CSV_FILE = Path(__file__).with_name("response_times.csv")


def load_data():
    """CSVから応答時間を読み込む。"""
    data = defaultdict(list)

    if not CSV_FILE.exists():
        print("response_times.csv がありません。")
        print("先に main.py を実行して音声コマンドを入力してください。")
        return data

    with CSV_FILE.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            command = row["command"]
            response_time = float(row["response_time_ms"])
            data[command].append(response_time)

    return data


def show_graph():
    """コマンドごとの平均応答時間をグラフ表示する。"""
    data = load_data()

    if not data:
        return

    commands = list(data.keys())
    averages = [
        sum(data[command]) / len(data[command])
        for command in commands
    ]

    plt.figure(figsize=(9, 5))
    plt.bar(commands, averages)

    plt.title("音声入力の平均応答速度")
    plt.xlabel("音声コマンド")
    plt.ylabel("応答時間 (ms)")
    plt.grid(axis="y", alpha=0.3)

    for i, value in enumerate(averages):
        plt.text(i, value, f"{value:.1f} ms",
                 ha="center", va="bottom")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    show_graph()
