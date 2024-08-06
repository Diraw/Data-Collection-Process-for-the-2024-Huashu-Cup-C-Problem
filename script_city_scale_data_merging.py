import pandas as pd


def merge_csv(file1, file2):
    # 读取CSV文件
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    # 合并CSV数据
    combined_df = pd.concat([df1, df2], ignore_index=True)

    # 处理“县级市”重复的数据
    combined_df.sort_values(by=["县级市"], inplace=True)
    duplicated_rows = combined_df[combined_df.duplicated(subset=["县级市"], keep=False)]

    duplicate_count = 0
    abnormal_count = 0
    abnormal_records = []

    # 创建一个字典来跟踪县级市的计数
    county_count = {}

    for county in duplicated_rows["县级市"].unique():
        duplicates = duplicated_rows[duplicated_rows["县级市"] == county]
        if duplicates.drop_duplicates().shape[0] == 1:
            duplicate_count += len(duplicates)
            # 删除多余的重复记录，只保留一条
            combined_df.drop(duplicates.index[1:], inplace=True)
        else:
            abnormal_count += len(duplicates)
            abnormal_records.append(duplicates)
            if county not in county_count:
                county_count[county] = 0
            for idx, row in duplicates.iterrows():
                combined_df.at[idx, "县级市"] = (
                    f"{row['县级市']}_{county_count[county] + 1}"
                )
                county_count[county] += 1

    print(f"重复的记录条数: {duplicate_count}")
    print(f"异常的记录条数: {abnormal_count}")

    if abnormal_records:
        print("以下是异常的记录（县级市重复但数据不一样）：")
        for abnormal in abnormal_records:
            print(abnormal)
    else:
        print("没有异常的记录（县级市重复但数据不一样）。")

    # 检查是否有“县级市”不一样但数据是一样的数据
    unique_by_county_df = combined_df.drop_duplicates(subset=["县级市"])
    duplicates_by_data = unique_by_county_df[
        unique_by_county_df.duplicated(
            subset=["总人口", "面积", "人口密度"], keep=False
        )
    ]

    if not duplicates_by_data.empty:
        print("以下记录“县级市”不同但数据相同：")
        print(duplicates_by_data)
    else:
        print("没有“县级市”不同但数据相同的记录。")

    return combined_df


# 调用函数并保存合并后的CSV
merged_df = merge_csv("county_data_0.csv", "county_data.csv")
merged_df.to_csv("merged_output.csv", index=False)
