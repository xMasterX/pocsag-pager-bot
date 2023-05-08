import telebot
import os
import re
import time
from telebot import types

API_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN_HERE_From_BotFather"

bot = telebot.TeleBot(API_TOKEN)

user_dict = {
    111111111: {  # Your telegram ID
        "name": "U1:",
        "lastmessage": "",
        "lastnumber": "",
        "access": True,
        "limited_access": False,
    },
    222222222: {  # Other user telegram ID
        "name": "U2:",
        "lastmessage": "",
        "lastnumber": "",
        "access": True,
        "limited_access": True,
    },
}


# Handle '/start' and '/help'
@bot.message_handler(commands=["help", "start"])
def send_welcome(message):
    chat_id = message.chat.id
    if message.chat.type != "private":
        bot.reply_to(message, "Go away, this is a private property!")
        return
    # user = user_dict[chat_id]
    if chat_id in user_dict:
        if user_dict[chat_id]["access"]:
            print("User found and has access:", chat_id, message.chat.first_name)
        else:
            print("User found and has NO access:", chat_id, message.chat.first_name)
            bot.reply_to(message, "Go away, this is a private property!")
            return
    else:
        print("User NOT found and has NO access:", chat_id, message.chat.first_name)
        bot.reply_to(message, "Go away, this is a private property!")
        return

    msg = bot.send_message(
        message.chat.id,
        """\
-=-MMX Telecom Paging-=-
-=-MMX Телеком Пейджинг-=-

-----
Внимание! Для номера 1123A возможен только английский текст! 
Русский будет транслитерирован!
-----

Напишите и отправьте ваше сообщение - на русском языке,
английский тоже разрешен но будет переведен в русский транслит

Затем вам будет предложено выбрать номер абонента, 
нажмите на номер и сообщение будет отправлено

Внимание! 
Номер 3123 предназначен для рассылок и уведомления на нём отключены!
""",
    )
    bot.register_next_step_handler(msg, process_message_step)


def process_message_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        if (message.text == "/start") or (message.text == "/help"):
            bot.reply_to(message, "Ошибка! Бот уже был активирован")
            raise Exception("already activated")
        user["lastmessage"] = message.text
        if user["limited_access"]:
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add("122", "111", "3123", "1123A")
            msg = bot.reply_to(message, "Укажите номер абонента", reply_markup=markup)
            bot.register_next_step_handler(msg, process_send_step)
        else:
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add("110", "122", "121", "111", "3123", "1123A")
            msg = bot.reply_to(message, "Укажите номер абонента", reply_markup=markup)
            bot.register_next_step_handler(msg, process_send_step)
    except Exception as e:
        msg = bot.reply_to(message, "Ошибка!")
        send_welcome(msg)


# Most important things are below
def msg_regex_cut(text):
    res = re.sub(r"[^a-zA-ZА-Яа-я0-9 =#@\n$%&*()_+';./:>?,<!ёЁ-]+", "*", text)
    return res


def msg_transliterator(text):
    search = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ@"
    replace = "ABWGDEEVZIJKLMNOPRSTUFHC^[]XYX\@Qabwgdeevzijklmnoprstufhc~{}xyx|@qA"
    trans = str.maketrans(search, replace)
    return text.translate(trans)


def msg_transliterator_en_to_ru(text):
    replace = "абцдефгхийклмнопярстувщхызАБЦДЕФГХИЙКЛМНОПЯРСТУВЩХЫЗ"
    search = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    trans = str.maketrans(search, replace)
    return text.translate(trans)


def msg_transliterator_ru_to_en(text):
    search = "абцдеёфгхийклмнопярстувжщызъьэючшАБЦДЕЁФГХИЙКЛМНОПЯРСТУВЩЫЗЪЬЭЮЧШЖ"
    replace = "abcdeefghijklmnopqrstuvxwyz''eu4wABCDEEFGHIJKLMNOPQRSTUVWYZ''EU4WX"
    trans = str.maketrans(search, replace)
    return text.translate(trans)


