from __future__ import print_function

from datetime import datetime
from pathlib import Path

import psycopg2
from apscheduler.schedulers.background import BlockingScheduler
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from services.database import DBHelper
from services.utils import get_usd_currency

db = DBHelper()
scheduler = BlockingScheduler()
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SAMPLE_SPREADSHEET_ID = '15IJJXbGQkiuDBwlg1cCJ8CVwI0kcX1gLAtziKFTcsb0'
SAMPLE_RANGE_NAME = 'Лист1!A2:D'

root = Path(__file__).absolute().parent


# Получение данных из Google таблицы
def get_values_from_google_sheet():
    creds = None
    if Path(root / 'token.json').exists():
        creds = Credentials.from_authorized_user_file(str(Path(root / 'token.json')), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                str(Path(root / 'login.json')), SCOPES)
            creds = flow.run_local_server(port=0)
        with open(Path(root / 'token.json'), 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result['values']
    if not values:
        return None
    else:
        return values


# Занесение данных из Google таблицы в БД
def add_sheet_values_to_db():
    usd = get_usd_currency()
    values = get_values_from_google_sheet()
    new_values = []
    for row in values:
        row.append(float(format(usd * float(row[2]), '.2f')))
        new_values.append(row)
    new_values = tuple([tuple(i) for i in new_values])
    try:
        db.__execute_batch__(
            'INSERT INTO orders (id, order_id, value_usd, delivery_date, value_rub) '
            "VALUES (%s, %s, %s, TO_DATE(%s,'DD.MM.YYYY'), %s) ON CONFLICT (id) DO "
            'UPDATE SET (order_id, value_usd, value_rub, delivery_date) = '
            '(EXCLUDED.order_id, EXCLUDED.value_usd, EXCLUDED.value_rub, EXCLUDED.delivery_date) ',
            (*[x for x in new_values],))
        db.__execute__(f'DELETE FROM orders WHERE order_id NOT IN {tuple([x[1] for x in new_values])}', '')
    except psycopg2.Error as e:
        print(e)
    finally:
        print(f'Done at: {datetime.now()}')


# Задача на постоянное выполнение скрипта с интервалов 2 секунды
scheduler.add_job(add_sheet_values_to_db, 'interval', seconds=2)

if __name__ == '__main__':
    scheduler.start()
