import pandas as pd


def handle_missing_values(csv_file_path):
    # 读取CSV文件
    df = pd.read_csv(csv_file_path)

    # 计算每一列的缺失值数量
    missing_values_count = df.isnull().sum()

    # 打印每一列的缺失值数量
    for column, count in missing_values_count.items():
        print(f"Column '{column}' has {count} missing values")

    # 处理缺失值
    # 取平均
    for column in ["平均气温"]:
        if column in df.columns:
            df[column].fillna(df[column].mean(), inplace=True)

    # 打印处理后的缺失值数量
    print("\nAfter handling missing values:")
    missing_values_count = df.isnull().sum()
    for column, count in missing_values_count.items():
        print(f"Column '{column}' has {count} missing values")

    # 保存处理后的数据到新的CSV文件
    df.to_csv("county_data_final_add_temp_clean.csv", index=False)


csv_file_path = "county_data_final_add_temp.csv"  # 需要处理的csv文件
handle_missing_values(csv_file_path)
