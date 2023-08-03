import psycopg2

from data.config import POSTGRES_USER, POSTGRES_PASSWORD, HOST

con = psycopg2.connect(user=POSTGRES_USER,
                       # пароль, который указали при установке PostgreSQL
                       password=POSTGRES_PASSWORD,
                       host=HOST,
                       port="5432")
cur = con.cursor()

cur.execute(f"SELECT * FROM olympic_feedback")
rows = cur.fetchall()
print(rows)

cur.execute(
    f"INSERT INTO olympic_feedback (user, feedback) VALUES('fdg', 'dfsgh')")
con.commit()
con.close()
