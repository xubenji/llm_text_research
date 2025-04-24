#!/usr/bin/env python3
import sys
import os

def filter_third_column(input_path: str, threshold: float = 0.29):
    # 构造输出文件名
    base, ext = os.path.splitext(input_path)
    output_path = f"{base}_filtered{ext or '.txt'}"

    with open(input_path, 'r') as fin, open(output_path, 'w') as fout:
        for lineno, line in enumerate(fin, start=1):
            # 去除行尾换行符后按任意空白拆分
            parts = line.rstrip('\n').split()
            if len(parts) < 3:
                # 如果列数不足，可根据需要跳过或报错；这里跳过
                continue
            try:
                value = float(parts[2])
            except ValueError:
                # 如果第三列无法转换成浮点数，也跳过
                continue

            if value < threshold:
                fout.write(line)

    print(f"过滤完成，共写入满足 < {threshold} 的行到: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"用法：{sys.argv[0]} <输入文件名>")
        sys.exit(1)

    input_file = sys.argv[1]
    if not os.path.isfile(input_file):
        print(f"错误：找不到文件 {input_file}")
        sys.exit(1)

    filter_third_column(input_file)
