#!/usr/bin/env python3
import sys
import pandas as pd

if len(sys.argv) < 2:
    print(f"用法: {sys.argv[0]} <行号> [输出文件名]")
    sys.exit(1)

# 从命令行参数获取目标行号（1基数）
try:
    target_line_number = int(sys.argv[1])
except ValueError:
    print("行号必须为整数！")
    sys.exit(1)

# 可选的输出文件名，如果没有提供则只在控制台打印
output_file = sys.argv[2] if len(sys.argv) > 2 else None

csv_filename = "train-eng.csv"  # 固定的 CSV 文件名

# 使用 pandas 读取 CSV 文件
try:
    df = pd.read_csv(csv_filename, encoding="utf-8", engine="python")
except Exception as e:
    print(f"读取 CSV 文件 {csv_filename} 时出错：{e}")
    sys.exit(1)

# 检查行号是否在有效范围内
if target_line_number < 1 or target_line_number > len(df):
    print(f"指定的行号 {target_line_number} 超出范围，该 CSV 文件共有 {len(df)} 行。")
    sys.exit(1)

# 利用 iloc 获取目标行（注意 pandas 行索引从 0 开始）
row = df.iloc[target_line_number - 1]

# 将每个字段单独处理，保留换行符
output_lines = []
for col in df.columns:
    cell_value = row[col]
    # 如果单元格是 NaN 或非字符串类型，转换为字符串后打印
    output_lines.append(f"{col}:\n{cell_value}\n")

final_output = "\n".join(output_lines)

# 打印结果到控制台
print("提取的行内容：")
print(final_output)

# 如果指定了输出文件，则保存内容到文件中
if output_file:
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(final_output)
        print(f"已将提取的行内容保存到 {output_file}")
    except Exception as e:
        print(f"写入输出文件 {output_file} 时出错：{e}")
