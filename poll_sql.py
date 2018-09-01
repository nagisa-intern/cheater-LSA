from urllib.parse import urlparse
import mysql.connector

url = urlparse('mysql://comic_user:nagisac2018@localhost:3306/comicdb')

conn = mysql.connector.connect(
    host = url.hostname,
    port = url.port,
    user = url.username,
    password = url.password,
    database = url.path[1:],
)

print(conn.is_connected())
