from BackLogic import kb, delete_message, ban_user, ban_checking, conditions
from settings import bot, admin_id


@bot.message_handler(func=lambda message: True)
def message_hand(message):
    conditions(message)


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    if ban_checking(message):
        bot.send_message(message.chat.id, "You were banned")
    else:
        file_id = message.photo[-1].file_id
        bot.send_photo(admin_id, file_id, caption=f"{message.caption}\n{message.chat.id}\n@{message.chat.username}", reply_markup=kb(message), parse_mode="Markdown")
        bot.send_message(message.chat.id, "Message sent✅")


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    command = call.data
    print(command)
    if command == "delete":
        delete_message(call)
    elif command == "add_ban":
        ban_user(call)
        delete_message(call)
    # elif command == "delete_all":
    #     delete_all_messages(call)


bot.polling()
