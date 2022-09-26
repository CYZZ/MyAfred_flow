# coding:utf-8


import requests
import sys
from lxml import etree
from workflow import Workflow3


def getIpInfo(ip: str):
    '''
    根据ip获取地址信息，爬取网站的信息
    '''
    url = "http://mip.chinaz.com/?query="+ip
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55'
    }
    page_text = requests.get(url, headers=headers).text
    tree = etree.HTML(page_text)
    addr_xpath = '//*[@id="ip-cont"]/div[3]/table/tbody/tr[3]/td[2]/text()'
    addr_str = tree.xpath(addr_xpath)[0]
    item = {
        'title': addr_str.strip(),
        # 'subtitle': addr_str.strip(),
        "valid": True,
        'arg': addr_str.strip()
    }
    wf = Workflow3()
    wf.add_item(**item)
    wf.send_feedback()

    # difinition_tr_list = tree.xpath('//*[@id="content-body"]/div[1]/div[3]/div/table[2]/tbody/tr')

    # wf = Workflow3()
    # for tr in difinition_tr_list[:6]:
    #     term = tr.xpath('td[@class="tal tm fsl"]/a/text()')[0]


def main():
    if len(sys.argv) > 1:
        word = sys.argv[1]
        getIpInfo(word)
        return
    url = "https://api.myip.com/"
    result = requests.get(url).json()
    ip = result["ip"]
    country = result["country"]
    cc = result["cc"]
    item = {
        'title': "External IP: "+ip,
        'subtitle': country+" / " + cc,
        "valid": True,
        'arg': ip
    }
    wf = Workflow3()
    wf.add_item(**item)
    wf.send_feedback()


if __name__ == "__main__":
    main()
