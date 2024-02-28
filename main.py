from hashlib import md5
import random
import time
import requests
from lxml import etree as ET

# 百度翻译API请求URL
URL = "https://fanyi-api.baidu.com/api/trans/vip/translate"

# 填写您的APP ID、密钥和生成的Access Token
APP_ID = "YOUR APP ID"
API_KEY = "YOUR API KEY"

# 函数：调用百度翻译API进行文本翻译
def translate_text(text, from_lang, to_lang):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    salt = random.randint(32768, 65536)
    payload = {
        'appid':APP_ID,
        'q': text,
        'from': from_lang,
        'to': to_lang,
        'salt':salt,
        'sign': ''
    }
    payload['sign'] = md5((APP_ID + text + str(payload['salt']) + API_KEY).encode('utf-8')).hexdigest()
    time.sleep(1)
    response = requests.post(URL, headers=headers, params=payload)
    return response.json()['trans_result'][0]['dst']

def add_comment_before_element(element, comment_text):
    comment = ET.Comment(comment_text)
    parent = element.getparent()
    index = parent.index(element)
    parent.insert(index, comment)

# 函数：将翻译结果添加到XML元素并添加注释
def translate_xml_element(element, text, from_lang, to_lang):
    translated_text = translate_text(text, from_lang, to_lang)
    # 在元素前添加注释
    add_comment_before_element(element,text)
    # 更新元素的文本内容
    element.text = translated_text

# 示例：使用函数翻译XML文件中的元素
def translate_xml_file(file_path, from_lang, to_lang):
    tree = ET.parse(file_path)
    root = tree.getroot()

    for elem in root.iter():
        if elem.text and elem.text != '\n  ':
            #print(elem.text)
            translate_xml_element(elem, elem.text, from_lang, to_lang)

    # 保存修改后的XML文件
    tree.write('translated_' + file_path)

# 调用函数
translate_xml_file('test.xml', 'en', 'zh')
