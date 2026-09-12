import pytest
from main import calc_similarity

#1.完全相同文本
def test_1_same():
    a = "今天是星期天，天气晴"
    b = "今天是星期天，天气晴"
    assert calc_similarity(a,b) > 0.95

#2.完全不同文本
def test_2_diff():
    a = "苹果香蕉"
    b = "汽车火车"
    assert calc_similarity(a,b) < 0.1

#3.原文为空
def test_3_empty_orig():
    a = ""
    b = "测试文字"
    assert calc_similarity(a,b) == 0.0

#4.抄袭文本为空
def test_4_empty_copy():
    a = "测试文字"
    b = ""
    assert calc_similarity(a,b) == 0.0

#5.少量改写
def test_5_small_change():
    a = "今天天气很好"
    b = "今日天气很好"
    assert calc_similarity(a,b) > 0.6

#6.长文本部分重复
def test_6_long_text():
    a = "计算机科学是一门研究信息的学科，包含算法编程"
    b = "软件工程研究项目开发，包含算法编程"
    res = calc_similarity(a,b)
    assert 0.2 < res < 0.8

#7.标点差异
def test_7_punct():
    a = "你好，世界。"
    b = "你好世界"
    assert calc_similarity(a,b) >0.7

#8.全部是标点
def test_8_all_punct():
    a = "，。！？"
    b = "！？"
    assert calc_similarity(a,b) == 0.0

#9.原文基础上增加大量无关内容
def test_9_add_more():
    a = "今天去看电影"
    b = "早上起床，吃饭，今天去看电影，晚上回家睡觉"
    assert calc_similarity(a,b) >0.4

#10.词语顺序打乱
def test_10_word_order():
    a = "小明爱吃苹果"
    b = "苹果小明爱吃"
    assert calc_similarity(a,b) >0.6
