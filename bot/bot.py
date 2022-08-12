import logging

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from services.database import DBHelper
from services.utils import add_user_to_db, get_outdated_orders, get_bot_users, note_sent_notification

token = '5584380727:AAE-DeZM2at1ndRPpdDMnpEyc66XbsL0EA4'

db = DBHelper()

# Инициализация бота и задачника
logging.basicConfig(level=logging.INFO)
bot = Bot(token=token)
dp = Dispatcher(bot)
scheduler = AsyncIOScheduler()


# Приветствие пользователя и занесение его в базу данных
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    add_user_to_db(message.chat.id)
    await message.reply(f"Hi {message.chat.full_name}!\nI'm Notification Bot!")


# Отправка сообщений о просроченных сроках пользователям из БД
async def send_notification():
    dates = get_outdated_orders()
    users = get_bot_users()
    try:
        for date in dates:
            note_sent_notification(date[0])
            for user in users:
                await bot.send_message(user[0], f"Outdated order: {date[0]}\nDate: {date[4]}")
    except Exception as e:
        for user in users:
            await bot.send_message(user[0], f"Something went wrong...\nCause: {e}")

# Задача на отправку сообщений каждую ночь в 00:05
scheduler.add_job(send_notification, 'cron', hour=0, minute=5)

if __name__ == '__main__':
    scheduler.start()
    executor.start_polling(dp, skip_updates=True)
