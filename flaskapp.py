from flask import Flask, request
from telegram import Bot, ReplyKeyboardMarkup, KeyboardButton
import config

app = Flask(__name__)
TOKEN = "7214563574:AAHDLhMld2h8ByhvKPvKNjcUzkqyZzlI_js"
bot = Bot(token=TOKEN)

keyboard = ReplyKeyboardMarkup([
    [KeyboardButton(text="👍"), KeyboardButton(text='👎')],
    [KeyboardButton(text="🆑")]
], resize_keyboard=True)

def file_write(like, dislike):
    with open("bot-deploy/results.txt", 'w') as file:
        file.write(f'{like}:{dislike}')

def read_results():
    with open("bot-deploy/results.txt", 'r') as file:
        file_read = file.read()
    data = file_read.split(':')
    like, dislike = data[0], data[1]
    return like, dislike

def check_likes():
    with open("bot-deploy/results.txt", 'r') as file:
        file_read = file.read()
        if ":" in file_read:
            return True
        else:
            return False

@app.route('/', methods=["POST"])
def main():
    like_count = 0
    dislike_count = 0
    data = request.get_json()
    chat_id = data['message']['from']['id']
    text = data['message'].get("text")
    first_name = data['message']['from']['first_name']
    if text != None:
        if text == '/start':
            bot.send_message(chat_id=chat_id, text= f"Hello {first_name}",reply_markup=keyboard)
        else:
            if text == "👍":
                if check_likes():
                    like, dislike = read_results()
                    like = int(like) + 1
                    file_write(like, dislike)
                    like_count, dislike_count = read_results()
                    text_like = f""""🔥 likes: {like_count}\n💣 dislikes: {dislike_count}"""
                    bot.send_message(chat_id=chat_id, text= text_like)
                else:
                    file_write(1, 0)
                    like_count, dislike_count = read_results()
                    text_like = f""""🔥 likes: {like_count}\n💣 dislikes: {dislike_count}"""
                    bot.send_message(chat_id=chat_id, text= text_like)

            elif text == "👎":
                dislike_count += 1
                text_like = f""""🔥 likes: {like_count}\n💣 dislikes: {dislike_count}"""
                bot.send_message(chat_id=chat_id, text= text_like)
            elif text == "🆑":
                like_count = 0
                dislike_count = 0
                text_like = f""""🔥 likes: {like_count}\n💣 dislikes: {dislike_count}"""
                bot.send_message(chat_id=chat_id, text= text_like)
            else:
                bot.send_message(chat_id=chat_id, text= text)

    else:
        bot.send_message(chat_id=chat_id, text= "Faqat button yuboring!")
    print(data)


    return data

@app.route('/home')
def home():
    return "Hello world"

if __name__ == '__main__':
    app.run(port=8080, debug=True)