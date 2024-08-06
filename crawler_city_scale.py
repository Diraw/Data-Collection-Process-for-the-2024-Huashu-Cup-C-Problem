import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


def read_counties(file_path):
    """读取县级市集合的CSV文件"""
    return pd.read_csv(file_path)["城市名字"].tolist()


def fetch_province_page(province, base_url):
    """获取省份页面内容"""
    full_url = f"{base_url}{province}/admin"
    try:
        response = requests.get(full_url)
        response.raise_for_status()
        return response.content
    except requests.RequestException as e:
        print(f"请求 {full_url} 失败: {e}")
        return None


def extract_county_data(soup, counties_need, matched_cities, base_url):
    """提取县级市数据"""
    data = []
    table = soup.find("table", {"class": "data"})
    if not table:
        return data

    for row in table.find_all("tr"):
        links = row.find_all("a", href=True)
        for county in counties_need:
            if county in matched_cities:
                continue

            for link in links:
                if (
                    county in str(link)
                    and "admin" in str(link)
                    and "china" in str(link)
                ):
                    print(f"{county} 匹配成功")
                    final_url = f"https://www.citypopulation.de{link.get('href')}"
                    print(f"最终网址是 {final_url}")

                    county_data = fetch_county_data(final_url, county)
                    if county_data:
                        data.append(county_data)
                        matched_cities.add(county)
                        print(f"{county} 已添加至 matched_cities")
                    break
    return data


def fetch_county_data(url, county):
    """获取县级市详细数据"""
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"请求 {url} 失败: {e}")
        return None

    soup = BeautifulSoup(response.content, "html.parser")
    try:
        soup_str = str(
            re.search(
                r"var addChartData = (.*?);</script>", str(soup), re.DOTALL
            ).group(1)
        )
        popularity_1 = re.search(r'"城镇人口",(\d+)', soup_str).group(1)
        popularity_2 = re.search(r'"乡村人口",(\d+)', soup_str).group(1)
        popularity = int(popularity_1) + int(popularity_2)
        print(f"{county} 的总人口为 {popularity}")
    except AttributeError:
        print(f"未能找到 {county} 的人口数据，跳过")
        return None

    td_with_data_area = soup.find("td", {"class": "rname"})
    if td_with_data_area:
        data_area = td_with_data_area.get("data-area")
        data_density = td_with_data_area.get("data-density")
    else:
        data_area = None
        data_density = None

    print(f"{county} 的面积为 {data_area}")
    print(f"{county} 的人口密度为 {data_density}")

    return [county, popularity, data_area, data_density]


def save_data_to_csv(data, file_path):
    """将数据保存到CSV文件"""
    df = pd.DataFrame(data, columns=["县级市", "总人口", "面积", "人口密度"])
    df.to_csv(file_path, index=False)
    print(f"数据已保存到 {file_path}")


def main():
    county_csv = "counties.csv"
    output_csv = "county_data_city_scale.csv"
    base_url = "https://www.citypopulation.de/zh/china/"
    provinces = [
        "anhui",
        "beijing",
        "chongqing",
        "fujian",
        "gansu",
        "guangdong",
        "guangxi",
        "guizhou",
        "hainan",
        "hebei",
        "heilongjiang",
        "henan",
        "hubei",
        "hunan",
        "jiangsu",
        "jiangxi",
        "jilin",
        "liaoning",
        "neimenggu",
        "ningxia",
        "qinghai",
        "shandong",
        "shanghai",
        "shanxi",
        "sichuan",
        "tianjin",
        "xinjiang",
        "xizang",
        "yunnan",
        "zhejiang",
    ]

    counties_need = read_counties(county_csv)
    matched_cities = set()
    all_data = []

    for province in provinces:
        page_content = fetch_province_page(province, base_url)
        if page_content:
            soup = BeautifulSoup(page_content, "html.parser")
            province_data = extract_county_data(
                soup, counties_need, matched_cities, base_url
            )
            all_data.extend(province_data)

    save_data_to_csv(all_data, output_csv)


if __name__ == "__main__":
    main()
