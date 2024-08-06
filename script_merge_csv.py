import pandas as pd
import os


def merge_csv_files(file_list, output_file):
    # 读取第一个 CSV 文件作为基础 DataFrame
    combined_data = pd.read_csv(file_list[0])

    for file in file_list[1:]:
        # 读取剩余的 CSV 文件
        data = pd.read_csv(file)

        # 合并数据 （基于第一列的 ID， 使用 how='outer' 来保留所有记录）
        combined_data = pd.merge(
            combined_data, data, on=combined_data.columns[0], how="outer"
        )

    # 保存合并后的文件
    combined_data.to_csv(output_file, index=False)


if __name__ == "__main__":
    csv_files = ["county_data_1_2_3.csv", "交通_处理字符串.csv"]

    output_csv = "county_data_final.csv"

    merge_csv_files(csv_files, output_csv)
    print(f"Merged file saved as {output_csv}")
