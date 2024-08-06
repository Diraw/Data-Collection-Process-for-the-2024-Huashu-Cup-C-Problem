import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from pypinyin import pinyin, Style

# 读取县级市集合的CSV文件
county_csv = "counties.csv"
counties_need = pd.read_csv(county_csv)["城市名字"].tolist()

# 将县级市名字转换为拼音
counties_pinyin = []
for city in counties_need:
    pinyin_list = pinyin(city, style=Style.NORMAL)
    pinyin_str = "".join([item[0] for item in pinyin_list])
    counties_pinyin.append(pinyin_str)

# 绑定县级市名字和拼音
counties_combined = list(zip(counties_need, counties_pinyin))

# 初始化存储数据的列表
data = []
failed_counties = []  # 初始化存储失败地点的列表

base_url = "https://www.air-level.com/air/"

for county in counties_combined:
    url = base_url + county[1]

    try:
        # 发送请求
        response = requests.get(url)

        # 检查请求状态
        if response.status_code == 200:
            # 解析HTML
            soup = BeautifulSoup(response.content, "html.parser")

            # 查找特定的<span>标签
            target_span = soup.find("span", class_="aqi-bg aqi-level-1")

            if target_span:
                # 提取目标数字
                aqi_value = target_span.text.split()[0]
                print(f"{county[0]} 的AQI值:", aqi_value)
                # 将数据添加到列表中
                data.append([county[0], aqi_value])
            else:
                print(f"{county[0]} 没有找到匹配的AQI值")
                data.append([county[0], np.nan])
                failed_counties.append(county[0])
        else:
            print(f"{county[0]} 请求失败，状态码: {response.status_code}")
            data.append([county[0], np.nan])
            failed_counties.append(county[0])

    except Exception as e:
        print(f"{county[0]} 抓取数据时出错: {e}")
        data.append([county[0], np.nan])
        failed_counties.append(county[0])

# 将数据保存到CSV文件
df = pd.DataFrame(data, columns=["县级市", "AQI值"])
df.to_csv("county_data_air_quality.csv", index=False)
print("数据已保存到 county_data_air_quality.csv")

# 输出失败地点信息
if failed_counties:
    print("以下地点的爬虫失败了:")
    for failed_county in failed_counties:
        print(failed_county)
else:
    print("所有地点的爬虫均成功。")
