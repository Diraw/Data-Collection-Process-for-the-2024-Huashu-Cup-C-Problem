import os
import pandas as pd
from tqdm import tqdm

# 指定文件夹路径
folder_path = "数据处理"

# 获取文件夹中所有CSV文件的列表
csv_files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]

# 初始化一个空的DataFrame用于存储合并后的数据
combined_csv = pd.DataFrame()

# 遍历所有CSV文件并合并
for csv_file in tqdm(csv_files, desc="合并进度"):
    file_path = os.path.join(folder_path, csv_file)
    df = pd.read_csv(file_path)

    # 添加“城市名称”列，值为文件名（去掉扩展名）
    df["城市名称"] = os.path.splitext(csv_file)[0]

    # 将“城市名称”列移动到第一列
    cols = df.columns.tolist()
    cols = [cols[-1]] + cols[:-1]
    df = df[cols]

    # 合并数据
    combined_csv = pd.concat([combined_csv, df], ignore_index=True)

# 保存合并后的CSV文件
combined_csv.to_csv("combined_csv_file.csv", index=False)

print("所有CSV文件已成功合并！")
