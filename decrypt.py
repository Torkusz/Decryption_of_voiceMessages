# -*- coding: utf-8 -*-

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.exceptions import Throttled
from aiogram.types.message import ContentType
import aiogram.utils.markdown as fmt
import asyncio

import logging
from time import time
from time import sleep
import datetime
import random
from random import randint
import re
import json
import sqlite3
import requests
import matplotlib.pyplot as plt
import numpy as np
import os
from conf import *

#Database
conn = sqlite3.connect('db.db', check_same_thread=False)
cursor = conn.cursor()

def db(user_id: int, requests: int, data: str, admin: bool):
	cursor.execute('INSERT INTO main (user_id, requests, data, admin) VALUES (?, ?, ?, ?)', (user_id, requests, data, admin))
	conn.commit()
	
def req(user_id: int, data: str, text: str):
	cursor.execute('INSERT INTO requests (user_id, data, text) VALUES (?, ?, ?)', (user_id, data, text))
	conn.commit()

def get_data(): #Getting the current date
	now = datetime.datetime.now()
	data = str(now.year) + "-" + str(now.month) + "-" + str(now.day) + " " + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second)
	return data

#initializing the bot
bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

#logg
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands = ["start"])
async def start(message: types.Message):
	cursor.execute(f"SELECT user_id FROM main WHERE user_id = '{message.from_user.id}'")
	if cursor.fetchone() is None:
		us_id = message.from_user.id
		us_name = message.from_user.first_name
		us_sname = message.from_user.last_name
		username = message.from_user.username
		db(user_id=us_id, requests=0, data=get_data(), admin=False)

	await message.answer(f"{message.from_user.first_name}, привет!\nЭтот бот умеет расшифровывать голосовые сообщения")

@dp.message_handler(commands =("help", "помощь"))
async def help(message: types.Message):
	buttons = [
		types.InlineKeyboardButton(text="Связь", url="https://t.me/Torkusz"),
		types.InlineKeyboardButton(text="Проект на GitHub", url="https://github.com/Torkusz/Decryption_of_voiceMessages")
	]
	keyboard = types.InlineKeyboardMarkup(row_width=1)
	keyboard.add(*buttons)
	await message.answer("Этот бот умеет расшифровывать голосовые сообщения\n\nДержи ссылку для обратной связи и на проект", reply_markup=keyboard)

@dp.message_handler(commands = ["get"])
async def start(message: types.Message):
	select_movies_query = "SELECT user_id, data, text FROM requests"
	cursor.execute(select_movies_query)
	result = cursor.fetchall()
	if result is None:
		await message.answer(f"{message.from_user.first_name}, кажется тебя нет в боте, нажми /start")
	else:
		await message.answer("📊Данные:{}".format("".join(["\n"+str(f"ID:%s  DATA:%s  TEXT:%s"%(row[0],row[1],row[2])) for row in result])))

@dp.message_handler(content_types=ContentType.VOICE)
async def check(message: types.Message):
	

if __name__ == "__main__":
	loop = asyncio.get_event_loop()
	executor.start_polling(dp, skip_updates=False)