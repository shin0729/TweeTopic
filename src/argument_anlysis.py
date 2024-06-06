import json
import os
import re
import torch
from pyknp import KNP
def load_tweet(person_name):
    path = "/home/syamaguchi/twitter-data/sub/"+person_name+"/"
    # print(path)
    files = os.listdir(path)
    json_files = [i for i in files if i.endswith(".json")]
    # print(json_files)
    contents = []
    num_text = 0
    for file_name in json_files:
        file_path = os.path.join(path, file_name)
        with open(file_path, 'r', encoding="utf_8_sig") as json_file:
            json_load = json.load(json_file)
            # print(json_load)
            if "data" in json_load:
                json_obj = json_load["data"]
                # print(json_obj)
                for item in json_obj:
                    # print(type(item))
                    if "author_id" in item:
                        d = item["text"]
                        contents.append(d)
                        num_text += 1
                    

                else:
                    contents.append("no_tweet")
    return  contents
# tweet = load_tweet()
# print(len(tweet))

def count_leading_numbers(lines):
    count_dict = {}

    for line in lines:
        line = str(line)
        match = re.match(r'^\d+', line)
        if match:
            number = match.group()
            if number in count_dict:
                count_dict[number] += 1
            else:
                count_dict[number] = 1

def augument_anlysis(person_name,**person_tweet):
    # print(person_tweet)
    tweet_list = person_tweet[person_name]
    # print(tweet_list)
    sentence_list = []
    for sentence in tweet_list:
        sentence = preprocessing(sentence)
        knp = KNP(option = '-tab -anaphora', jumanpp=False)
        result = knp.parse(sentence)
        for b in  result.bnst_list():
            match = re.search(r"<項構造:(.+)>", b.spec())
            if match:
                pas =  match.group(1)
                items = pas.split(":")
                print((b.bnst_id,items))
                sentence_list.append((b.bnst_id, items))
    print(sentence_list)
    print(count_leading_numbers(sentence_list))

def preprocessing(sentence):
    # 文の前処理
    #10文字以下の文を空にする
    if len(sentence) <=10:
       sentence = " "
    else:
        # 記号の削除
        code_regex = re.compile('[\t\s!"#$%&\'\\\\()*+,-./:;；：<=>?@[\\]^_`{|}~○｢｣「」〔〕“”〈〉'\
            '『』【】＆＊（）＄＃＠？！｀＋￥¥％♪…◇→←↓↑｡･ω･｡ﾟ´∀｀ΣДｘ⑥◎©︎♡★☆▽※ゞノ〆εσ＞＜┌┘]')
        # 数字の削除
        num_regex = re.compile('\d+,?\d*')
        sentence = code_regex.sub("", sentence)
        sentence = num_regex.sub("0", sentence)
    return sentence
       

def main():
    folder_path = "/home/syamaguchi/twitter-data/sub/"
    files = os.listdir(folder_path)
    # print(files)
    person_tweet = {}
    # for i in files:
    #     # print(i)
    #     person_tweet[i] = load_tweet(i)
    #     print(person_tweet)
    for i in range(1):
        # print(i)
        person_tweet[files[i]] = load_tweet(files[i])
        augument_anlysis(files[i],**person_tweet)

if __name__ == "__main__":
    main()