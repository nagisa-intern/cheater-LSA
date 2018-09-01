from urllib.parse import urlparse
import mysql.connector
import csv

url = urlparse('mysql://comic_user:nagisac2018@localhost:3306/comicdb')

conn = mysql.connector.connect(
    host = url.hostname,
    port = url.port,
    user = url.username,
    password = url.password,
    database = url.path[1:],
)

print(conn.is_connected())

cur = conn.cursor()
cur.execute('select id, summary from comics')
data = cur.fetchall()

print(data)

with open("detail.csv", "w", newline="") as f:

    # 「delimiter」に区切り文字、「quotechar」に囲い文字を指定します
    # quotingにはクォーティング方針を指定します（後述）
    writer = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)

    # writerowに行列を指定することで1行分を出力できます
    writer.writerow(["id", "summary"])
    for i in range(len(data)):
      writer.writerow([ data[i][0], data[i][1] ])
