import telebot
import Sender_message_telegram
import tele_keyboards
import message_worker
import os

#token="1233173072:AAHvqvXYxLK6fuZquGlkn3iw1XEXtBQfKf0"
token=os.environ.get('data_token', None)
bot = telebot.TeleBot(token)
print("BOT RUN")


@bot.message_handler(commands=['start'])
def start_message(message):
    hello=f"""Рады приветствовать тебя {message.chat.username} в нашей онлайн табачке Дымовой 🚬
    
У нас ты найдёшь:
• Только ОРИГИНАЛЬНАЯ продукция ✅
• Быстрая и бесплатная доставка по г. Обнинску и окраинам
• Разнообразность и эксклюзивность продукции
• Работаем 24/7 ⌚️
• Всегда слушаем вашу обратную связь и подстраиваемся под ваши интересы 🥰

Здесь ты можешь заказать самый разнообразный, а главное толко оригинальный товар буквально в несколько кликов и в ближайшее время тебе привезут его прямо домой!🤯"""

    ng="""Отличная новость!🔥 Наш магазин работает в Новогодние праздники 🎉 

Мы готовы принимать ваши заказы даже в новогоднюю ночь и с радостью привезём вам подарок под ёлочку)😉"""

    keyboard=tele_keyboards.Keyboard_Generator(["Эллектронки", "Испарители", "Жижи", "/Поделиться", "/Корзина"],X=[1,2,2])
    chat_id=message.chat.id
    name = message.chat.username
    print("Hello",chat_id)
    if name==None or name=="None":
        keyboard=tele_keyboards.Keyboard_Generator(["/start"])
        err="""К сожалению, чтобы пользоваться ботом, вам необходимо создать имя пользователя, иначе мы не сможем связаться с вами. 😢
Создайте имя пользователя и нажмите кнопку ниже, мы ждём твоего заказа! 👇"""
        Sender_message_telegram.send_message(bot, message, err, keyboard=keyboard)
    else:
        message_worker.add_in_Users_Base(chat_id, name)
        Sender_message_telegram.send_message(bot,message,hello,keyboard=keyboard)
        Sender_message_telegram.send_message(bot, message, ng)

@bot.message_handler(commands=['Корзина'])
def basket(message):
    message_worker.basket(bot,message)

@bot.message_handler(commands=['Поделиться'])
def share(message):
    text="Telegram: https://t.me/dymovoy_bot \nInstagram: https://instagram.com/dymovoy.dv?utm_medium=copy_link"
    pathQR="QR.jpg"

    keyboard = tele_keyboards.Keyboard_Generator(["Эллектронки", "Испарители", "Жижи", "/Поделиться", "/Корзина"],
                                                 X=[1, 2, 2])
    Sender_message_telegram.send_photo_video_message(bot,message,text,pathQR,keyboard=keyboard)

@bot.message_handler(commands=['Купить'])
def buy(message):
    message_worker.buy(bot,message)

@bot.message_handler(content_types=['text'])
def get_message(message):
    text = message.text
    chat_id=message.chat.id
    print(text,chat_id)
    message_worker.main_command_worker(bot, message, text)



@bot.callback_query_handler(func=lambda call: True)
def Callback_inline(call):
    if call.message:
        text = str(call.data)
        chat_id = call.message.chat.id
        name = call.message.chat.username
        print("button_inline",text,chat_id)
        message_worker.add_in_Users_Base(chat_id, name)
        message_worker.inline_buttons_worker(bot,call,text)

bot.infinity_polling()