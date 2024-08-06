import pandas as pd

# 读取CSV文件
df = pd.read_csv("combined_csv_word_frequency.csv")

# 按城市名称分组，并对相应的列进行求和
df_merged = df.groupby("城市名称").sum(numeric_only=True).reset_index()

# 保存合并后的数据到新的CSV文件
df_merged.to_csv("county_data_word_frequency.csv", index=False)

print("合并完成，结果已保存到 county_data_word_frequency.csv")
