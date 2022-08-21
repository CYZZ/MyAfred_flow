# -*- coding: utf-8 -*-
import sys
import uuid
import requests
import hashlib
import time

# reload(sys)
# sys.setdefaultencoding('utf-8')

YOUDAO_URL = 'https://openapi.youdao.com/api'
APP_KEY = '262666bf9792cab8'
APP_SECRET = 'ECUvZ6Qnsbl9q2e6QVekvWC54CO0iVaN'


def encrypt(signStr):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(signStr.encode('utf-8'))
    return hash_algorithm.hexdigest()


def truncate(q):
    if q is None:
        return None
    q_utf8 = q
    size = len(q_utf8)
    return q_utf8 if size <= 20 else q_utf8[0:10] + str(size) + q_utf8[size - 10:size]


def do_request(data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return requests.post(YOUDAO_URL, data=data, headers=headers)


def youdao_translate(t, word):
    q = word

    data = {}
    data['from'] = 'auto'
    data['to'] = t
    data['signType'] = 'v3'
    curtime = str(int(time.time()))
    data['curtime'] = curtime
    salt = str(uuid.uuid1())
    signStr = APP_KEY + truncate(q) + salt + curtime + APP_SECRET
    sign = encrypt(signStr)
    data['appKey'] = APP_KEY
    data['q'] = q
    data['salt'] = salt
    data['sign'] = sign
    # data['vocabId'] = "您的用户词表ID"

    response = do_request(data).json()
    # print("response=",response)
    return response["translation"][0], "有道单词" if response["isWord"] else "有道句子"

# youdao_translate("en","")