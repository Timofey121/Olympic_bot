import psycopg2

from data.config import POSTGRES_USER, POSTGRES_PASSWORD, HOST

con = psycopg2.connect(user=POSTGRES_USER,
                       # пароль, который указали при установке PostgreSQL
                       password=POSTGRES_PASSWORD,
                       host=HOST,
                       port="5432")
cur = con.cursor()

cur.execute(f"SELECT * FROM olympic_registrationtelegram")
rows = cur.fetchall()
con.close()

print(rows)
