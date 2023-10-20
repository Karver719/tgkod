<<<<<<< HEAD
import telebot
import sous

token = "6363377954:AAGTtkjp4ov05F5hBG01HGk82LQZW739unw"

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def answer_to_start(message):
    bot.send_message(message.chat.id, sous.startmess)

@bot.message_handler(content_types=["text"])
def answer_to_text(message):
    global gorod_set
    word = 'минск'
    if word in message.text.lower():
        bot.send_message(message.chat.id, 'Укажите ваш пол (мужской/женский)')
        gorod_set = 1
    elif message.text.lower() == 'мужской' and gorod_set == 1:
        bot.send_message(message.chat.id, 'Йоу, у тебя получилось!')
        # Если нужно изменить город и начать по новой добавьте 'gorod_set = 0'
    elif message.text.lower() == 'женский' and gorod_set == 1:
        bot.send_message(message.chat.id, 'Тоже нормально!')
        # Здесь так же 'gorod_set = 0'
    else:
        bot.send_message(message.chat.id, "Извините, у вас другой город!")

=======
import telebot
import sous

token = "6363377954:AAGTtkjp4ov05F5hBG01HGk82LQZW739unw"

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def answer_to_start(message):
    bot.send_message(message.chat.id, sous.startmess)

@bot.message_handler(content_types=["text"])
def answer_to_text(message):
    global gorod_set
    word = 'минск'
    if word in message.text.lower():
        bot.send_message(message.chat.id, 'Укажите ваш пол (мужской/женский)')
        gorod_set = 1
    elif message.text.lower() == 'мужской' and gorod_set == 1:
        bot.send_message(message.chat.id, 'Йоу, у тебя получилось!')
        # Если нужно изменить город и начать по новой добавьте 'gorod_set = 0'
    elif message.text.lower() == 'женский' and gorod_set == 1:
        bot.send_message(message.chat.id, 'Тоже нормально!')
        # Здесь так же 'gorod_set = 0'
    else:
        bot.send_message(message.chat.id, "Извините, у вас другой город!")

>>>>>>> 0ee55233b1fc00a761cf9eb267658161a72363ae
bot.polling(none_stop=True)