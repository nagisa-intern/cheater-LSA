import warnings
warnings.filterwarnings('ignore')

from urllib.parse import urlparse
from flask import Flask, jsonify, abort, make_response
import gensim
import mysql.connector
from calc_dist import calc_word_dist
from calc_dist import calc_page_time

model  =  gensim.models.KeyedVectors.load_word2vec_format('../model.vec', binary=False)

url = urlparse('mysql://comic_user:nagisac2018@localhost:3306/comicdb')
#url = urlparse('mysql://bb72568e1ffe6c:9c7cce5f@us-cdbr-iron-east-01.cleardb.net:3306/heroku_5a61d935653267e')

conn = mysql.connector.connect(
    host = url.hostname,
    port = url.port,
    user = url.username,
    password = url.password,
    database = url.path[1:],
)

#Flaskクラスのインスタンスを作成
# __name__は現在のファイルのモジュール名
api = Flask(__name__)

# GETの実装
@api.route('/get', methods=['GET'])
def get():
    ans = calc_word_dist(conn, model)
    #print(ans)    
    result = calc_page_time(conn, ans)
    return make_response(jsonify(rank=result))
    #result = ans
    #return make_response(jsonify(result))

# エラーハンドリング
@api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

# ファイルをスクリプトとして実行した際に
# ホスト0.0.0.0, ポート3001番でサーバーを起動
if __name__ == '__main__':
    api.run(host='0.0.0.0', port=3001)
