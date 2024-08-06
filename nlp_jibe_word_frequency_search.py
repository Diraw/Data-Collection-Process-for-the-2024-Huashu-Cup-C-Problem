import pandas as pd
from collections import Counter
import jieba
from tqdm import tqdm

# 读取CSV文件
df = pd.read_csv("combined_csv_file.csv")

# 要处理的列名是 '介绍' 和 '小贴士'
text_columns = ["介绍", "小贴士"]

# 将非字符串类型的数据转换为字符串，并且移除缺失值
text_data = df[text_columns].fillna("").astype(str)

# 初始化一个空字符串，用于拼接所有文本
all_text = ""

# 使用 tqdm 显示进度条
for _, row in tqdm(
    text_data.iterrows(), desc="Processing text data", total=text_data.shape[0]
):
    combined_text = " ".join(row)
    all_text += " " + combined_text

# 使用 jieba 进行中文分词
words = jieba.lcut(all_text)

# 统计词频
word_counts = Counter(words)

# 获取最常见的1000个词
most_common_words = word_counts.most_common(1000)

# 将结果输出到一个txt文件中
with open("most_common_words.txt", "w", encoding="utf-8") as f:
    for word, count in most_common_words:
        f.write(f"{word}: {count}\n")

print("已完成分词！")