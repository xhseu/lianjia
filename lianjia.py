#!usr/bin/python
"""
@Project ：python_code 
@File    ：lianjia.py
@Author  ：xx
@Date    ：xx
"""

import requests
from bs4 import BeautifulSoup
import random
import time
import csv

def get_page_content(url):
    """
    :param url: 单页的url
    :return: 单页的内容
    """
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.58',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/548.39 (KHTML, like Gecko) Chrome/104.0.234 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/598.45 (KHTML, like Gecko) Chrome/103.0.2647 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/585.54 (KHTML, like Gecko) Chrome/92.0.2667 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/585.52 (KHTML, like Gecko) Chrome/93.0.2005 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.70',
        'Mozilla/5.0 (Windows NT 9_1_2; Win64; x64) AppleWebKit/600.48 (KHTML, like Gecko) Chrome/95.0.1729 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.99 Vulcan/0.3.0.1 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.74 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.78',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Core/1.94.182.400 QQBrowser/11.3.5182.400',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Core/1.94.168.400 QQBrowser/11.0.5120.400',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) tcs_app/3.7.3 Chrome/94.0.4606.81 TCS/3.7.3 TTTCS/3.7.3 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.39',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.105 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4482.0 Safari/537.36 Edg/92.0.874.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36',
    ]
    agent = random.choice(user_agents)
    headers = {
                  'User-Agent': agent,
                  'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
                  'Accept-Encoding': 'gzip, deflate, br',
                  'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
    }

    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.encoding = 'utf-8'
    except Exception as e:
        print(f"req fail for url{url} err {e}")
        return None
    return response.text


def parse_page_content(text, csv_writer, data_file):
    """
    从首页的内容上解析出想要的信息写入文件，包括 小区名称、单位面积均价、建成年代、户数、物业费
    :param text: 首页的内容
    :param csv_writer: 文件写入工具
    """
    info_keys = ['建成年代', '房屋总数', '物业费']
    soup = BeautifulSoup(text, 'html.parser')
    community_list = soup.find_all('div', class_='title')
    # print(community_list)
    succ_num = 0
    fail_num = 0
    for community in community_list:
        print(community)

        res_dict = dict(
            {
                '小区名称': "暂无信息",
                '单位面积均价': "暂无信息",
                '建成年代': "暂无信息",
                '房屋总数': "暂无信息",
                '物业费': "暂无信息",
            }
        )
        time.sleep(random.randint(1, 3))  # 操作之间加入随机间隔时，避免程序操作太快被逮住
        try:
            tag = community.find('a')
            name = tag.get_text()
            res_dict['小区名称'] = name
            href = tag.get('href')
            res_dict['详情页'] = href
            href_content = get_page_content(href)
            soup = BeautifulSoup(href_content, 'html.parser')
            info = soup.find('div', class_='xiaoquOverview')
            unit_price = info.find('span', class_='xiaoquUnitPrice')
            if unit_price is None:
                res_dict['单位面积均价'] = "暂无数据"
            else:
                res_dict['单位面积均价'] = unit_price.text
            item_infos = info.find_all('div', class_='xiaoquInfoItem')
            ourter_item_infos1 = info.find_all('div', class_='xiaoquInfoItem ourterItem')
            all_infos = item_infos + ourter_item_infos1
            for part_info in all_infos:
                if part_info is None:
                    continue
                info_label = part_info.find('span', class_='xiaoquInfoLabel')
                if info_label.text in info_keys:
                    info_content = part_info.find('span', class_='xiaoquInfoContent')
                    res_dict[info_label.text] = info_content.text
        except Exception as e:
            print(f"get community {community} info fail {e}, turn to next")
            fail_num += 1

        if len(res_dict) > 0:
            print(res_dict)
            if '详情页' in res_dict.keys() and res_dict['详情页'] is not None:
                csv_writer.writerow(res_dict)
                data_file.flush()
                succ_num += 1

    return succ_num, fail_num


if __name__ == '__main__':
    with open('house_data2.csv', mode='a', encoding='utf-8', newline='') as data_file:
        csv_writer = csv.DictWriter(data_file, fieldnames=[
            '小区名称',
            '单位面积均价',
            '建成年代',
            '房屋总数',
            '物业费',
            '详情页'
        ])
        csv_writer.writeheader()

        for i in range(0, 5):
            url = f"https://nj.lianjia.com/xiaoqu/pg{i}/?from=rec"
            if i == 1:
                url = "https://nj.lianjia.com/xiaoqu/?from=rec"
            print(f"----start get page {i} info-----")
            res = get_page_content(url)
            #print(res)
            succ, fail = parse_page_content(res, csv_writer, data_file)
            print(f"----end get page {i} info succ {succ} fail {fail}-----")
