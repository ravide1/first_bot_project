import telebot
import info

t = "6943717447:AAGwkZ3Fpj-R4yi4jYi5tVQvEz8bXWpVJ44"

character_names = info.get_character_names_list()

last_command = ""

current_character_name = ""

bot = telebot.TeleBot(token=t)

@bot.message_handler(commands=["start"])
def handle_command_start(message):
    global last_command
    last_command = "start"
    bot.send_message(message.chat.id, f"Привет, меня зовут { bot.get_my_name().name}."
                              f"\n Я могу рассказать тебе о персонажах игры GTA V, к сожалению не о всех, но основные в их составе есть.\n"
                              f"С помощью комманды \"/help\" ты можешь ознакомиться с коммандами")
@bot.message_handler(commands=["help"])
def handle_command_help(message):
    global last_command
    last_command = "help"
    bot.send_message(message.chat.id, "С помощью комманды \"/get_character_names\" ты можешь получить список имен персонажей,"
                              "о которых можешь получить информацию.\n"
                              "С помощью комманды \"/set_name\" ты можешь выбрать персонажа, о котором хочешь получить информацию\n"
                              "С помощью комманды \"/get_description\" после выбора персонажа, вы сможите прочитать описание песонажа.\n"
                              "С помощью комманды \"/get_voiced_by\" после выбора персонажа, ты можешь узнать кем он был озвучен."
                              "С помощью комманды \"/cancel\" вы можете отменить ввод параметров последней комманды")

@bot.message_handler(commands=["get_character_names"])
def handle_command_help(message):
    global last_command
    last_command = "get_character_names"
    bot.send_message(message.chat.id, f" Имена персонажей, информация о которых доступна боту - {character_names}")

@bot.message_handler(commands=["set_name"])
def handle_command_set_name(message):
    global last_command
    last_command = "set_name"
    bot.send_message(message.chat.id, "Введите имя персонажа, о котором хотели бы получить информацию:")

@bot.message_handler(commands=["cancel"])
def handle_command_cancel(message):
    global last_command
    bot.send_message(message.chat.id, f"Ввод параметров комманды {last_command} отменен")
    last_command = ""

@bot.message_handler(commands=["get_description"])
def handle_command_get_description(message):
    global last_command
    last_command = "get_description"
    if current_character_name == "":
        last_command = "set_name"
        bot.send_message(message.chat.id, f"Имя не заданно, используйте комманду \"/set_name\", чтобы задать имя")
    else:
        current_character_description = info.find_charracter_by_name(current_character_name)["description"]
        bot.send_message(message.chat.id, f"Описание персонажа {current_character_name}: {current_character_description}")

@bot.message_handler(commands=["get_voiced_by"])
def handle_command_get_voiced_by(message):
    global last_command
    last_command = "get_voiced_by"
    if current_character_name == "":
        last_command = "set_name"
        bot.send_message(message.chat.id, f"Имя не заданно, используйте комманду \"/set_name\", чтобы задать имя")
    else:
        current_character_voiced = info.find_charracter_by_name(current_character_name)["voiced_by"]
        bot.send_message(message.chat.id, f"Персонаж {current_character_name}: {current_character_voiced}")

@bot.message_handler(content_types=["text"])
def handle_text_message(message):
    global last_command
    global current_character_name
    if last_command == "set_name":
        if info.check_character_exists(message.text):
            current_character_name = info.find_charracter_by_name(message.text)["name"]
            bot.send_message(message.chat.id, f"Вы выбрали персонажа \"{current_character_name}\"")
        else:
            bot.send_message(message.chat.id, "к сожалению имя введено неверно,  попробуйте еще раз.")

bot.polling()
