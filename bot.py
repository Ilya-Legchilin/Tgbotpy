#!/usr/bin/env python
# -*- coding: utf-8 -*-
from time import sleep

import seaborn as sns
import numpy as np

def plot_hist(data):

    sns.set(color_codes=True)
    snsplot = sns.distplot(np.array(data), kde=False)
    fig = snsplot.get_figure()
    fig.savefig("output1.png")

    snsplot = sns.kdeplot(np.array(data), shade=True)
    fig = snsplot.get_figure()
    fig.savefig("output2.png")

TOKEN = "1026083345:AAGNy9fiaEQa2fD5Igb8UsdMKX11HGquN8w"


discriptions = ['определение подходящей ФТ-школы',
                'оставьте отзыв о ПК',
                'задать вопрос боту',
                'не баг, а feature',
                'задайте экспресс-вопрос админу',
                'распределение по баллам']

ask_dict = {"Выбери любимые предметы (m)": ['физика', 'математика', 'информатика', 'биология', 'химия'],
            "Знаешь что такое машина Тьюринга? (u)": ['Да', 'Нет'],
            "Любишь играть в футбол? (u)" : ['Да', 'Нет'],
            "Призер/победитель физтех-олимпиады(М/Ф)? (u) ": ['Да', 'Нет'],
            "Любимый цвет? (u)": ['Красный', 'Желтый', 'Синий', 'Зеленый', 'Белый'],
            "Знаешь когда родился Ландау? (u)": ['Да', 'Нет'],
            "Знаешь когда родился Капица? (u)": ['Да', 'Нет'],
            "Знаешь когда создали Физтех? (u)": ['Да', 'Нет'],
            "Пол (u)": ['М', 'Ж'],
            "Кто такой Овчинкин? (u)": ["Математик", 'Физик', 'Физрук', 'Не знаю'],
            "Какие разделы математики интересуют вас больше всего? (m)": ["геометрия", "алгебра", "теорвер, комбинаторика"],
            "Какие разделы физики в школе были интересны? (m)": ["Механика", "Электричество", "Оптика", "Термодинамика"],
            "Какие разделы программирования в школе были вам интересны? (m)": ["никакие", "олимпиадные алгоритмы",
            "проектное программирование", "программирование микроконтроллеров"]}

from telegram import ReplyKeyboardMarkup, Bot, KeyboardButton, Poll, PollOption, ReplyMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, PicklePersistence)

import logging
import classifier
import find_nearest_seq

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

connected_users = set()
sessions = {}
possible_answers = []
questions = []

class Session(object):
    def __init__(self):
        self.counter = 0
        self.answers = []
        self.handled_answers = []
        self.state = 'start'

class AdminSession(object):
    def __init__(self, id):
        self.id = id
        self.feedback_list = []
        self.message_list = []
        self.state = ''

admin = AdminSession(105660139)

for q in ask_dict:
    questions.append(q)
    possible_answers.append(ask_dict[q])

questions_value = len(questions)

def start(update, context):
    welcome_message = 'Привет, это бот приёмной комиссии Физтеха!\nКоманды:\n'
    id = update.effective_chat.id
    if id not in connected_users:
        connected_users.add(id)
        sessions.update({id : Session()})

    keyboard = []
    for command, dis in zip(commands, discriptions):
        welcome_message += ('/' + command + ' - ' + dis + '\n')
        keyboard.append(['/' + command])

    markup = ReplyKeyboardMarkup(keyboard=keyboard)
    context.bot.send_message(chat_id=id, text=welcome_message + '\n\n' + 'Ваш Telegram ID: '+ str(update.effective_chat.id), reply_markup=markup)

def poll_step(update, context):
    print("xxx\n\n")
    #global counter, answers, handled_answers, state
    global sessions
    id = update.effective_chat.id
    recieved_answer = update.message.text
    sessions[id].answers.append(recieved_answer)
    if (sessions[id].counter < questions_value - 1):
        sessions[id].counter += 1
        answers_string = ''
        i = 0
        for ans in possible_answers[sessions[id].counter]:
            i += 1
            answers_string += (str(i) + '. ' + ans + '\n')
        context.bot.send_message(chat_id=id, text=questions[sessions[id].counter] + '\n' + answers_string)
    else:
        for answer in sessions[id].answers:
            sessions[id].handled_answers.append(list(answer))
        context.bot.send_message(chat_id=id, text='Наиболее подходящая Физтех-Школа для вас:')
        res = classifier.classifier(sessions[id].handled_answers)
        context.bot.send_message(chat_id=id, text=res[0])
        sessions[id].counter = 0
        sessions[id].answers = []
        sessions[id].handled_answers = []
        sessions[id].state = 'start'
        start(update, context)


def answer(update, context):
    global sessions
    id = update.effective_chat.id
    question = update.message.text
    res = find_nearest_seq.find_nearest_seq(question)
    string = ''
    for q in res:
        string += 'Вопрос:\n' + q + '\n\nОтвет:\n' + res[q] + '\n\n'
    context.bot.send_message(chat_id=id, text=string)
    start(update, context)

def question(update, context):
    global sessions
    id = update.effective_chat.id
    sessions[id].state = 'question'
    print('1\n')
    context.bot.send_message(chat_id=id, text='Задайте вопрос боту')

def write_feedback(update, context):
    global sessions
    id = update.effective_chat.id
    feedback_message = update.message.text
    admin.feedback_list.append(feedback_message)
    context.bot.send_message(chat_id=update.effective_chat.id, text='Спасибо за ваш фидбэк!')
    start(update, context)

