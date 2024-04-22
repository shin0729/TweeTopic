import json
import os
import re
import torch
from transformers import BertJapaneseTokenizer, BertForMaskedLM
def load_tweet():
    path = "/home/syamaguchi/twitter-data/sub/shoiti121109"
    files = os.listdir(path)
    json_files = [i for i in files if i.endswith(".json")]
    print(json_files)
    contents = []
    for file_name in json_files:
        file_path = os.path.join(path, file_name)
        with open(file_path, 'r', encoding="utf_8_sig") as json_file:
            json_load = json.load(json_file)
            # print(json_load)
            json_obj = json_load["data"]
            # print(json_obj)
            for item in json_obj:
                # print(type(item))
                d = item["text"]
                contents.append(d)
    return contents
tweet = load_tweet()
print(len(tweet))


# Load pre-trained tokenizer
tokenizer = BertJapaneseTokenizer.from_pretrained('cl-tohoku/bert-base-japanese-whole-word-masking')
token =[]
for item in tweet:
    token.append(tokenizer.tokenize(item))
print(type(token))

# トークンの前処理
# 記号の削除
code_regex = re.compile('[\t\s!"#$%&\'\\\\()*+,-./:;；：<=>?@[\\]^_`{|}~○｢｣「」〔〕“”〈〉'\
    '『』【】＆＊（）＄＃＠？！｀＋￥¥％♪…◇→←↓↑｡･ω･｡ﾟ´∀｀ΣДｘ⑥◎©︎♡★☆▽※ゞノ〆εσ＞＜┌┘]')
# 数字の削除
num_regex = re.compile('\d+,?\d*')

for i in token:
    for item in i:
        item = code_regex.sub("", item)
        item = num_regex.sub("0", item)
print(token)

