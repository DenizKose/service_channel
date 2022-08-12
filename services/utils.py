import xml.etree.ElementTree as ET

import psycopg2
import requests

from services.database import DBHelper

db = DBHelper()


# Получение текущего курса доллара
def get_usd_currency():
    url = 'https://www.cbr.ru/scripts/XML_daily.asp'
    data = requests.get(url).text
    root = ET.fromstring(data)
    for valute in root.findall('Valute'):
        if valute.attrib['ID'] == 'R01235':
            for usd_currency in valute.findall('Value'):
                return float(usd_currency.text.replace(',', '.'))


# Получение всех заказов
def get_orders():
    return db.__fetch_all__('SELECT * FROM orders ORDER BY id', '')


# Получение просроченных заказов
def get_outdated_orders():
    outdated_orders = tuple(db.__fetch_all__('SET datestyle = DMY; '
                                             'SELECT * FROM orders WHERE delivery_date<CURRENT_DATE AND '
                                             'notification_sent=FALSE;', ''))
    return outdated_orders


# Обновление статуса уведомлений
def note_sent_notification(order_id):
    try:
        db.__execute__('UPDATE orders SET notification_sent=TRUE WHERE id=(%s)', (order_id,))
    except Exception as e:
        print(e)


# Добавление пользователя бота в БД
def add_user_to_db(user_id):
    try:
        db.__execute__('INSERT INTO bot_users (user_id) '
                       'VALUES (%s) '
                       'ON CONFLICT (user_id) DO NOTHING ',
                       (user_id,))
    except (psycopg2.Warning or psycopg2.Error) as e:
        print(e)


# Получение пользователей бота
def get_bot_users():
    return db.__fetch_all__('SELECT user_id FROM bot_users', '')
