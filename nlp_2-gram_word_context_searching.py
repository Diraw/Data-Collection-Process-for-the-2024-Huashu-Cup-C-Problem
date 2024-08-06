import pandas as pd
import jieba.posseg as pseg
from tqdm import tqdm

# 读取CSV文件
df = pd.read_csv("combined_csv_file.csv")

# 要处理的列名是 '介绍' 和 '小贴士'
text_data = df[["介绍", "小贴士"]]

# 将非字符串类型的数据转换为字符串，并且移除缺失值
text_data = text_data.dropna().astype(str)

# 初始化一个列表，用于存储处理后的句子
processed_sentences = []

# 使用 tqdm 显示进度条
for _, row in tqdm(
    text_data.iterrows(), desc="Processing text data", total=len(text_data)
):
    # 将多列内容合并成一个字符串
    text = " ".join(row)
    # 使用 jieba 进行中文分词和词性标注
    words = pseg.cut(text)
    # 将词和词性组合，并加入到处理后的句子中
    processed_sentences.append([(word, flag) for word, flag in words])


# 定义一个函数来获取某个词的上下文
def get_context(target_words, window_size=2):
    context = {word: [] for word in target_words}
    for sentence in processed_sentences:
        words = [word for word, _ in sentence]
        for target_word in target_words:
            if target_word in words:
                idx = words.index(target_word)
                start = max(0, idx - window_size)
                end = min(len(words), idx + window_size + 1)
                context[target_word].append(sentence[start:end])
    return context


# 指定要查询的词语列表
target_words = [
    "自然",
    "生态",
    "森林",
    "天然",
    "湿地",
    "植物",
    "环境",
    "草原",
    "自然保护区",
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
    "四季",
    "气候",
    "餐厅",
    "美食",
    "品尝",
]

# 获取特定词语的上下文
contexts = get_context(target_words)

# 将上下文输出保存到txt文件中
with open("words_context.txt", "w", encoding="utf-8") as f:
    for word in target_words:
        f.write(f"\nContext for '{word}':\n")
        for context in contexts[word][:10]:  # 只保存前10个上下文
            f.write(" ".join([f"{word}({flag})" for word, flag in context]) + "\n")
