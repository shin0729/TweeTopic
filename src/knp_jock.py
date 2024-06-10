import re
from pyknp import KNP


def analyze_pas(sentence):
    knp = KNP(option = '-tab -anaphora', jumanpp=False)
    result = knp.parse(sentence)
    for b in  result.bnst_list():
        match = re.search(r"<項構造:(.+)>", b.spec())
        if match:
            pas =  match.group(1)
            items = pas.split(":")
            print(b.bnst_id, items)

sentence1 = "日本社会はジョック・ヤングがブレミア・ソサイエティと呼ぶ過剰包摂社会になっていきました。これは、過剰包摂社会の結果として高所得者と低所得者の間での消費行動の差異が小さくなったことを示しています。"
sentence2 ="日本の社会はジョック・ヤングがブレミア・ソサイエティと呼ぶ「みんなが同じように買い物する社会」になっていきました。これは、お金持ちの人とあまりお金を持っていない人との間での買い物の違いが小さくなったことを示しています。" 
analyze_pas(sentence1)
print("-------------------------------------------------")
analyze_pas(sentence2)