import csv

# 输入的CSV文件名
input_filename = "交通.csv"
# 输出的CSV文件名
output_filename = "交通_处理字符串.csv"

# 读取CSV文件并去掉引号
with open(input_filename, "r", encoding="utf-8") as infile, open(
    output_filename, "w", encoding="utf-8", newline=""
) as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile, quoting=csv.QUOTE_NONE, escapechar="\\")

    for row in reader:
        # 去掉每个元素的引号
        new_row = [elem.strip('"') for elem in row]
        writer.writerow(new_row)

print(f"处理完成，结果已保存到 {output_filename}")
