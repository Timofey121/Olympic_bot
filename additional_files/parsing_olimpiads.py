# import psycopg2
import asyncio
import datetime
import sqlite3

import requests
from aiogram.utils.markdown import hlink, hunderline, hbold
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from xvfbwrapper import Xvfb

from additional_files.dictionary import numbers, months, months2, subjects_rsosh
from utils.db_api.PostgreSQL import select_info, select, select_yes_or_no_in_notifications, add_notification_dates


def connection_to_bd(host, user, passwd, database):
    global connection, cur
    connection = sqlite3.connect('additional_files/olimpic_bd')
    cur = connection.cursor()


async def add_subject(subject, title, information, start):
    connection_to_bd('host', 'user', 'passwd', 'database')
    cur.execute(f"INSERT INTO olympiads (subject, title, information, start) VALUES ('{subject}', '{title}', "
                f"'{information}', '{start}')")
    connection.commit()
    connection.close()


async def delete_subject(subject):
    connection_to_bd('host', 'user', 'passwd', 'database')
    cur.execute(f"DELETE FROM olympiads WHERE subject = '{subject}'")
    connection.commit()
    connection.close()


async def subject_to_bd():
    subjects = 'Информатика, Математика, Физика, Химия, Биология, География, История, Обществознание, Право, ' \
               'Экономика, Русский язык, Литература, Английский язык, ' \
               'Французский язык, Немецкий язык, Астрономия, Робототехника, ' \
               'Технология, Искусство, Черчение, Психология'.split(', ')
    for i in range(len(subjects)):
        try:
            await delete_subject(subject=subjects[i])
            vdisplay = Xvfb()
            vdisplay.start()
            data_start = ''
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            options.add_argument('--no-sandbox')
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--no-sandbox")
            options.add_argument('--start-maximized')
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            URL = f'https://olimpiada.ru/activities?type=any&subject%5B{numbers[subjects[i].strip().capitalize()]}' \
                  f'%5D=on&class=any&period_date=&period=week'
            driver.get(URL)

            for j in range(10):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                await asyncio.sleep(0.05)

            html = driver.page_source
            driver.close()
            vdisplay.stop()

            soup = BeautifulSoup(html, "lxml")

            a = soup.find_all('a', 'none_a black olimp_desc')
            for item in a:
                try:
                    url = "https://olimpiada.ru" + item.get('href')
                    req = requests.get(url=url)
                    src = req.text
                    soup = BeautifulSoup(src, "lxml")
                    title = soup.find_all('title')[0].text.strip()

                    href_olimp = soup.find_all('div', 'contacts')[0].find('a', 'color').get('href')

                    fg = "https://olimpiada.ru" + soup.find_all('tr', 'notgreyclass')[0].find("a").get('href')

                    if fg != 'Расписание олимпиады в этом году пока не известно':
                        url = fg
                        req = requests.get(url=url)
                        src = req.text
                        soup = BeautifulSoup(src, "lxml")

                        step = soup.find('div', 'right').find('h1').text
                        data_start1 = (soup.find('span', 'main_date red').text.strip().replace('\n', '')
                                       .replace('20', ' 20').replace('!', '').replace('До', '')
                                       ).strip().replace(' ', ' ').split('...')[0]

                        for item2 in months2:
                            if item2 in data_start1:
                                data_start1 = data_start1.split(item2.strip())
                                if len(data_start1[0]) == 0:
                                    data_start1 = data_start1[1]

                                data_start = f"{data_start1[-1].strip()}-{months[item2.strip()]}-" \
                                             f"{('0' * (2 - len(data_start1[0].strip())))}{data_start1[0].split('-')[0].strip()}"

                        information_about_olimpiad = (f"{hunderline(title)}.  \n"
                                                      f"Этап олимпиады - {hbold(step)} \n"
                                                      f"{data_start} \n"
                                                      f"Расписание можете посмотреть {hlink(title='ТУТ!', url=fg)}\n"
                                                      f"Сайт этой олимпиады Вы можете посмотреть"
                                                      f"{hlink(title='ТУТ!', url=href_olimp)}  \n")
                        data = datetime.datetime.strptime(''.join(data_start.split("-")), '%Y%m%d').date()
                        now = datetime.datetime.strptime(datetime.datetime.today().strftime('%Y%m%d'), '%Y%m%d').date()
                        if data > now:
                            await add_subject(subject=subjects[i], title=title, information=information_about_olimpiad,
                                              start=data_start.strip().split(' - ')[0].replace('-До', ''))

                            gen = set(list(await select_info(subjects[i])))
                            for tg in gen:
                                if len(await select_yes_or_no_in_notifications(tg[0], information_about_olimpiad)) == 0:
                                    f = (title in subjects_rsosh[subjects[i].lower().capitalize()])
                                    if 'no' in str(list(await select(tg[0], subjects[i]))[0]):
                                        flag = False
                                        a = 'no'
                                    else:
                                        flag = True
                                        a = 'yes'
                                    if (flag is False) or (f is True and flag is True):
                                        await add_notification_dates(telegram_id=tg[0], data_olymp=data_start,
                                                                     subject=subjects[i],
                                                                     information=information_about_olimpiad, rsoch=a)

                except Exception as ex:
                    pass
        except Exception as ex:
            pass


async def main():
    while True:
        start = datetime.datetime.now()
        await subject_to_bd()
        with open('additional_files/log.txt', 'w') as f:
            f.write(f"{datetime.datetime.today().date()};{str(datetime.datetime.now() - start).split('.')[0]}")
        await asyncio.sleep(432000)


asyncio.run(main())
