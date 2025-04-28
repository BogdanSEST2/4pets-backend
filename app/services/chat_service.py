def get_all_chats():
    return {"message": "Тут будут все чаты"}


def send_message(chat_id, user_id, message):
    return {"message": f"Сообщение в чат {chat_id} от юзера {user_id}: {message}"}