def send_question_to_admin(update, context):
    global sessions
    id = update.effective_chat.id
    message_to_send = update.message.text
    admin.message_list.append({'id' : id, 'mes' : message_to_send})
    context.bot.send_message(chat_id=update.effective_chat.id, text='Спасибо за ваш вопрос!')
    start(update, context)

def message(update, context):
    global sessions
    print(update.message.text + 'aaaaaaaa\n\n\n')
    id = update.effective_chat.id
    if sessions[id].state == 'poll':
        poll_step(update, context)
    if sessions[id].state == 'question':
        answer(update, context)
    if sessions[id].state == 'feedback':
        write_feedback(update, context)
    if sessions[id].state == 'send_qta':
        send_question_to_admin(update, context)
    if sessions[id].state == 'get_hist':
        print('asd\n\n')
        send_hist(update, context)

def send_hist(update, context):
    data = np.random.normal(loc=296, scale=5, size=150)
    plot_hist(data)
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('output1.png', 'rb'))
    context.bot.send_message(chat_id=update.effective_chat.id, text='Данная гистограмма показывает распределение абитуриентов по баллам в данной ФТ-школе')
    start(update, context)

def feedback(update, context):
    global sessions
    id = update.effective_chat.id
    sessions[id].state = 'feedback'
    context.bot.send_message(chat_id=update.effective_chat.id, text="Напишите фидбэк")

def admin_cmd(update, context):
    pass

def snd(update, context):
    print('OOO\n\n')
    if (update.effective_chat.id == admin.id):
        rcv_msg = update.message.text[update.message.text.find(' ') + 1:]
        mes = rcv_msg[rcv_msg.find(' ') + 1:]
        reciever_id = int(rcv_msg[:rcv_msg.find(' ')])
        print(mes + ' | ' + str(reciever_id))
        context.bot.send_message(chat_id=reciever_id, text=mes)
        context.bot.send_message(chat_id=admin.id, text='Сообщение успешно отправлено!')

def show_feedback(update, context):
    if (update.effective_chat.id == admin.id):
        context.bot.send_message(chat_id=admin.id, text='Анонимный фидбэк:')
        for mes in admin.feedback_list:
            context.bot.send_message(chat_id=admin.id, text=str(mes) + '\n\n\n')

def show_messages(update, context):
    print('x\n')
    if (update.effective_chat.id == admin.id):
        context.bot.send_message(chat_id=admin.id, text='Сообщения от абитуриентов:')
        for mes in admin.message_list:
            context.bot.send_message(chat_id=admin.id, text=str(mes['id']) + ':\n' + str(mes['mes']) + '\n\n\n')

def poll(update, context):
    global sessions
    id = update.effective_chat.id
    sessions[id].state = 'poll'

    answers_string = ''
    i = 0
    for ans in possible_answers[sessions[id].counter]:
        i += 1
        answers_string += (str(i) + '. ' + ans + '\n')
    context.bot.send_message(chat_id=update.effective_chat.id, text='Данный опрос поможет вам подобрать ФТ-школу! Флажок (m) разрешает выбирать несколько ответов, флажок (u) - только один. Ответ давать номерами без пробелов.')
    context.bot.send_message(chat_id=update.effective_chat.id, text=questions[sessions[id].counter] + '\n' + answers_string)

    #button1 = KeyboardButton(text='4', callback_data='0')
    #button2 = KeyboardButton(text='3', callback_data='1')
    #button3 = KeyboardButton(text='10 000', callback_data='2')

    #options = ['4', '3', '10 000']

    #keyboard = [[button1, button2], [button3]]
    #keyboard = [['4', '3'], ['10 000']]
    #markup = ReplyKeyboardMarkup(keyboard=keyboard)
    #context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
    #context.bot.send_poll(chat_id=update.effective_chat.id, question="2 + 2 = ?", options=options, reply_markup=markup)

def get_hist(update, context):
    global sessions
    id = update.effective_chat.id
    sessions[id].state = 'get_hist'
    keyboard = [['ФРКТ'], ['ФПМИ'], ['ЛФИ'], ['ФАКТ'], ['ИНБИКСТ'], ['ФЭФМ'], ['ФБМФ']]
    markup = ReplyKeyboardMarkup(keyboard=keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id, text="выбери школу", reply_markup=markup)

def question_to_admin(update, context):
    global sessions
    id = update.effective_chat.id
    sessions[id].state = 'send_qta'
    context.bot.send_message(chat_id=id, text='Напиши сообщение админу')

commands = {'poll' : poll, 'feedback' : feedback, 'question' : question, 'start' : start, 'question_to_admin' : question_to_admin, 'get_hist' : get_hist}
admin_commands = {'admin_cmd' : admin_cmd, 'show_feedback' : show_feedback, 'show_messages' : show_messages}
handlers = []
for command in commands:
    handlers.append(CommandHandler(command, commands[command]))
    dispatcher.add_handler(handlers[-1])

for command in admin_commands:
    handlers.append(CommandHandler(command, admin_commands[command]))
    dispatcher.add_handler(handlers[-1])

admin_send_message_handler = MessageHandler(Filters.regex('^send'), snd)
all_messages_handler = MessageHandler(Filters.regex('^(?!send)'), message)
dispatcher.add_handler(all_messages_handler)
dispatcher.add_handler(admin_send_message_handler)
updater.start_polling()
