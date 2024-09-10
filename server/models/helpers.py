from server.models.chatModels import ChatMessage


def add_message(chat_session, user, text):
    new_message = ChatMessage(chat_session=chat_session, sender=user, text=text)
    new_message.save()
