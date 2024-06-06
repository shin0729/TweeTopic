import json
import os
import re
import torch
from transformers import BertJapaneseTokenizer, BertForMaskedLM
from pyknp import KNP

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
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
docs =[]
for item in tweet:
    docs.append(tokenizer.tokenize(item))
print(type(docs))

# トークンの前処理
# 記号の削除
code_regex = re.compile('[\t\s!"#$%&\'\\\\()*+,-./:;；：<=>?@[\\]^_`{|}~○｢｣「」〔〕“”〈〉'\
    '『』【】＆＊（）＄＃＠？！｀＋￥¥％♪…◇→←↓↑｡･ω･｡ﾟ´∀｀ΣДｘ⑥◎©︎♡★☆▽※ゞノ〆εσ＞＜┌┘]')
# 数字の削除
num_regex = re.compile('\d+,?\d*')

for i in docs:
    for item in i:
        item = code_regex.sub("", item)
        item = num_regex.sub("0", item)
print(docs)

from gensim.models import Phrases
bigram = Phrases(docs, min_count=20)
for idx in range(len(docs)):
    for token in bigram[docs[idx]]:
        if '_' in token:
            # Token is a bigram, add to document.
            docs[idx].append(token)
print(token)


# Remove rare and common tokens.
from gensim.corpora import Dictionary

# Create a dictionary representation of the documents.
dictionary = Dictionary(docs)

# Filter out words that occur less than 20 documents, or more than 50% of the documents.
dictionary.filter_extremes(no_below=20, no_above=0.5)

# Bag-of-words representation of the documents.
corpus = [dictionary.doc2bow(doc) for doc in docs]

print('Number of unique tokens: %d' % len(dictionary))
print('Number of documents: %d' % len(corpus))

# Train LDA model.
from gensim.models import LdaModel

# Set training parameters.
num_topics = 10
chunksize = 2000
passes = 20
iterations = 400
eval_every = None  # Don't evaluate model perplexity, takes too much time.

# Make an index to word dictionary.
temp = dictionary[0]  # This is only to "load" the dictionary.
id2word = dictionary.id2token

model = LdaModel(
    corpus=corpus,
    id2word=id2word,
    chunksize=chunksize,
    alpha='auto',
    eta='auto',
    iterations=iterations,
    num_topics=num_topics,
    passes=passes,
    eval_every=eval_every
)

top_topics = model.top_topics(corpus)

# Average topic coherence is the sum of topic coherences of all topics, divided by the number of topics.
avg_topic_coherence = sum([t[1] for t in top_topics]) / num_topics
print('Average topic coherence: %.4f.' % avg_topic_coherence)

from pprint import pprint
pprint(top_topics)
