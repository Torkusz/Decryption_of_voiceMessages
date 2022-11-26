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
from config import *

#Database
conn = sqlite3.connect('db.db', check_same_thread=False)
cursor = conn.cursor()

def db(user_id: int, requests: int, data: str, admin: bool):
	cursor.execute('INSERT INTO main (user_id, requests, data, admin) VALUES (?, ?, ?, ?)', (user_id, requests, data, admin))
	conn.commit()

def get_data():
	now = datetime.datetime.now()
	data = str(now.year) + "-" + str(now.month) + "-" + str(now.day) + " " + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second)
	return data

#инициализируем бота
bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# logg
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

	await message.answer(f"{us_name}, привет!\n")

@dp.message_handler(commands = ["verif"])
async def ver(message: types.Message):
	await asyncio.sleep(1)
	await bot.delete_message(message.chat.id, message.message_id)

	keyboard = types.InlineKeyboardMarkup()
	bt_1 = InlineKeyboardButton(text="🍏", callback_data="apple_green")
	bt_2 = InlineKeyboardButton(text="🍎", callback_data="apple_red")
	bt_3 = InlineKeyboardButton(text="🫐", callback_data="blueberries")
	keyboard.add(bt_1, bt_2, bt_3)

	first_name = message.from_user.first_name
	id = message.from_user.id
	text2 = f"[{first_name}](tg://user?id={id}) \nНажми 🫐"
	await message.answer(text2, disable_web_page_preview=True, parse_mode="MarkdownV2", reply_markup=keyboard)

@dp.message_handler(commands =("help", "помощь"))
async def help(message: types.Message):
	buttons = [
		types.InlineKeyboardButton(text="Dark TON Chat 💭💎💯", url="https://t.me/nft_ton_community_chat"),
		types.InlineKeyboardButton(text="Dark NFT TON TRADE", url="https://t.me/tontrandenft"),
		types.InlineKeyboardButton(text="Dark Club Game Ton", url="https://t.me/+duKh95q9oAo4MzFk"),
		types.InlineKeyboardButton(text="Dark Ton флудилка 🫰", url="https://t.me/floodick")
	]
	keyboard = types.InlineKeyboardMarkup(row_width=1)
	keyboard.add(*buttons)
	await message.answer("""Правила группы: 

💭Правила чата:
• Не злоупотрелять матом
• Не оскорблять участников чата
• Не провоцировать агрессию в чате
• Не спамить
• Ссылки на сторонние проекты только после одобрения администрации чата.
• Минимальная отправка чека(+send тоже считается туда) 0.05 $TON или 10 $BOLT 
• Здесь не продаём, все продажи в отдельном чате (@tontrandenft) 💎
• Использование твинков запрещено 🚫 
• Попрошайничать что либо категорически запрещено 😡
• ОБСУЖДЕНИЕ ПОЛИТИКИ СТРОГО ЗАПРЕЩЕНО

За нарушения правил нарушители будут наказаны👮‍♂

Давайте уважать себя и окружающих♥️☺️

⭐️Канал: @nft_ton_community
🌟Владелец: @janekurjudope - вопросы по сотрудничеству""", reply_markup=keyboard)


@dp.message_handler(content_types=ContentType.TEXT)
async def check(message: types.Message):
	cursor.execute(f"SELECT user_id FROM main WHERE user_id = '{message.from_user.id}'")
	if cursor.fetchone() is None:
		us_id = message.from_user.id
		us_name = message.from_user.first_name
		us_sname = message.from_user.last_name
		username = message.from_user.username
		db_table_val(user_id=us_id, message=0, admin=False, mute=0, message_trand=0, message_flood=0, message_game=0, username='{username}', lastmessage=get_data(), mess=0)

@dp.message_handler(content_types=ContentType.VOICE)
async def check(message: types.Message):
	cursor.execute(f"SELECT user_id FROM main WHERE user_id = '{message.from_user.id}'")
	if cursor.fetchone() is None:
		us_id = message.from_user.id
		us_name = message.from_user.first_name
		us_sname = message.from_user.last_name
		username = message.from_user.username
		db_table_val(user_id=us_id, message=0, admin=False, mute=0, message_trand=0, message_flood=0, message_game=0, username='{username}', lastmessage=get_data(), mess=0)



if __name__ == "__main__":
	loop = asyncio.get_event_loop()
	loop.create_task(scheduled(15))
	executor.start_polling(dp, skip_updates=False)