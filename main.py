import logging
import asyncio
import random
import os

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher 
from aiogram.utils import executor
from aiogram.utils.executor import start_webhook
from aiogram.types.message import ContentType
from aiogram.utils.markdown import text, bold, italic, code, pre
from aiogram.types import ParseMode, InputMediaPhoto, InputMediaVideo, ChatActions


logging.basicConfig(format=f'%(filename)s [ LINE:%(lineno)+3s ]#%(levelname)+8s [%(asctime)s] %(message)s', level=logging.INFO)


TOKEN = '5249944816:AAEGA7WFQeV6Eq6rR79fIv6FsxHgjIfKNwc'
bot = Bot(token=TOKEN) 
dp = Dispatcher(bot)

HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME') 
# webhook settings 
WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com' 
WEBHOOK_PATH = f'/webhook/{TOKEN}' 
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}' 
# webserver settings 
WEBAPP_HOST = '0.0.0.0' 
WEBAPP_PORT = os.getenv('PORT', default=8000) 

async def on_startup(dispatcher): 
	await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True) 
async def on_shutdown(dispatcher): 
	await bot.delete_webhook() 



@dp.message_handler(commands=['start']) 
async def Start_Command(message: types.Message): 
	await message.reply("Привет!\nЗа помощью /help")


@dp.message_handler(commands=['help'])
async def Help_Command(message: types.Message):
	msg = text(bold('Вот какие комманды у меня есть: '), '/start', '/help','/random 0 10', 'А еще я повторяю слова', sep='\n') 
	await message.reply(msg, parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(commands=['random'], content_types=ContentType.ANY)
async def Random_Command(message: types.Message):
	argument = message.get_args()
	args = argument.split(' ')
	if (len(args) > 0 and len(args) < 2):
		await message.reply('Недостаточно аргументов')
	if (len(args) > 2):
		await message.reply('Аргументов больше чем два')
	if (len(args) == 2):
		oneN = int(args[0])
		twoN = int(args[1])
		rdigit = int(random.randint(oneN, twoN))
		str(rdigit)
		msg = text('Вот твое число: ', rdigit)
		await message.reply(msg, parse_mode=ParseMode.MARKDOWN)



@dp.message_handler() 
async def main_message_send(msg: types.Message): 
	await bot.send_message(msg.from_user.id, msg.text)




@dp.message_handler(content_types=ContentType.ANY)
async def IDK_Message(message: types.Message):
	msg = text(code('Я не знаю что с этим делать.'))
	await message.reply(msg, parse_mode=ParseMode.MARKDOWN)



if __name__ == '__main__': 
	executor.start_polling(dp)