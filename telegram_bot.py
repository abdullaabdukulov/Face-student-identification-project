import json
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler
import numpy as np
import face_recognition

TOKEN = '5128866034:AAHktgDUfM6B0coUlsVBbv1qQ5rvcvHsnkE'
admin_id = '2143798298'


def start_command(update, context):
    update.message.reply_text(
        text=f'Assalom Alekum! {update.message.from_user.first_name.title()},\nAstrum It akademiyasining studentlarini Face orqali aniqlash xizmatiga xush kelibsiz!')
    # context.bot.send_message(chat_id=admin_id, text=f'Ismi: {update.message.from_user.first_name}\nFoydalanuvchi ismi: {update.message.from_user.username}\nBotga start bosdi.')


def message_handler(update, context):
    message = update.message.text
    if message:
        update.message.reply_text(
            text=f'Hurmatli {update.message.from_user.first_name.title()} botga faqat rasm tashlashingiz mumkin!')


def photo_handler(update, context):
    file = update.message.photo[-1].file_id
    obj = context.bot.get_file(file)
    obj.download("photos/test_photo/test.jpg")

    with open("astrum_students.json") as json_file:
        data = json.load(json_file)

    face_encodings = [np.asarray(i['encode']) for i in data]
    face_names = [f"Astrum  o'quvchisi.\nYo'nalishi:  {i['dir']}\nToliq ismi  {i['name']}" for i in data]

    bot_to_pic = face_recognition.load_image_file("photos/test_photo/test.jpg")
    w = 0
    try:
        bot_encode_pic = face_recognition.face_encodings(bot_to_pic)[0]
        w = face_recognition.api.compare_faces(face_encodings, bot_encode_pic, tolerance=0.5)
    except:
        update.message.reply_text(text='Faqat shaxsning yuz qiyofasini tashlang!')

    if True not in w:  update.message.reply_text(f"Bu o'quvchi bizda yo'q")
    for idx, i in enumerate(w):
        if i:
            update.message.reply_text(f"{face_names[idx]}")


def main():
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start_command))
    dispatcher.add_handler(MessageHandler(Filters.text, message_handler))
    dispatcher.add_handler(MessageHandler(Filters.photo, photo_handler))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
