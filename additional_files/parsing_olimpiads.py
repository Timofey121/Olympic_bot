# import psycopg2
import asyncio
import sqlite3

import requests
from aiogram.utils.markdown import hlink, hunderline, hbold
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from xvfbwrapper import Xvfb

from additional_files.dictionary import numbers, months


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
               'Экономика, Русский язык, Литература, Английский язык, Испанский язык, ' \
               'Французский язык, Немецкий язык, Астрономия, Робототехника, ' \
               'Технология, Искусство, Черчение, Психология, Физкультура'.split(', ')
    for i in range(len(subjects)):
        try:
            await delete_subject(subject=subjects[i])
            data_start = ''
            vdisplay = Xvfb()
            vdisplay.start()
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            options.add_argument('--no-sandbox')
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            URL = f'https://olimpiada.ru/activities?type=any&subject%5B{numbers[subjects[i].strip().capitalize()]}' \
                  f'%5D=on&class=any&period_date=&period=week'

            driver.get(URL)

            for j in range(10):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                await asyncio.sleep(0.05)

            html = driver.page_source
            soup = BeautifulSoup(html, "lxml")

            driver.close()
            vdisplay.stop()

            a = soup.find_all('a', 'none_a black olimp_desc')
            for item in a:
                try:
                    url = "https://olimpiada.ru" + item.get('href')
                    req = requests.get(url=url)
                    src = req.text
                    soup = BeautifulSoup(src, "lxml")
                    title = soup.find_all('title')[0].text.strip()

                    href_olimp = soup.find_all('div', 'contacts')[0].find('a', 'color').get('href')

                    try:
                        fg = "https://olimpiada.ru/" + soup.find('a', "blue ei-a").get(
                            'href')
                    except Exception:
                        try:
                            fg = "https://olimpiada.ru/" + soup.find('div', 'event_name').parent.get(
                                'href')
                        except Exception:
                            try:
                                fg = "https://olimpiada.ru/" + soup.find('span',
                                                                         'events-info ei-link').text
                            except Exception:
                                fg = "Расписание олимпиады в этом году пока не известно"

                    if fg != 'Расписание олимпиады в этом году пока не известно':
                        url = fg
                        req = requests.get(url=url)
                        src = req.text
                        soup = BeautifulSoup(src, "lxml")

                        step = soup.find('div', 'right').find('h1').text

                        try:
                            data = soup.find('span', 'main_date grey').find('font').text
                        except Exception:
                            data = soup.find('span', 'main_date red').find('font').text

                        try:
                            data_start = soup.find_all('span', 'month fleft')[1].text + '-' + months[
                                soup.find_all('span', 'month fleft')[0].text] + '-' + data.split('...')[0]
                        except:
                            try:
                                data_start = soup.find_all('span', 'month fleft')[1].text + '-' + months[
                                    soup.find_all('span', 'month fleft')[0].text] + '-' + data.split(' - ')[0]
                            except:
                                try:
                                    data_start = soup.find_all('span', 'month')[2].text + '-' + months[
                                        soup.find_all('span', 'month fleft')[0].text] + '-' + data.split('...')[0]
                                except:
                                    try:
                                        data_start = soup.find_all('span', 'month')[1].text + '-' + months[
                                            soup.find('span', 'main_date grey').find_all('td')[1].find('font').text]
                                    except:
                                        try:
                                            data_start = soup.find_all('span', 'month')[2].text + '-' + months[
                                                soup.find_all('span', 'month fleft')[0].text] + '-' + \
                                                         data.split(' - ')[0]
                                        except:
                                            try:
                                                data_start = soup.find_all('span', 'month')[1].text + '-' + months[
                                                    soup.find_all('span', 'month')[0].text] + '-' + data
                                            except:
                                                pass

                        try:
                            data_end = soup.find_all('span', 'month fright')[1].text + '-' + months[
                                soup.find_all('span', 'month fright')[0].text] + '-' + data.split('...')[1]
                        except:
                            try:
                                data_end = soup.find_all('span', 'month fright')[1].text + '-' + months[
                                    soup.find_all('span', 'month fright')[0].text] + '-' + data.split(' - ')[1]
                            except:
                                try:
                                    data_end = soup.find_all('span', 'month')[1].text + '-' + \
                                               months[soup.find('span', 'month fright').text] + '-' + \
                                               str(int(soup.find('span', 'main_date grey').find_all('td')[1].find(
                                                   'font').text) - 1)
                                except:
                                    try:
                                        data_end = soup.find_all('span', 'month fleft')[1].text + '-' + months[
                                            soup.find_all('span', 'month fleft')[0].text] + '-' + data.split(' - ')[
                                                       1]
                                    except:
                                        try:
                                            data_end = soup.find_all('span', 'month')[2].text + '-' + months[
                                                soup.find_all('span', 'month fright')[0].text] + '-' + \
                                                       data.split(' - ')[1]
                                        except:
                                            data_end = ''

                        information_about_olimpiad = (f"{hunderline(title)}.  \n"
                                                      f"Этап олимпиады - {hbold(step)} \n"
                                                      f"{data_start.split(' - ')[0]} "
                                                      f"{'--' * (len(data_end.split(' - ')[0]) != 0)} "
                                                      f"{data_end.split(' - ')[0]}  \n"
                                                      f"Расписание можете посмотреть {hlink(title='ТУТ!', url=fg)}\n"
                                                      f"Сайт этой олимпиады Вы можете посмотреть"
                                                      f"{hlink(title='ТУТ!', url=href_olimp)}  \n")

                        await add_subject(subject=subjects[i], title=title, information=information_about_olimpiad,
                                          start=data_start.strip().split(' - ')[0].replace('-До', ''))
                except:
                    pass
        except Exception as ex:
            pass


async def main():
    while True:
        await subject_to_bd()
        await asyncio.sleep(432000)


if __name__ == '__main__':
    asyncio.run(main())
