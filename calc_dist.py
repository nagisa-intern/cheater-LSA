import warnings
warnings.filterwarnings('ignore')

from urllib.parse import urlparse
import mysql.connector
import csv
import gensim
import pandas as pd

'''
model = gensim.models.KeyedVectors.load_word2vec_format('../model.vec', binary=False)

#url = urlparse('mysql://comic_user:nagisac2018@localhost:3306/comicdb')
url = urlparse('mysql://bb72568e1ffe6c:9c7cce5f@us-cdbr-iron-east-01.cleardb.net:3306/heroku_5a61d935653267e')

conn = mysql.connector.connect(
    host = url.hostname,
    port = url.port,
    user = url.username,
    password = url.password,
    database = url.path[1:],
)

print(conn.is_connected())
'''

def calc_word_dist(conn, model):
  cur = conn.cursor()
  cur.execute('select like1 from users where id=1')
  data = cur.fetchall()
  print(data[0])

  csv_input = pd.read_csv(filepath_or_buffer="keitaiso.csv", encoding="utf8", sep=",")
  keitaiso = csv_input.values[:,1]
  #print(data)
 
  result = [ [0 for l in range(2)] for u in range(len(keitaiso)) ]
  for i in range(len(keitaiso)):
    sep_data = keitaiso[i].split(" ")
    ans = [0 for p in range(len(sep_data))]
    for j in range(len(sep_data)):
       try:
           ans[j] = model.similarity(data[0], sep_data[j])[0]
       except:
           ans[j] = 0.0
  
    ans.sort()
    ans.reverse()
    ave = 0
    for k in range(5):
      ave += ans[k]
    ave = ave / 5 
    result[i][0] = ave
    result[i][1] = i+1

  result.sort()
  result.reverse()

  json_result = {}
  for i in range(len(result)):
     json_result[i+1] = { "id" :result[i][1]}
	
  return json_result

def calc_page_time(conn, rank):
  print(rank[1]['id'])
  return 0
