#!/usr/bin/env python3
import argparse
import sys

def load_overrides(file2_path):
    """
    从 file2 中读取所有第三列 > 0.3 的行，
    并以第一列为 key，整行内容为 value，返回 dict。
    """
    overrides = {}
    with open(file2_path, 'r', encoding='utf-8') as f2:
        for line in f2:
            parts = line.rstrip('\n').split()
            # 至少要有三列
            if len(parts) < 3:
                continue
            # 尝试解析第三列
            try:
                val = float(parts[2])
            except ValueError:
                continue
            if val > 0.3:
                key = parts[0]
                overrides[key] = line  # 保留原始换行符
    return overrides

def apply_overrides(file1_path, overrides, out_path='final.txt'):
    """
    读取 file1，每行按第一列匹配 overrides：
    若存在 key，则用 overrides[key] 覆盖，否则保留原行；
    写入 out_path。
    """
    with open(file1_path, 'r', encoding='utf-8') as f1, \
         open(out_path, 'w', encoding='utf-8') as fout:
        for line in f1:
            parts = line.rstrip('\n').split()
            if parts and parts[0] in overrides:
                fout.write(overrides[parts[0]])
            else:
                fout.write(line)

def main():
    parser = argparse.ArgumentParser(
        description='用 file2 中第三列>0.3 的行覆盖 file1 中匹配第一列的行，输出到 final.txt'
    )
    parser.add_argument('file1', help='基准文件路径')
    parser.add_argument('file2', help='包含覆盖行的文件路径')
    args = parser.parse_args()

    overrides = load_overrides(args.file2)
    if not overrides:
        sys.stderr.write("警告：在第二个文件中没有找到第三列>0.3 的行，输出将与原 file1 相同。\n")
    apply_overrides(args.file1, overrides)
    print(f"完成！结果已写入 final.txt （共覆盖 {len(overrides)} 条键）。")

if __name__ == '__main__':
    main()

