import pandas as pd
from tqdm import tqdm_notebook as tqdm
import json
import csv
from sudachipy import tokenizer
from sudachipy import dictionary
from sudachipy import config


with open(config.SETTINGFILE, "r", encoding="utf-8") as f:
    settings = json.load(f)
tokenizer_obj = dictionary.Dictionary(settings).create()

#csvファイルに読み込んで一旦データフレームに入れる
file_df = pd.read_csv("detail.csv")
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

for lines in tqdm(file_df['summary']):
    wakati_list.append(wakati_by_sudachi(lines))

#file_df['wakati'] = wakati_list
#file_df.to_csv("detail_wakati.csv")

with open("keitaiso.csv", "w", newline="") as f:

    # 「delimiter」に区切り文字、「quotechar」に囲い文字を指定します
    writer = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)

    writer.writerow(["id", "wakati"])
    for i in range(len(wakati_list)):
      writer.writerow([ i+1, wakati_list[i] ])

