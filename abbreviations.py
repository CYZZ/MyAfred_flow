#coding:utf-8
from lxml import etree
import requests
from workflow import Workflow3
import sys


def getAbbreviations(word):
    # 获取单词缩写的详细描述，
    url = 'https://www.abbreviations.com/' + word
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55'
    }
    response = requests.get(url=url, headers=headers)
    page_text = response.text
    # 数据解析
    tree = etree.HTML(page_text)
    difinition_tr_list = tree.xpath('//*[@id="content-body"]/div[1]/div[3]/div/table[2]/tbody/tr')

    wf = Workflow3()
    for tr in difinition_tr_list[:6]:
        term = tr.xpath('td[@class="tal tm fsl"]/a/text()')[0]
        definition = tr.xpath('td[@class="tal dx fsl"]/p[@class="desc"]/text()')[0]
        item = {
            'title': term,
            'subtitle': definition,
            "valid": True,
            'arg': definition
        }
        wf.add_item(**item)
    wf.send_feedback()


def main():
    word = sys.argv[1]
    getAbbreviations(word)


if __name__ == "__main__":
    main()
