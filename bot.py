#! /usr/bin/env python
# -*- coding: utf-8 -*-


import telebot
import config
import random
import geocoder

from telebot import types


bot = telebot.TeleBot(config.TOKEN)

import feedback

@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('static/welcome.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)

    #keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton(")) Рандомное число")
    item2 = types.KeyboardButton(")) Как дела?")
    item3 = types.KeyboardButton(")) Where am I?")

    markup.add(item1, item2, item3)

    
    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\n Я - <b>{1.first_name}</b>бот.".format(message.from_user, bot.get_me()),
        parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def lalala(message):
    if message.chat.type == 'private':
        if message.text == ')) Рандомное число':
            bot.send_message(message.chat.id, str(random.randint(0,100)))
        elif message.text == ')) Как дела?':
            bot.send_message(message.chat.id, 'Отлично, сам как?')

        elif message.text == ')) Where am I?':
            g = geocoder.ip('me')
            bot.send_location(message.chat.id, g.latlng[0], g.latlng[1])

        else:
            bot.send_message(message.chat.id, 'Я не знаю что ответить :(')

bot.polling(none_stop=True)

