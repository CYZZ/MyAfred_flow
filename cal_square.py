#coding:utf-8
# use cmd5 api to decode md5
# python script for alfred workflow
# author: LANVNAL
# python2.7

from datetime import datetime
import time
import requests
import re
import sys
# from alfred.feedback import Feedback
from workflow import Workflow3

S = requests.Session()
error_dict = {"0" : "解密失败", "-1" : "无效的用户名密码", "-2" :"余额不足", "-3" : "解密服务器故障", "-4" : "不识别的密文", "-7" :"不支持的类型", "-8" :"api权限被禁止", "-999" :"其它错误"}

REGEXP_MD5 = r'^[0-9a-fA-F]{16,32}$'

def set_params(language,word):
    source_lang = language
    target_lang = "EN" if language == "ZH" else "ZH"

    commonJobParams = {
        "regionalVariant": "en-US",
        "browserType": 1
    }
    if target_lang == "ZH":
        commonJobParams = {
            "browserType": 1
        }
    
    now = time.mktime(datetime.now().timetuple())
    return {
	"jsonrpc": "2.0",
	"method": "LMT_handle_jobs",
	"params": {
            "jobs": [
                {
                    "kind": "default",
                    "sentences": [
                            {
                                "text": word,
                                "id": 0,
                                "prefix": ""
                            }
                    ],
                    "raw_en_context_before": [],
                    "raw_en_context_after": [],
                    "preferred_num_beams": 4,
                    "quality": "fast"
                }
            ],
            "lang": {
                "preference": {
                    "weight": {},
                    "default": "default"
                },
                "source_lang_computed": source_lang,
             	"target_lang": target_lang
            },
            "priority": 1,
            "commonJobParams": commonJobParams,
            "timestamp": now
	},
	"id": 89050025
    }

def trans_from_zh_en(language,word):
    '''
    获取翻译结果
    '''
    url = "https://www2.deepl.com/jsonrpc?method=LMT_handle_jobs"
    headers = {
        "cookie": "dapSid=%7B%22sid%22%3A%2259cd9e6c-0222-427b-870f-9612d4ead25d%22%2C%22lastUpdate%22%3A1660220876%7D",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) / DeepL macOS 3.2.157164",
        "referer": "https://www.deepl.com/",
    }
    params = set_params(language,word)
    json_data = S.post(url=url, json=params,headers=headers).json()
    beams = json_data["result"]["translations"][0]["beams"]
    title = beams.pop(0)["sentences"][0]["text"]
    subtitle =  r'推荐：'
    for beam in beams:
        subtitle += ' /'
        subtitle += beam["sentences"][0]["text"].encode('utf8')
        # abc = ""
        # abc.encode("utf-8")
    subtitle += ' --end'
    return title, subtitle

def baidu_trans(word):
    '''
    百度翻译，自动识别中英文
    支持翻译单词
    '''
    def getArgs(result, subtitle):
        return {
            'title': result,
            'subtitle': subtitle,
            "valid": True,
            'arg': result
        }
    url = "https://fanyi.baidu.com/sug"
    params = {"kw": word}
    # headers = {
    #     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.77"
    # }
    headers = {}
    json = requests.get(url, params=params, headers=headers).json()
    data = json["data"]
    result = [getArgs(obj["k"], obj["v"]) for obj in data]
    # result = [ getArgs("test",str(json))]
    # print(result)
    wf = Workflow3()
    for item in result:
        wf.add_item(**item)
    wf.send_feedback()


def generate_feedback_results(judge_code,result,subtitle):
    wf = Workflow3()
    if(judge_code == 1):
        kwargs = {
                    'title': result,
                    'subtitle': subtitle,
                    "valid": True,
                    'arg': result
                }
    else:
        kwargs = {
                    'title': result,
                    'subtitle': '' ,
                    'valid': False
                }
    wf.add_item(**kwargs)
    wf.send_feedback()



def main():
    language = sys.argv[1]
    word = sys.argv[2]
    if language == "Baidu":
        baidu_trans(word)
        return
    if not (word.endswith("。") or word.endswith(".")):
        generate_feedback_results(0,"请输入句号","")
        return
    value, subtitle = trans_from_zh_en(language,word)
    generate_feedback_results(1,value,subtitle)
    # if md5_value.isdigit():
    #     generate_feedback_results(1,"123")
    # else:
    #     generate_feedback_results(0,"请输入数字。")



if __name__ == "__main__":
    main()