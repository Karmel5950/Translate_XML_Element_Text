from hashlib import md5
import random
import sys
import time
import requests
from lxml import etree as ET
import configparser

# 在config.ini文件中配置
URL = ""
APP_ID = ""
API_KEY = ""

# 翻译的方向
FROM_LANG = "en"
TO_LANG = "zh"

# 函数：调用百度翻译API进行文本翻译
def translate_text_baidu(text, from_lang, to_lang):
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
    # 百度API如果访问过快会拒绝访问
    time.sleep(1)
    response = requests.post(URL, headers=headers, params=payload)
    return response.json()['trans_result'][0]['dst']

# 函数：在元素前添加注释
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
    #print(translated_text)
    element.text = translated_text

# 示例：使用函数翻译XML文件中的元素
def translate_xml_file(file_path,trans_file_path, from_lang, to_lang):
    tree = ET.parse(file_path)
    root = tree.getroot()

    for elem in root.iter():
        if elem.text and elem.text != '\n  ':
            #print(elem.text)
            translate_xml_element(elem, elem.text, from_lang, to_lang)

    # 保存修改后的XML文件
    tree.write(trans_file_path,encoding='utf-8',xml_declaration=True,pretty_print=True)

def get_config(translate_tool):
    global URL, APP_ID, API_KEY
    config=configparser.ConfigParser()
    config.read('config.ini')
    URL=config[translate_tool]['URL']
    APP_ID=config[translate_tool]['APP_ID']
    API_KEY=config[translate_tool]['API_KEY']

# 支持的翻译方法
TRANSLATE_TOOLS={
    'BAIDU':translate_text_baidu
}

def translate_text(text, from_lang, to_lang,translate_tool='BAIDU'):
    get_config(translate_tool)
    return TRANSLATE_TOOLS[translate_tool](text, from_lang, to_lang)

if __name__ == '__main__':
    # 调用函数
    #translate_xml_file('test.xml','translated_test.xml', FROM_LANG, TO_LANG)
    file_path = sys.argv[1]
    trans_file_path = sys.argv[2]
    translate_xml_file(file_path,trans_file_path, FROM_LANG, TO_LANG)
    print('Done')
