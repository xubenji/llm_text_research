#!/usr/bin/env python3
import sys

if len(sys.argv) < 2:
    print(f"用法: {sys.argv[0]} input_filename [output_filename]")
    sys.exit(1)

input_filename = sys.argv[1]
output_filename = sys.argv[2] if len(sys.argv) > 2 else "output.txt"

with open(input_filename, "r") as fin, open(output_filename, "w") as fout:
    for line in fin:
        line = line.strip()
        if not line:
            continue
        # 根据实际分隔符调整，比如这里假设各列之间以空格分隔
        cols = line.split()
        if len(cols) < 3:
            continue
        try:
            # 如果第三列无法转换为数字，则会跳到 except 块
            if float(cols[2]) == 0:
                fout.write(line + "\n")
        except ValueError:
            continue

print("过滤完成！已将第三列为数字 0 的行保存到", output_filename)
