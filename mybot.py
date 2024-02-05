import telebot
import speech_recognition as sr
import subprocess

API_TOKEN = '6263296106:AAGc8bZlf8CM45Y60wZ3hdhTIgtx7_ylQvw'

bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет, я бот для конвертации аудиофайлов в текст. Отправь мне аудио и я "
                                      "преобразую его в текст.")


@bot.message_handler(content_types=["audio"])
def handle_audio(message):
    try:
        chat_id = message.chat.id
        audio_info = bot.get_file(message.audio.file_id)
        audio_file = bot.download_file(audio_info.file_path)

        with open('audiofile.mp3', 'wb') as f:
            f.write(audio_file)

        bot.send_message(chat_id, "Преобразую аудио в текст: ")
        text = convert()
        bot.reply_to(message, text)
    except Exception as e:
        bot.reply_to(message, e)


def convert():
    subprocess.call(['ffmpeg', '-i', 'audiofile.mp3', '-vn', '-acodec', 'pcm_s16le', '-ar', '44100', '-f', 'wav', 'temp.wav'])

    r = sr.Recognizer()

    with sr.AudioFile('temp.wav') as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data)

    subprocess.call(['rm', 'temp.wav'])
    return text


bot.infinity_polling()
