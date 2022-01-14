from glob import glob
import telebot

# t.me/Mamotrahatel_bot
# token='5005617277:AAHp0drU9ArX2pvHOvWQvCkVmezqMvziIKM'
token = '5036488639:AAHV3ZdGoopXcsDLUU6jCPl5ecQvWcvUmQI'
bot = telebot.TeleBot(token)
f = open('baza.txt', 'r', encoding='utf-8').read().split('\n')
f = list(map(lambda x: x.split('###'), f))
users = {}
users_waiting_for_answer = {}
users_waiting_for_question = {}


def save(f):
    open('baza.txt', 'w', encoding='utf-8').write('\n'.join(list(map(lambda x: '###'.join(x), f))))
    print('saving')


def make_question(message):
    global users_waiting_for_answer
    global users_waiting_for_question
    bot.send_message(message.chat.id, 'Введи вопрос, который поможет отличить ' + message.text + ' от ' +
                     f[users_waiting_for_answer[message.chat.id]][0])
    users_waiting_for_question[message.chat.id] = [users_waiting_for_answer.pop(message.chat.id), message.text]


def make_question_real(message):
    global users_waiting_for_question
    global f
    question = users_waiting_for_question[message.chat.id][0]
    answer = users_waiting_for_question[message.chat.id][1]
    xyi = f[question]
    f[question] = [message.text.rstrip('?') + '?', str(len(f)), str(len(f) + 1)]
    f.append([answer])
    f.append(xyi)
    users_waiting_for_question.pop(message.chat.id)
    save(f)
    bot.send_message(message.chat.id, 'Мы учтём это в будущем!')


def akinator(chat_id, boolean=True):
    global users
    global f
    global users_waiting_for_answer
    last_question = f[users[chat_id]]
    if len(last_question) == 1:
        if boolean:
            bot.send_message(chat_id, 'Ебать я умный')
        else:
            bot.send_message(chat_id, 'Бля, я тупорылая свинья, пиздец нахуй сука блять! Введи то, что ты загадал')
            users_waiting_for_answer[chat_id] = users[chat_id]
        users.pop(chat_id)
        return
    number_of_question = int(last_question[(2, 1)[boolean]])
    question = f[number_of_question]
    users[chat_id] = number_of_question
    if len(question) == 1:
        bot.send_message(chat_id, 'Я знаю, это ' + question[0] + '!')
    else:
        bot.send_message(chat_id, question[0])


@bot.message_handler(commands=['start'])
def start_message(message):
    global users
    global users_waiting_for_question
    global users_waiting_for_answer
    if message.chat.id in users_waiting_for_answer:
        users_waiting_for_answer.pop(message.chat.id)
    if message.chat.id in users_waiting_for_question:
        users_waiting_for_question.pop(message.chat.id)
    users[message.chat.id] = 0
    akinator(message.chat.id)


@bot.message_handler(commands=['yes'])
def yes(message):
    global users
    if message.chat.id in users:
        akinator(message.chat.id, True)
    else:
        bot.send_message(message.chat.id, 'Напишите /start и начните игру!')


@bot.message_handler(commands=['no'])
def no(message):
    global users
    if message.chat.id in users:
        akinator(message.chat.id, False)
    else:
        bot.send_message(message.chat.id, 'Напишите /start и начните игру!')


@bot.message_handler(content_types='text')
def text(message):
    global users_waiting_for_answer
    if message.chat.id in users_waiting_for_answer:
        make_question(message)
        return
    global users_waiting_for_question
    if message.chat.id in users_waiting_for_question:
        make_question_real(message)
        return


bot.infinity_polling()