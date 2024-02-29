# Translate XML Element Text
通过翻译API直接翻译XML文件中的元素值文本

# 安装依赖

python version >= 3.7

```
pip install -r requirements.txt
```

# 使用
将配置文件`config_example.ini`修改文件名为`config.ini`,并填写配置信息

然后通过以下命令行使用
```
python main.py FILE_PATH TRANS_FILE_PATH
```

# TODO LIST

1. 增加支持更多在线API的方法
2. 增加支持离线大模型翻译的方法
3. 支持批量翻译文件的方法