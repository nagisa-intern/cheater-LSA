import pandas as pd
from tqdm import tqdm_notebook as tqdm
import json
from sudachipy import tokenizer
from sudachipy import dictionary
from sudachipy import config


with open(config.SETTINGFILE, "r", encoding="utf-8") as f:
    settings = json.load(f)
tokenizer_obj = dictionary.Dictionary(settings).create()

#csvファイルに読み込んで一旦データフレームに入れる
file_df = pd.read_csv("hoge.csv")
wakati_list=[]

def wakati_by_sudachi(text):
    mode = tokenizer.Tokenizer.SplitMode.C #モードCの一番長い形で分ける
    results =[m.surface() for m in tokenizer_obj.tokenize(mode, text)]
    word_list = []
    for mrph in results:
        if not (mrph == ""):
            seikika = tokenizer_obj.tokenize(mode,mrph)[0].normalized_form() 
            hinsi = tokenizer_obj.tokenize(mode,seikika)[0].part_of_speech()[0]
            if hinsi in  ["名詞", "動詞", "形容詞"]:  # 対象とする品詞を指定
                word = tokenizer_obj.tokenize(mode,seikika)[0].dictionary_form()
                word_list.append(word)
    return " ".join(word_list)

for lines in tqdm(file_df['text']):
    wakati_list.append(wakati_by_sudachi(lines))

file_df['wakati'] = wakati_list
file_df.to_csv("hoge_wakati.csv")
