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


async def all_feedback():
    main()
    cur.execute(f"SELECT * FROM feedback")
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


async def add_notification_dates(telegram_id, data_olymp, subject, information):
    main()
    cur.execute(f"INSERT INTO notification_dates (telegram_id, data_olymp, subject, information) "
                f"VALUES('{telegram_id}', '{data_olymp}', '{subject}', '{information}')")
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


async def data_olympiads(subject):
    main()
    cur.execute(f"SELECT title, information, start FROM olympiads WHERE subject='{subject}'")
    rows = cur.fetchall()
    con.close()
    return rows


async def select_data_olimp_use_id(telegram_id):
    main()
    cur.execute(f"SELECT data_olymp FROM notification_dates WHERE telegram_id='{telegram_id}'")
    rows = cur.fetchall()
    con.close()
    return rows


async def select_subjects_olimp_use_id(telegram_id):
    main()
    cur.execute(f"SELECT subject FROM notification_dates WHERE telegram_id='{telegram_id}'")
    rows = cur.fetchall()
    con.close()
    return rows


async def select_data_sub_info(telegram_id):
    main()
    cur.execute(f"SELECT data_olymp, subject, information FROM notification_dates WHERE telegram_id='{telegram_id}'")
    rows = cur.fetchall()
    con.close()
    return rows


async def select_data_olimp_use_subject(subject):
    main()
    cur.execute(f"SELECT data_olymp FROM notification_dates WHERE subject='{subject}'")
    rows = cur.fetchall()
    con.close()
    return rows


async def del_data_in_olimpic(telegram_id, subject):
    main()
    cur.execute(
        f"DELETE FROM notification_dates WHERE telegram_id = '{telegram_id}' AND subject = '{subject}'")
    con.commit()
    con.close()


async def del_feedback():
    main()
    cur.execute(
        f"DELETE FROM feedback")
    con.commit()
    con.close()


async def del_notif_in_olimpic(telegram_id, information):
    main()
    cur.execute(
        f"DELETE FROM notification_dates WHERE telegram_id = '{telegram_id}' AND information = '{information}'")
    con.commit()
    con.close()


async def del_tech(tag, help):
    main()
    cur.execute(
        f"DELETE FROM technical_support WHERE telegram_id = '{tag}' AND help = '{help}'")
    con.commit()
    con.close()


async def all_tech_failed():
    main()
    cur.execute(f"SELECT telegram_id, help FROM technical_support")
    rows = cur.fetchall()
    con.close()
    return rows


async def select_data_infor_id():
    main()
    cur.execute(f"SELECT telegram_id, data_olymp, information FROM notification_dates")
    rows = cur.fetchall()
    con.close()
    return rows
