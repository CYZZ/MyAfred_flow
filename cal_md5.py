#coding:utf-8
# use cmd5 api to decode md5
# python script for alfred workflow
# author: LANVNAL
# python2.7

import requests
import re
import sys
# from alfred.feedback import Feedback
from workflow import Workflow3

S = requests.Session()
error_dict = {"0" : "解密失败", "-1" : "无效的用户名密码", "-2" :"余额不足", "-3" : "解密服务器故障", "-4" : "不识别的密文", "-7" :"不支持的类型", "-8" :"api权限被禁止", "-999" :"其它错误"}

REGEXP_MD5 = r'^[0-9a-fA-F]{16,32}$'


def search_from_cmd5(md5_value):
    url = "https://www.cmd5.com/api.ashx?email=your_email&key=your_key&hash={}".format(md5_value)
    query_data = S.get(url=url).text
    return query_data

def show_result(query_data):
    if "CMD5-ERROR" in query_data:
        error_code = re.findall(r'^CMD5-ERROR:(.*)', query_data)
        result = error_dict[str(error_code[0])]
    else:
        result = query_data
    return result


def generate_feedback_results(judge_code,result):
    wf = Workflow3()
    if(judge_code == 1):
        kwargs = {
                    'title': result,
                    'subtitle': '' ,
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
    md5_value = sys.argv[1]
    REGEXP_MD5 = r'^[0-9a-fA-F]{16,32}$'
    if (len(re.findall(REGEXP_MD5, md5_value)) > 0):
        query_data = search_from_cmd5(md5_value)
        result = show_result(query_data)
        generate_feedback_results(1,result)
    else:
        generate_feedback_results(0,"格式错误，确定是MD5?")



if __name__ == "__main__":
    main()