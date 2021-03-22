import telebot
import os
import psutil
import subprocess
import sys
import time
from robot import Robot
from PIL import Image

bot = telebot.TeleBot('')
status = "Покой"
path = 'AR_BOT/files'
null_path = 'AR_BOT'
ffs = []
check = False
robot = Robot()


class Program():
    def __init__(self, file, call):
        self.ff = subprocess
        try:
            self.ff = subprocess.Popen(['python', path + '/'  + file])
        except subprocess.CalledProcessError as e:
            try:
                bot.send_message(call.message.chat.id, "Ошибка: \n" + str(e.output))
            except:
                pass
            
    def close(self):
        global status
        status = 'Покой'
        self.ff.kill()

with open(null_path + '/' + 'auto.txt', 'r') as f:
    global line
    line = f.readlines(1)
    print(line[0])
    if line[0] != "null":
        ffs.append(Program(line[0], False))

def send_photo(message):
    try:
        img = open(null_path + '/buffer/' + 'picture.jpg', 'rb')
        bot.send_chat_action(message.chat.id, 'upload_photo')
        bot.send_photo(message.chat.id, img)
        img.close()
    except:
        bot.send_message(message.chat.id, "Изображение отсутствует")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    global line
    #bot.send_chat_action(message.chat.id, 'typing')
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('Список файлов', 'Статус')
    keyboard.row('Получение вывода', 'Получение кадра')
    keyboard.row('Автозапуск', 'Остановить процесс')
    keyboard.row('Показания датчиков')
    bot.send_message(message.chat.id, "Запущен\n" + "Файл автозапуска: " + line[0], reply_markup=keyboard)
    #bot.send_chat_action(message.chat.id, 'typing')

@bot.message_handler(commands=['status'])
def send_status(message):
    bot.reply_to(message, status)

@bot.message_handler(commands=['list'])
def send_list(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='Удаление файлов', callback_data="n1"))
    markup.add(telebot.types.InlineKeyboardButton(text='Запуск файлов', callback_data="n2"))
    #markup.add(telebot.types.InlineKeyboardButton(text='Получение фото с камеры', callback_data="n3"))
    markup.add(telebot.types.InlineKeyboardButton(text='Получить файл', callback_data="n4"))
    st = ""
    for root, dirs, files in os.walk(path + '/'):  
        for filename in files:
            st += filename + '\n'
    try:
        bot.reply_to(message, st, reply_markup=markup)
    except:
        bot.reply_to(message, 'Пусто')

@bot.message_handler(content_types=['document'])
def handle_file(message):
    global status
    status = "Скачивание файла: " + message.document.file_name
    try: 
        chat_id = message.chat.id
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = path + '/'  + message.document.file_name
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.reply_to(message, "Сохранено")
        status = "Покой"
    except Exception as e:
        bot.reply_to(message, e)

@bot.message_handler(commands=['gyro'])
def send_gyro(message):
    bot.send_message(message.chat.id, str(robot.GetGyro()) + '\n' + str(robot.GetAccel()))

@bot.message_handler(content_types=['text'])
def send_text(message):
    global check
    if message.text == 'Статус':
        send_status(message)
    elif message.text == 'Список файлов':
        send_list(message)
    elif message.text == 'Получение кадра':
        send_photo(message)
    elif message.text == 'Автозапуск':
        send_auto(message)
    elif message.text == 'Получение вывода':
        check = True
        send_data(message)
    elif message.text == 'Показания датчиков':
        send_gyro(message)
    elif message.text == 'Остановить':
        check = False
        send_welcome(message)
    elif message.text == 'Остановить процесс':
        for ff in ffs:
            ff.close()
        bot.send_message(message.chat.id, 'Все процессы остановлены')

