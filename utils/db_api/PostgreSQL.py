# -*- coding: utf8 -*-
import sqlite3


def main():
    global con, cur

    con = sqlite3.connect('additional_files/olimpic_bd')
    cur = con.cursor()


async def add_user(telegram_id, full_name, blocked, data_registration):
    main()
    cur.execute(
        f"INSERT INTO registration (telegram_id, full_name, blocked, data_registration) VALUES('{telegram_id}', '{full_name}', '{blocked}', '{data_registration}')")
    con.commit()
    con.close()


async def select_all_users():
    main()
    cur.execute(f"SELECT * FROM registration WHERE blocked='Нет'")
    rows = cur.fetchall()
    con.close()
    return rows


async def subscriber_exists(telegram_id):
    main()
    cur.execute(f"SELECT * FROM registration WHERE telegram_id='{telegram_id}'")
    rows = cur.fetchall()
    con.close()
    return rows


async def count_users():
    main()
    cur.execute(f"SELECT COUNT(*) FROM registration WHERE blocked='Нет'")
    rows = cur.fetchall()
    con.close()
    return rows


async def add_user_feedback(telegram_id, feedback):
    main()
    cur.execute(f"INSERT INTO feedback (telegram_id, feedback) VALUES('{telegram_id}', '{feedback}')")
    con.commit()
    con.close()


async def add_user_tech(telegram_id, help):
    main()
    cur.execute(f"INSERT INTO technical_support (telegram_id, help) VALUES('{telegram_id}', '{help}')")
    con.commit()
    con.close()


async def check_blocked(telegram_id):
    main()
    cur.execute(f"SELECT blocked FROM registration WHERE telegram_id='{telegram_id}'")
    rows = cur.fetchall()
    con.close()
    return rows


async def update_blocked_users(telegram_id, blocked):
    main()
    cur.execute(
        f"UPDATE registration SET blocked='{blocked}' WHERE telegram_id='{telegram_id}'")
    con.commit()
    con.close()


async def select_blocked_users():
    main()
    cur.execute(f"SELECT * FROM registration WHERE blocked='Да'")
    rows = cur.fetchall()
    con.close()
    return rows


async def information_about_olympiads(subject):
    main()
    cur.execute(f"SELECT title, information FROM olympiads WHERE subject='{subject}'")
    rows = cur.fetchall()
    con.close()
    return rows
