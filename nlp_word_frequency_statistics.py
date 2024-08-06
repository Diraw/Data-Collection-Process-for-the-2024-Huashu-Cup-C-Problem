import pandas as pd
import jieba
import nltk
from nltk.corpus import stopwords
from collections import Counter
import string
from difflib import get_close_matches
from tqdm import tqdm

# 下载NLTK的停用词和标点符号数据
nltk.download("stopwords")

# 读取CSV文件
df = pd.read_csv("combined_csv_file.csv")

# 假设需要处理的列名列表
columns_to_process = ["介绍", "小贴士"]

# 定义关键词及其同义词列表
synonyms = {
    "环境环保": [
        "自然",
        "生态",
        "森林",
        "天然",
        "湿地",
        "植物",
        "环境",
        "草原",
        "自然保护区",
    ],
    "人文底蕴": [
        "建筑",
        "历史",
        "文化",
        "古代",
        "遗址",
        "博物馆",
        "文物",
        "艺术",
        "古城",
        "古镇",
        "传统",
    ],
    "气候": ["四季"],
    "美食": ["特色", "餐厅", "品尝"],
}

# 将同义词映射到标准关键词
keyword_map = {
    synonym: keyword
    for keyword, synonyms_list in synonyms.items()
    for synonym in synonyms_list
}

# 手动定义一个中文停用词表
stop_words = set(stopwords.words("chinese"))


# 文本预处理函数
def preprocess_text(text):
    # 转为小写
    text = text.lower()
    # 去除标点符号
    text = text.translate(str.maketrans("", "", string.punctuation))
    # 分词
    words = jieba.lcut(text)
    # 去除停用词
    words = [word for word in words if word not in stop_words]
    return words


# 初始化新的DataFrame，用于存储结果
result_df = df.iloc[:, :2].copy()  # 保留前两列
for keyword in synonyms.keys():
    result_df[keyword] = 0  # 初始化关键词列

# 处理每一行
for index, row in tqdm(df.iterrows(), total=df.shape[0], desc="Processing rows"):
    row_keyword_freq = Counter()

    for column in columns_to_process:
        if pd.notna(row[column]):
            words = preprocess_text(row[column])
            for word in words:
                # 查找近似匹配的关键词
                matched_keywords = get_close_matches(
                    word, keyword_map.keys(), n=1, cutoff=0.8
                )
                if matched_keywords:
                    matched_keyword = matched_keywords[0]
                    standard_keyword = keyword_map[matched_keyword]
                    row_keyword_freq[standard_keyword] += 1

    # 更新结果DataFrame中的关键词频次
    for keyword in synonyms.keys():
        result_df.at[index, keyword] = row_keyword_freq[keyword]

# 保存结果到新的CSV文件
result_df.to_csv("combined_csv_word_frequency.csv", index=False)

print("关键词频次统计已保存到 combined_csv_word_frequency.csv")
