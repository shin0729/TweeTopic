import json
import os
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
print(tweet)
