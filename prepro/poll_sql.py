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

    writer = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)

    writer.writerow(["id", "summary"])
    for i in range(len(data)):
      writer.writerow([ data[i][0], data[i][1] ])
