#! /usr/bin/env python
# -*- coding: utf-8 -*-


import telebot
import config
import random
import geocoder

from telebot import types


bot = telebot.TeleBot(config.TOKEN)

#import feedback

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


@bot.message_handler(commands=['send'])
def process_start(message):
    if int(message.chat.id) == config.owner:
        bot.send_message(message.chat.id, 'Для отправки сообщения сделай реплей')
        bot.forward_message(config.owner, message.chat.id, message.message_id)
        bot.register_next_step_handler(message, process_mind)
    else:
        bot.send_message(message.chat.id, 'Вы не являетесь администратором для выполнения этой команды!')


def process_mind(message):
    if int(message.chat.id) == config.owner:
        text = 'Сообщение было отправлено пользователю ' + str(message.reply_to_message.forward_from.first_name)
        bot.forward_message(message.reply_to_message.forward_from.id, config.owner, message.message_id)
        bot.send_message(config.owner, text)
    else:
        bot.send_message(message.chat.id, 'Вы не являетесь администратором для выполнения этой команды!')


@bot.message_handler(commands=['id'])
def process_start(message):
    bot.send_message(message.chat.id, "Твой ID: " + str(message.from_user.id), parse_mode='HTML')
    bot.forward_message(config.owner, message.chat.id, message.message_id)


@bot.message_handler(commands=["help"])
def start(message):
    bot.send_message(message.chat.id,
                     'Этот бот создан для обратной связи с Abitu Для этого просто напишите сообщение, я его получу и отвечу. Дополнительные команды:\n\n/ping — проверяет работоспособность бота\n/id — показывает твой ID')
    bot.send_message(config.owner,
                     'Привет, хозяин! ' + str(message.from_user.first_name) + ' использовал команду /help')
    bot.forward_message(config.owner, message.chat.id, message.message_id)


@bot.message_handler(content_types=["text"])
def messages(message):
    if int(message.chat.id) == config.owner:
        try:
            bot.send_message(message.chat.id, 'Сообщение от администратора было получено')
        except:
            bot.send_message(config.owner,
                             'Что-то пошло не так! Бот продолжил свою работу.' + ' Ошибка произошла в блоке кода:\n\n <code>@bot.message_handler(content_types=["text"])</code>',
                             parse_mode='HTML')
    else:
        pass
        try:
            bot.forward_message(config.owner, message.chat.id, message.message_id)
            bot.send_message(message.chat.id, str(
                message.from_user.first_name) + ',' + ' я получил сообщение и очень скоро на него отвечу :)')
        except:
            bot.send_message(config.owner, 'Что-то пошло не так! Бот продолжил свою работу.')


bot.send_message(config.owner, 'Скрипт полностью запущен, бот функционирует! Используй /send для отправки сообщения :)')



bot.polling(none_stop=True)

