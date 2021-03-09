import telebot
import os
import psutil
import subprocess
bot = telebot.AsyncTeleBot('1625952028:AAGHJaISo5qq3oOEyR3NXOz3XZt5yakIuDE')
status = "Покой"
ffs = []

class Program():
    def __init__(self, file, call):
        try:
            self.ff = subprocess.Popen(['python', file])
        except Exception as e:
            bot.send_message(call.message.chat.id, "Ошибка: \n" + e)
    def close(self):
        global status
        status = 'Покой'
        self.ff.kill()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('Список файлов', 'Статус', 'Остановить процесс')
    bot.send_message(message.chat.id, "Запущен", reply_markup=keyboard)

@bot.message_handler(commands=['status'])
def send_status(message):
    bot.reply_to(message, status)

@bot.message_handler(commands=['list'])
def send_list(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='Удаление файлов', callback_data="n1"))
    markup.add(telebot.types.InlineKeyboardButton(text='Запуск файлов', callback_data="n2"))
    markup.add(telebot.types.InlineKeyboardButton(text='Изменение параметров', callback_data="n3"))
    markup.add(telebot.types.InlineKeyboardButton(text='Получить файл', callback_data="n4"))
    st = ""
    for root, dirs, files in os.walk('C:/Users/turki/Desktop/ROBOCUP/PYTHON/files/'):  
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
        src = 'C:/Users/turki/Desktop/ROBOCUP/PYTHON/files/' + message.document.file_name
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.reply_to(message, "Сохранено")
        status = "Покой"
    except Exception as e:
        bot.reply_to(message, e)

@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text == 'Статус':
        send_status(message)
    elif message.text == 'Список файлов':
        send_list(message)
    elif message.text == 'Остановить процесс':
        for ff in ffs:
            ff.close()
        bot.send_message(message.chat.id, 'Все процессы остановлены')

@bot.message_handler(commands=['delete'])
def send_delete(call):
    markup = telebot.types.InlineKeyboardMarkup()
    for root, dirs, files in os.walk('C:/Users/turki/Desktop/ROBOCUP/PYTHON/files/'):  
        for filename in files:
            markup.add(telebot.types.InlineKeyboardButton(text=filename, callback_data="d"+filename))
    bot.send_message(call.message.chat.id, "Выберите файл: ", reply_markup=markup)

def send_file(call):
    markup = telebot.types.InlineKeyboardMarkup()
    for root, dirs, files in os.walk('C:/Users/turki/Desktop/ROBOCUP/PYTHON/files/'):  
        for filename in files:
            markup.add(telebot.types.InlineKeyboardButton(text=filename, callback_data="w"+filename))
    bot.send_message(call.message.chat.id, "Выберите файл: ", reply_markup=markup)

@bot.message_handler(commands=['up'])
def send_up(call):
    markup = telebot.types.InlineKeyboardMarkup()
    for root, dirs, files in os.walk('C:/Users/turki/Desktop/ROBOCUP/PYTHON/files/'):  
        for filename in files:
            markup.add(telebot.types.InlineKeyboardButton(text=filename, callback_data="s"+filename))
    bot.send_message(call.message.chat.id, "Выберите файл: ", reply_markup=markup)
    

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    global status
    if call.data == 'n1':
        send_delete(call)
    if call.data == 'n2':
        send_up(call)
    if call.data == 'n3':
        pass
    if call.data == 'n4':
        send_file(call)
    else:
        if call.data[0] == 'd':
            try:
                os.remove('C:/Users/turki/Desktop/ROBOCUP/PYTHON/files/' + call.data[1:])
                bot.send_message(call.message.chat.id, "Удален файл: " + call.data[1:])
            except:
                bot.send_message(call.message.chat.id, "Ошибка")
        if call.data[0] == 's':
            status = "Запущен файл: " + call.data[1:]
            bot.send_message(call.message.chat.id, "Запущен файл: " + call.data[1:])
            ffs.append(Program(call.data[1:], call))
        if call.data[0] == 'w':
            status = "Отправка файла: " + call.data[1:]
            bot.send_document(call.message.chat.id, open('C:/Users/turki/Desktop/ROBOCUP/PYTHON/files/' + call.data[1:], 'rb'))
            status = "Покой"

bot.polling(none_stop=True)