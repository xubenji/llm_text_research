#!/usr/bin/env python3
import argparse
import sys

def load_file1(file1_path):
    """
    读取 file1，返回：
      - lines: 原始所有行的列表（保留换行符）
      - data: {key: (index, float_value)}，key 为第一列，
              index 为在 lines 中的行号（0-based），
              float_value 为第三列解析的浮点数（无法解析则为 None）
    """
    lines = []
    data = {}
    with open(file1_path, 'r', encoding='utf-8') as f1:
        for idx, line in enumerate(f1):
            # 跳过空行或仅空白行
            if not line.strip():
                continue
            lines.append(line)
            parts = line.rstrip('\n').split()
            # 至少要有三列才能解析第三列
            if len(parts) < 3:
                # 如果没有第三列，将值设为 None
                key = parts[0] if parts else None
                if key:
                    data[key] = (idx, None)
                continue

            key = parts[0]
            try:
                val = float(parts[2])
            except ValueError:
                val = None
            data[key] = (idx, val)
    return lines, data

def load_replacements(file2_path, file1_data):
    """
    读取 file2，遍历每行：
      - 跳过空行
      - 尝试解析第三列为 float
      - 若 key 在 file1_data 且 file1 的第三列可解析，
        且 file2 的第三列 > file1 的第三列，则记录替换行
    返回 replacements 字典：{ key: line }
    """
    replacements = {}
    with open(file2_path, 'r', encoding='utf-8') as f2:
        for line in f2:
            # 跳过空行或仅空白行
            if not line.strip():
                continue
            parts = line.rstrip('\n').split()
            if len(parts) < 3:
                continue

            key = parts[0]
            try:
                val2 = float(parts[2])
            except ValueError:
                continue

            if key in file1_data:
                _, val1 = file1_data[key]
                # 只有当 file1 的值存在且 file2 的值更大时，才记录替换
                if val1 is not None and val2 > val1:
                    replacements[key] = line
    return replacements

def write_output(file1_lines, replacements, out_path='final.txt'):
    """
    遍历 file1_lines，若某行的 key 在 replacements 中，
    则写入替换行；否则写入原行。
    """
    with open(out_path, 'w', encoding='utf-8') as fout:
        for orig_line in file1_lines:
            parts = orig_line.rstrip('\n').split()
            if parts and parts[0] in replacements:
                fout.write(replacements[parts[0]])
            else:
                fout.write(orig_line)

def main():
    parser = argparse.ArgumentParser(
        description='当 file2 中某 key 的第三列 > file1 中相同 key 的第三列时，'
                    '用 file2 的整行替换 file1 中对应行，并输出到 final.txt'
    )
    parser.add_argument('file1', help='基准文件路径')
    parser.add_argument('file2', help='用于比较并替换的文件路径')
    args = parser.parse_args()

    # 1. 加载并解析 file1
    file1_lines, file1_data = load_file1(args.file1)

    # 2. 从 file2 中找出需要替换的行
    replacements = load_replacements(args.file2, file1_data)
    if not replacements:
        sys.stderr.write(
            "警告：没有找到需要替换的行；final.txt 将与 file1 相同。\n"
        )

    # 3. 生成合并后的输出
    write_output(file1_lines, replacements)
    print(f"完成！共替换 {len(replacements)} 行，结果已写入 final.txt")

if __name__ == '__main__':
    main()
