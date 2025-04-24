#!/usr/bin/env python3

import argparse

def main():
    # 解析命令行参数，获取输入文件名
    parser = argparse.ArgumentParser(
        description='Count lines where the 3rd column float value > 0.3'
    )
    parser.add_argument('filename', help='Path to the input file')
    args = parser.parse_args()

    count = 0
    # 打开文件并逐行处理
    with open(args.filename, 'r') as f:
        for line in f:
            parts = line.strip().split()
            # 确保至少有三列
            if len(parts) < 3:
                continue
            # 尝试将第三列转换为浮点数，失败则跳过
            try:
                value = float(parts[2])
            except ValueError:
                continue
            # 统计大于 0.3 的情况
            if value > 0.3:
                count += 1

    print(count)

if __name__ == '__main__':
    main()
