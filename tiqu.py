import pandas as pd

# 读取原始CSV文件
df = pd.read_csv("average_temperature.csv")

# 提取“城市”和“平均气温”列
new_df = df[["城市", "平均气温"]]

# 将提取的内容保存到新文件
new_df.to_csv("county_average_temperature.csv", index=False)
