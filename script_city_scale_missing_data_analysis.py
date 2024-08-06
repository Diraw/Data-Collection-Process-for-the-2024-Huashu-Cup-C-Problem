import csv


def read_first_column(file_path):
    county_set = set()
    with open(file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # 跳过标题行
        for row in reader:
            county_set.add(row[0])
    return county_set


def find_missing_items(file1, file2):
    set1 = read_first_column(file1)
    set2 = read_first_column(file2)

    missing_in_file1 = set2 - set1
    missing_in_file2 = set1 - set2

    return missing_in_file1, missing_in_file2


file1 = "county_data.csv"
file2 = "counties.csv"

missing_in_file1, missing_in_file2 = find_missing_items(file1, file2)

print(f"{file1}中缺失的县级市: {missing_in_file1}")
print(f"{file2}中缺失的县级市: {missing_in_file2}")