def send_msg_to_pgr(capcode, freq, mesg):
    runcheck_command = 'pidof pocsag >/dev/null && echo "run" || echo "nf"'
    rstream = os.popen(runcheck_command)
    routput = rstream.read()
    print(routput)
    while routput == "run":
        print("pocsag is running - sleeping for 8 sec and retry")
        time.sleep(8)
        nrstream = os.popen(runcheck_command)
        nroutput = nrstream.read()
        if nroutput == "nf":
            break
        else:
            continue
    else:
        print("pocsag is not running - executing")

    command = (
        'echo $(echo "'
        + capcode
        + ":"
        + mesg
        + '") | sudo /home/pi/rpitx/pocsag -f "'
        + freq
        + '" -b 3 -r 1200'
    )  # -r 1200 === POCSAG 1200
    print(command)
    stream = os.popen(command)
    output = stream.read()
    dell = output


def process_send_step(message):
    try:
        chat_id = message.chat.id
        abonent = message.text
        user = user_dict[chat_id]
        if (
            (abonent == "110")
            or (abonent == "122")
            or (abonent == "121")
            or (abonent == "111")
            or (abonent == "3123")
            or (abonent == "1123A")
        ):
            user["lastnumber"] = abonent
            if (
                (abonent == "110")
                or (abonent == "122")
                or (abonent == "121")
                or (abonent == "3123")
            ) and (len(user["lastmessage"]) > 209):
                bot.reply_to(
                    message,
                    "Количество знаков превышает допустимое! Разрешено до: 209 знаков!",
                )
                raise Exception("too many symbols")
            elif ((abonent == "111") or (abonent == "1123A")) and (
                len(user["lastmessage"]) > 116
            ):
                bot.reply_to(
                    message,
                    "Количество знаков превышает допустимое! Разрешено до: 116 знаков!",
                )
                raise Exception("too many symbols")
            # print(len(user["lastmessage"]))
            prepared_msg = user["name"] + msg_regex_cut(user["lastmessage"])
            rmsg = msg_transliterator_en_to_ru(prepared_msg)
            print(rmsg)
            sendmsg = msg_transliterator(rmsg)
            if user["lastnumber"] == "1123A":
                sendmsg = msg_transliterator_ru_to_en(prepared_msg)
            print(sendmsg)
            bot.send_message(chat_id, "Сообщение отправляется...")

            if user["lastnumber"] == "110":
                send_msg_to_pgr("0000110", "160037000", sendmsg)
            elif user["lastnumber"] == "121":
                if user["limited_access"]:
                    bot.reply_to(
                        message, "Для отправки на этот номер нужно иметь допуск!"
                    )
                    raise Exception("poputal malenko")
                send_msg_to_pgr(
                    "0000121", "160037000", sendmsg
                )  # 0000121 = CAPCODE / 160037000 = Frequency
            elif user["lastnumber"] == "122":
                send_msg_to_pgr("0000122", "160037000", sendmsg)
            elif user["lastnumber"] == "111":
                send_msg_to_pgr("0000111", "160037000", sendmsg)
            elif user["lastnumber"] == "3123":
                send_msg_to_pgr("0003123", "160037000", sendmsg)
            elif user["lastnumber"] == "1123A":
                send_msg_to_pgr("0001123A", "160037000", sendmsg)
            else:
                bot.reply_to(message, "Такой номер не существует!")
                raise Exception("Unknown num")
        else:
            bot.reply_to(message, "Такой номер не существует!")
            raise Exception("Unknown num")
        if user["lastnumber"] == "1123A":
            msg = bot.send_message(
                chat_id,
                "Сообщение отправлено!\nОт кого: "
                + user["name"]
                + "\nКому: "
                + user["lastnumber"]
                + "\nВаше сообщение:\n"
                + prepared_msg
                + "\n\nЧто придет абоненту:\n"
                + sendmsg,
            )
            bot.register_next_step_handler(msg, process_message_step)
        else:
            msg = bot.send_message(
                chat_id,
                "Сообщение отправлено!\nОт кого: "
                + user["name"]
                + "\nКому: "
                + user["lastnumber"]
                + "\nТекст в кодировке Advisor:\n"
                + sendmsg
                + "\n\nЧто придет абоненту:\n"
                + rmsg,
            )
            bot.register_next_step_handler(msg, process_message_step)
        # msg = bot.send_message(chat_id, 'Сообщение отправлено!\nОт кого: ' + user["name"] + '\nКому: ' + user["lastnumber"] + '\nТекст в кодировке Advisor:\n' + sendmsg + '\n\nЧто придет абоненту:\n' + rmsg)

    except Exception as e:
        print(e)
        msg = bot.reply_to(message, "Ошибка!")
        bot.register_next_step_handler(msg, process_message_step)


# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

print("Bot started!")
bot.infinity_polling()