@bot.message_handler(commands=['delete'])
def send_delete(call):
    markup = telebot.types.InlineKeyboardMarkup()
    for root, dirs, files in os.walk(path):  
        for filename in files:
            markup.add(telebot.types.InlineKeyboardButton(text=filename, callback_data="d"+filename))
    bot.send_message(call.message.chat.id, "Выберите файл: ", reply_markup=markup)

def send_data(message):
    global check
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('Остановить')
    while check:
        with open(null_path + '/buffer/' + 'data.txt', 'r') as f:
            try:
                data = f.readlines()[0]
            except:
                pass
        bot.send_message(message.chat.id, data, reply_markup=keyboard)
        time.sleep(0.300)

def send_chose(call):
    markup = telebot.types.InlineKeyboardMarkup()
    for root, dirs, files in os.walk(path):  
        for filename in files:
            markup.add(telebot.types.InlineKeyboardButton(text=filename, callback_data="a"+filename))
    bot.send_message(call.message.chat.id, "Выберите файл: ", reply_markup=markup)

def send_auto(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='Убрать автозапуск', callback_data="g1"))
    markup.add(telebot.types.InlineKeyboardButton(text='Выбрать файл', callback_data="g2"))
    markup.add(telebot.types.InlineKeyboardButton(text='Узнать текущий', callback_data="g3"))
    bot.send_message(message.chat.id, "Выберите действие: ", reply_markup=markup)

def send_file(call):
    markup = telebot.types.InlineKeyboardMarkup()
    for root, dirs, files in os.walk(path):  
        for filename in files:
            markup.add(telebot.types.InlineKeyboardButton(text=filename, callback_data="w"+filename))
    bot.send_message(call.message.chat.id, "Выберите файл: ", reply_markup=markup)

@bot.message_handler(commands=['up'])
def send_up(call):
    markup = telebot.types.InlineKeyboardMarkup()
    for root, dirs, files in os.walk(path):  
        for filename in files:
            markup.add(telebot.types.InlineKeyboardButton(text=filename, callback_data="s"+filename))
    bot.send_message(call.message.chat.id, "Выберите файл: ", reply_markup=markup)
    

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    global status
    global ffs
    if call.data == 'n1':
        send_delete(call)
    if call.data == 'n2':
        send_up(call)
    if call.data == 'n3':
        send_photo(call)
    if call.data == 'n4':
        send_file(call)
    if call.data == 'g1':
        with open(null_path + '/' + 'auto.txt', 'w') as f:
            f.write('null')
        bot.send_message(call.message.chat.id, "Автозапуск очищен")
    if call.data == 'g2':
        send_chose(call)
    if call.data == 'g3':
        with open(null_path + '/' + 'auto.txt', 'r') as f:
            global line
            line = f.readlines(1)
        bot.send_message(call.message.chat.id, "Файл автозапуска: " + line[0])
    else:
        if call.data[0] == 'd':
            try:
                os.remove(path + '/' + call.data[1:])
                bot.send_message(call.message.chat.id, "Удален файл: " + call.data[1:])
            except:
                bot.send_message(call.message.chat.id, "Ошибка")
        if call.data[0] == 's':
            status = "Запущен файл: " + call.data[1:]
            if call.data[len(call.data) - 1 ] == "y":
            	bot.send_message(call.message.chat.id, "Запущен файл: " + call.data[1:])
            	ffs.append(Program(call.data[1:], call))
            else:
            	bot.send_message(call.message.chat.id, "Файл должен иметь расширение .py")
        if call.data[0] == 'w':
            status = "Отправка файла: " + call.data[1:]
            bot.send_chat_action(call.message.chat.id, 'upload_document')
            bot.send_document(call.message.chat.id, open(path + '/'  + call.data[1:], 'rb'))
            status = "Покой"
        if call.data[0] == 'a':
            with open(null_path + '/' + 'auto.txt', 'w') as f:
                f.write(call.data[1:])
            bot.send_message(call.message.chat.id, "Выбран файл: " + call.data[1:])

bot.polling(none_stop=True)
