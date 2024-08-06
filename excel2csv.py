import pandas as pd


def excel_to_csv(excel_file_path, csv_file_path):
    # 读取Excel文件的第一个工作表
    df = pd.read_excel(excel_file_path, sheet_name="【2022年】逐年平均气温")

    # 将DataFrame保存为CSV文件
    df.to_csv(csv_file_path, index=False)


# 示例用法
excel_file_path = "368个城市平均气温数据（2001-2022年）.xlsx"
csv_file_path = "average_temperature.csv"

excel_to_csv(excel_file_path, csv_file_path)
