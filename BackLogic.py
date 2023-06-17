from settings import bot, ban_list, admin_id
from telebot import types
import telebot

content_type = None


def get_user(text, symbol, integer):
    name = text.split(symbol)
    return name[len(name)-integer]


def kb(message):
    keyboard = types.InlineKeyboardMarkup()
    ban_button = types.InlineKeyboardButton(text='📛', callback_data='add_ban')
    delete_button = types.InlineKeyboardButton(text='❎', callback_data='delete')
    person_button = types.InlineKeyboardButton(text='🚻', callback_data='account')
    delall_button = types.InlineKeyboardButton(text='❌', callback_data='delete_all')
    keyboard.add(ban_button, delall_button, delete_button, person_button)
    return keyboard


def delete_message(call):
    c_id = call.message.chat.id
    m_id = call.message.message_id
    bot.delete_message(c_id, m_id)


def ban_user(call):
    ban_list.insert_one({"username": get_user(call.message.text, "@", 1)})


def ban_checking(message):
    ban_list1 = list(ban_list.find())
    username = message.chat.username
    banned_user = next((user for user in ban_list1 if user.get("username") == username), None)
    return banned_user


def unban(string):
    updated = string.replace("/unban @", "")
    ban_list.delete_one({"username": updated})


def conditions(message):
    txt = message.text
    if txt.startswith("/unban ") and message.chat.id == admin_id:
        unban(txt)
        bot.send_message(admin_id, "User successfully unbanned")

    elif ban_checking(message):
        bot.send_message(message.chat.id, "You were banned")

    elif txt == "/start":
        bot.send_message(message.chat.id, f"Hello, {message.chat.first_name}, its supporting bot, write here your problem and admin will answer")
        print(txt)

    elif message.reply_to_message and message.chat.id == admin_id:
        bot.send_message(get_user(message.reply_to_message.text, "`", 2), txt)

    else:
        user_message = f"{txt}\n`{message.chat.id}`\n@{message.chat.username}"
        bot.send_message(admin_id, user_message, reply_markup=kb(message))
        bot.send_message(message.chat.id, "Message sent✅")






# def delete_all_messages(call):
#     c_id = call.message.chat.id
#     username_part = call.message.text.split("@")
#     username = username_part[len(username_part)-1]
#     print(username)
    # if username:
    #     messages = bot.get_chat_history(c_id)
    #     for message in messages:
    #         if username in message.text:
    #             bot.delete_message(c_id, message.message_id)
    #     bot.send_message(c_id, f"All messages mentioning @{username} have been deleted.")
    # else:
    #     bot.send_message(c_id, "No username found in the message caption.")
