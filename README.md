# 华数杯2024C题数据集收集过程

省流：最终数据集为 [county_data_final_add_temp_clean.csv](https://github.com/Diraw/Data-Collection-Process-for-the-2024-Huashu-Cup-C-Problem/blob/main/county_data_final_add_temp_clean.csv)


## 预处理

1、`附件`文件夹为官方提供的文件夹，`数据处理`为剔除重复值之后的文件夹

## 爬虫

2、**城市规模**使用 https://www.citypopulation.de/zh/china/ 网站进行爬虫，统计`总人口,面积,人口密度`三个指标的数据

使用`crawler_city_scale.py`进行爬虫，csv文件保存为`county_data_city_scale.csv`，可以多下载几次用`script_city_scale_data_merging.py`进行合并，然后用`script_city_scale_missing_data_analysis.py`查询缺失的值，之后可以手动查询

我爬数据的时候陕西省有好多爬失败了，然后有一些根本不是县级市的地名，如（坝上-丰宁，青木川-汉中，武功山-萍乡）

3、**空气质量**使用 https://www.air-level.com/ 网站进行爬虫，统计`AQI值`

使用`crawler_air_quality.py`进行爬虫，csv文件保存为`county_data_air_quality.csv`，

4、为了方便管理，给csv文件加上123的后缀

为了合并顺利，手动将所有的csv的第一列表头改为`城市名称`

5、使用`script_merge_csv.py`对前两个爬虫的结果做合并，保存为`county_data_1_2.csv`

## 自然语言处理

7、使用`script_merge_csv_file_folder.py`对`数据处理`文件夹中的csv文件进行合并，合并为`combined_csv_file.csv`

8、使用`nlp_jibe_word_frequency_search.py`对`介绍`和`小贴士`这两列进行jieba分词，统计词频前1k的词语，保存在`most_common_words.txt`

9、挑选自己需要的关键词，我的选择如下：

> 环境环保:自然: 1793 生态: 1539 森林: 1483 天然: 1347  湿地: 1128 植物: 1121 环境: 1022 草原: 1017 自然保护区: 466
> 
> 人文底蕴:建筑: 5212 历史: 3812 文化: 5365 古代: 935 遗址: 1960 博物馆: 2617 文物: 1224 艺术: 1211 古城: 1107 古镇: 1054  传统: 974
> 
> 交通便利:
> 
> 气候:四季: 511 气候: 404
> 
> 美食:特色: 2391 餐厅: 483 美食: 526 品尝: 325

除`交通便利`方面，均有不错的关键词

10、使用`nlp_2-gram_word_context_searching.py`用2-gram对关键词的上下文进行查询，以此来验证我们关键词选择的可靠性，查询结果保存在`words_context.txt`

11、使用`nlp_word_frequency_statistics.py`对关键词的频次做统计，结果保存在`combined_csv_word_frequency.csv`

12、使用`script_merge_csv_word_frequency.py`对同一城市各景点的结果进行合并，结果保存为`county_data_word_frequency_3.csv`

13、使用`script_merge_csv.py`对爬虫和自然语言处理的结果进行合并，结果保存为`county_data_1_2_3.csv`

## 交通数据

14、队友通过统计年鉴处理好了`交通.csv`，使用`处理字符串.py`剔除双引号，后使用`script_merge_csv.py`合并得到最终的数据集`county_data_final.csv`

## 平均气温

根据上下文，觉得`气候`的关键字不得行，遂找了各城市的平均气温`368个城市平均气温数据（2001-2022年）.xlsx`，使用`excel2csv.py`转成csv文件，使用`tiqu.py`(懒得命名了)将特定两列保存出来为`county_average_temperature.csv`，然后因为两个文件的城市名一个是缩写一个是完整名，使用`hebing.py`进行合并得到`county_data_final_add_temp.csv`，然后用`fill_nan.py`处理完缺失值之后得到最终的数据集`county_data_final_add_temp_clean.csv`

但最终数据集中还是有一些指标不需要的，比如最终哦我们选择删除`总人口,面积`这两列，保留了`人口密度`这一列
