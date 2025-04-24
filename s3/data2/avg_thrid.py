#!/usr/bin/env python3
import argparse
import sys

def compute_average_third_column(filename):
    total = 0.0
    count = 0

    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            # 跳过空行
            if not line.strip():
                continue

            parts = line.strip().split()
            # 确保至少有三列
            if len(parts) < 3:
                continue

            # 尝试解析第三列为浮点数，失败则跳过
            try:
                value = float(parts[2])
            except ValueError:
                continue

            total += value
            count += 1

    if count == 0:
        print("没有可解析的第三列浮点数。")
    else:
        average = total / count
        print(f"第三列可解析浮点数的平均值：{average}")

def main():
    parser = argparse.ArgumentParser(
        description="读取指定文件的第三列浮点数并计算平均值，非浮点值行会被跳过。"
    )
    parser.add_argument('filename', help='要处理的文件路径')
    args = parser.parse_args()

    compute_average_third_column(args.filename)

if __name__ == '__main__':
    main()

