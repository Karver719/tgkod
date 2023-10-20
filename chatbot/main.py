import telegram
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, ConversationHandler
import speech_recognition as sr

# Замените 'YOUR_BOT_TOKEN' на токен вашего бота
bot_token = '6716422782:AAE_JplrDrq-K8i8kDhX2btrzL9zzYfY0Yw'


# Создаем объект бота с использованием токена
bot = telegram.Bot(token=bot_token)
updater = Updater(bot=bot, use_context=True, request_kwargs={"read_latency": 1.0})
dispatcher = updater.dispatcher





# Создаем константы для состояний беседы
MODE, QUANTITY, DESCRIPTION, DIMENSIONS, WEIGHT, COST, ADDRESS, PAYMENT = range(8)

# Словарь для хранения данных накладной
invoice_data = {}

def start(update, context):
    update.message.reply_text("Привет! Отправьте голосовое сообщение для создания накладной.")
    return MODE

def process_mode(update, context):
    text = update.message.text
    invoice_data['mode'] = text
    update.message.reply_text("Введите количество мест:")
    return QUANTITY

def process_quantity(update, context):
    text = update.message.text
    invoice_data['quantity'] = text
    update.message.reply_text("Введите описание вложений:")
    return DESCRIPTION

def process_description(update, context):
    text = update.message.text
    invoice_data['description'] = text
    update.message.reply_text("Введите габариты вложений (длина - ширина - высота):")
    return DIMENSIONS

def process_dimensions(update, context):
    text = update.message.text
    invoice_data['dimensions'] = text
    update.message.reply_text("Введите вес каждого места в кг:")
    return WEIGHT

def process_weight(update, context):
    text = update.message.text
    invoice_data['weight'] = text
    update.message.reply_text("Введите стоимость вложения (общая / по местам):")
    return COST

def process_cost(update, context):
    text = update.message.text
    invoice_data['cost'] = text
    update.message.reply_text("Введите точный адрес отправки (город, улица, дом):")
    return ADDRESS

def process_address(update, context):
    text = update.message.text
    invoice_data['address'] = text
    update.message.reply_text("Введите способ оплаты (Оплата получателем / Отправителем по договору):")
    return PAYMENT

def process_payment(update, context):
    text = update.message.text
    invoice_data['payment'] = text

    # Создаем текст накладной
    invoice_text = f"Накладная:\nРежим отправки: {invoice_data['mode']}\nКоличество мест: {invoice_data['quantity']}\nОписание: {invoice_data['description']}\nГабариты: {invoice_data['dimensions']}\nВес: {invoice_data['weight']}\nСтоимость: {invoice_data['cost']}\nАдрес отправки: {invoice_data['address']}\nСпособ оплаты: {invoice_data['payment']}"

    # Отправляем накладную пользователю
    update.message.reply_text(invoice_text)

    return ConversationHandler.END

def process_voice(update, context):
    r = sr.Recognizer()
    voice = update.message.voice
    if voice:
        file_id = voice.file_id
        file = context.bot.get_file(file_id)
        file.download("voice.ogg")

        with sr.AudioFile("voice.ogg") as source:
            audio = r.record(source)

        text = r.recognize_google(audio, language="ru-RU")
        update.message.text = text
        return process_mode(update, context)
    else:
        update.message.reply_text("Пожалуйста, отправьте голосовое сообщение.")
        return ConversationHandler.END

def cancel(update, context):
    update.message.reply_text("Отправка голосовых сообщений отменена.")
    return ConversationHandler.END

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        MODE: [MessageHandler(Filters.text, process_mode)],
        QUANTITY: [MessageHandler(Filters.text, process_quantity)],
        DESCRIPTION: [MessageHandler(Filters.text, process_description)],
        DIMENSIONS: [MessageHandler(Filters.text, process_dimensions)],
        WEIGHT: [MessageHandler(Filters.text, process_weight)],
        COST: [MessageHandler(Filters.text, process_cost)],
        ADDRESS: [MessageHandler(Filters.text, process_address)],
        PAYMENT: [MessageHandler(Filters.text, process_payment)],
        ConversationHandler.END: [MessageHandler(Filters.text, cancel)]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)

dispatcher.add_handler(conv_handler)

updater.start_polling()
updater.idle()
