import telebot
import sqlite3

bot = telebot.TeleBot('5798218737:AAHHXEGUJVlHv2ad2CIctfilrdgjkcQqxFE')
name = None


@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('lumine.sql')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primarykey, name varchar(50), pass varchar(50))')
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, 'Привет, сейчас тебя зарегестрируем! Введи имя пользователя')
    bot.register_next_step_handler(message, user_name)

def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, 'Введите пароль')
    bot.register_next_step_handler(message, user_pass)

def user_pass(message):
    password = message.text.strip()

    conn = sqlite3.connect('lumine.sql')
    cur = conn.cursor()

    cur.execute("INSERT INTO users (name, pass) VALUES ('%s', '%s')" % (name, password))
    conn.commit()
    cur.close()
    conn.close()

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('Список пользоватеоей', callback_data='users'))
    bot.send_message(message.chat.id, 'Пользователь зарегестрирован', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    conn = sqlite3.connect('lumine.sql')
    cur = conn.cursor()

    cur.execute('SELECT * FROM users')
    users = cur.fetchall()

    info = ''
    for elem in users:
        info += f'Имя: {elem[1]},пароль: {elem[2]}\n'

    cur.close()
    conn.close()

    bot.send_message(call.message.chat.id, info)


bot.polling(none_stop=True)