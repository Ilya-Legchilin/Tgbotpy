
import telebot
from time import sleep
import config
import logging
import datetime

#logger = telebot.logger
#telebot.logger.setLevel(logging.DEBUG)
#bot = telebot.AsyncTeleBot(token=config.token, threaded=False, skip_pending=False)


@bot.message_handler(commands=["ping"])
def start(message):
    try:
        bot.send_message(message.chat.id, "<b>PONG!</b>", parse_mode="HTML")
        bot.forward_message(config.owner, message.chat.id, message.message_id)
    except:
        bot.send_message(config.owner,
                         'Что-то пошло не так!')


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, 'Привет, ' + str(
        message.from_user.first_name) + '!\n' 'Напиши /help для просмотра возможностей бота.')
    bot.forward_message(config.owner, message.chat.id, message.message_id)
    if int(message.chat.id) == int(config.blacklist):
        pass


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

# bot.send_message(config.owner, 'Найдено администраторов бота: <b>2</b>', parse_mode='html')
# bot.send_message(config.owner, 'Администратор №1 - @amir_foreverornever', parse_mode='html')
# bot.send_message(config.owner, 'Worker <b>#1</b> был запущен!', parse_mode='html')
# bot.send_message(config.owner, 'Worker <b>#2</b> был запущен!', parse_mode='html')
# bot.send_message(config.owner, 'Worker <b>#3</b> был запущен!', parse_mode='html')
# bot.send_message(config.owner, 'Worker <b>#4</b> был запущен!', parse_mode='html')
# bot.send_message(config.owner, 'Worker <b>#5</b> был запущен!', parse_mode='html')
# bot.send_message(config.owner, 'Есть сообщения в очереди!', parse_mode='html')
# bot.send_message(config.owner, 'Сообщений в очереди:', parse_mode='html')
# bot.send_message(config.owner, random.randint(1,200))
# bot.send_message(config.owner, 'Вся служебная информация была доставлена администратору @amir_foreverornever!', parse_mode='html')


@bot.message_handler(content_types=['new_chat_member'])
def bot_users_new(msg):
	try:
		bot.send_message(468437664, 'test')
		bot.send_message(message.from_user.chat.id, 'ttttt')
		bot.leave_chat(c.message.chat.id)
	except:
		bot.send_message(468437664, 'Что-то пошло не так! Ошибка в:\n\n' + "<code>@bot.message_handler(content_types=['new_chat'])\ndef bot_users_new(msg):</code>")


