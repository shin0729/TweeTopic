import json
import os
import re
import torch
from transformers import BertJapaneseTokenizer, BertForMaskedLM
# トークナイザーの読み込み
tokenizer = BertJapaneseTokenizer.from_pretrained('cl-tohoku/bert-base-japanese-whole-word-masking')

# トークナイズする文
sentences = []
sentences.append("日本社会はジョック・ヤングがブレミア・ソサイエティと呼ぶ過剰包摂社会になっていきました。これは、過剰包摂社会の結果として高所得者と低所得者の間での消費行動の差異が小さくなったことを示しています。年収200万円の人と年収2億円の人が同じようなスターバックスでラテを飲んでいて、ユニクロやギャップで買った服を着ているというような状態になっていったのです。")
sentences.append("日本の社会は、ジョック・ヤングという人が『過剰包摂社会』と呼ぶ状態になってきました。これは、お金持ちの人もあまりお金を持っていない人も、同じようなお店で買い物をしたり、同じようなものを飲んだりするようになったことを意味します。例えば、年収200万円の人と年収2億円の人が同じスターバックスでラテを飲み、ユニクロやギャップで買った服を着ているという感じです。")
sentences.append("日本の社会は、ジョック・ヤングという人が『みんな一緒』と言うような状態になってきました。これは、お金持ちの人もあまりお金を持っていない人も、同じようなお店で買い物をしたり、同じような飲み物を飲んだりするようになったということです。たとえば、年収200万円の人と年収2億円の人が同じスターバックスでラテを飲んだり、ユニクロやギャップで買った服を着たりするようになったということです。")
# トークナイズされた文を格納するリスト
for sentence in sentences:
    tokenized_sentence = tokenizer.tokenize(sentence)
    # トークナイズされた文を表示
    print(tokenized_sentence)



