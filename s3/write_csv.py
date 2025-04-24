import csv

# 准备要写入的数据
headers = ['Name', 'Age', 'City']
rows = [
    ['Alice', 30, 'New York'],
    ['Bob', 25, 'Los Angeles']
]

# 写入 CSV
with open('output.csv', mode='w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(headers)   # 写入表头
    writer.writerows(rows)     # 写入多行数据

