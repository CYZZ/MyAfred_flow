# coding:utf-8
from lxml import etree
import requests
import aiohttp
import asyncio
from aiohttp import ClientSession
from hashlib import md5
from workflow import Workflow3
import sys
import time


async def request_with_aio(url, headers):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=headers, ssl=False) as response:
            text = await response.text()
            return text


def get_html_string(url, headers):
    return asyncio.run(request_with_aio(url, headers))


async def translator(word: str, f="en"):
    appid = "20220811001303267"
    salt = "1435660288"
    key = "78BbFaUdV8LroJwnbzw8"
    sign = md5((appid+word+salt+key).encode('utf-8')).hexdigest()
    url = "https://fanyi-api.baidu.com/api/trans/vip/translate"
    params = {
        "from": f,
        "to": "zh" if f == "en" else "en",
        "q": word,
        "appid": appid,
        "salt": salt,
        "sign": sign
    }
    async with ClientSession() as session:
        async with session.get(url=url, params=params) as response:
            response_data = await response.json()
            # print("responsedst=",response_data["trans_result"][0]["dst"])
            return response_data["trans_result"][0]["dst"]

def my_workflow(func):
    def wrapper(*args, **kwargs):
        text = func(*args, **kwargs)
        page_text = text
        # 数据解析
        tree = etree.HTML(page_text)
        difinition_tr_list = tree.xpath('//*[@id="content-body"]/div[1]/div[3]/div/table/tbody/tr')

        wf = Workflow3()
        items = []
        for tr in difinition_tr_list:
            term = tr.xpath('td[@class="tal tm fsl"]/a/text()')[0]
            definition = tr.xpath('td[@class="tal dx fsl"]/p[@class="desc"]/text()')[0]
            star = tr.xpath('td[@class="tal vam rt nowrap"]/span[@class="sc rate-stars"]/span[@class="sf"]')
            star = len(star)
            star = "⭐️" * star
            item = {
                'title': definition,
                'subtitle': term + " " + str(star),
                "valid": True,
                'arg': definition,
            }
            items.append(item)
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError as e:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        tasks = [asyncio.ensure_future(translator(item["title"])) for item in items[0:10]]
        # loop = asyncio.get_event_loop()
        result = loop.run_until_complete(asyncio.gather(*tasks))
        loop.close()
        for idx, item in enumerate(items):
            if idx < len(result):
                item['subtitle'] = item['subtitle'] + ":" + result[idx]
            wf.add_item(**item)
        wf.send_feedback()
        return text
    return wrapper


@my_workflow
def getAbbreviations(word):
    star_time = time.time()
    # 获取单词缩写的详细描述，
    url = 'https://www.abbreviations.com/' + word
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55'
    }
    # response = requests.get(url=url, headers=headers)
    text = get_html_string(url, headers)
    return text
    page_text = text
    # 数据解析
    tree = etree.HTML(page_text)
    difinition_tr_list = tree.xpath('//*[@id="content-body"]/div[1]/div[3]/div/table[2]/tbody/tr')

    wf = Workflow3()
    for tr in difinition_tr_list:
        term = tr.xpath('td[@class="tal tm fsl"]/a/text()')[0]
        definition = tr.xpath('td[@class="tal dx fsl"]/p[@class="desc"]/text()')[0]
        item = {
            'title': definition,
            'subtitle': term,
            "valid": True,
            'arg': definition,
        }
        wf.add_item(**item)
    time_item = item = {
        'title': "Time Spent",
        'subtitle': "{}s".format(time.time() - star_time),
        "valid": True,
        'arg': "",
    }
    wf.add_item(**time_item)
    wf.send_feedback()


def main():
    word = sys.argv[1]
    getAbbreviations(word)


if __name__ == "__main__":
    main()
