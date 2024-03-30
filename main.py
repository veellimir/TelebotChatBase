import os
import requests
import json
import telepot
import time
from os import listdir, mkdir
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv

load_dotenv()

CHATBASE_API = os.getenv('CHATBASE_API')
CHATBASE_ID = os.getenv('CHATBASE_ID')
TELEBOT_TOKEN = os.getenv('TELEBOT_TOKEN')

welcome_messages = [
    """Привет! Я чат бот компании Intetix и готов рассказать тебе всё про создание музеев и выставок!
    Задай любой вопрос в этот чат текстом или выбери готовый вопрос. С чего начнем?"""
]


def send_request(id_, text):
    chatbase_url = 'https://www.chatbase.co/api/v1/chat'
    requests_headers = {
        'Authorization': f'Bearer {CHATBASE_API}',
        'Content-Type': 'application/json'
    }
    chat_data = {
        'conversationId': id_,
        'messages': [],
        'chatbotId': CHATBASE_ID,
        'stream': False,
        'temperature': 0
    }
    chat_data['messages'].append({'content': text, 'role': 'user'})
    response = requests.post(chatbase_url, headers=requests_headers, data=json.dumps(chat_data))
    response_data = response.json()

    if response.status_code == 200:
        output = response_data['text']
        chat_data['messages'].append({'content': response_data['text'], 'role': 'assistant'})

        for message in chat_data['messages']:
            message['content'] = ''

        with open(f'data/{id_}.json', 'w') as f:
            json.dump(chat_data, f)
        return output
    else:
        output = response_data['message']
        return output


def send_message_with_buttons(chat_id):
    keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Расскажи про кейс музея')],
        [KeyboardButton(text='Корпоративные музеи')],
        [KeyboardButton(text='Краеведческие и отраслевые музеи')],
        [KeyboardButton(text='Школьные музеи')],
        [KeyboardButton(text='Музейное проектирование')],
        [KeyboardButton(text='Макеты и экспонаты')],
        [KeyboardButton(text='Видео, графический контент ПО для музея, AR & VR')],
    ])
    telegram_bot.sendMessage(
        chat_id,
        'Напиши вопрос или воспользуйся кнопками быстрых сообщений',
        reply_markup=keyboard
    )


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    chat_id = str(chat_id)

    if content_type == 'text' and (msg['text'] == '/start' or f'{chat_id}.json' not in listdir('data')):
        for message in welcome_messages:
            telegram_bot.sendMessage(chat_id, message)

        send_message_with_buttons(chat_id)
        with open(f'data/{chat_id}.json', 'w') as f:
            json.dump({
                'conversationId': chat_id,
                'messages': [],
                'chatbotId': CHATBASE_ID,
                'stream': False,
                'temperature': 0}, f
            )
    elif content_type == 'text' and msg['text'].strip():
        time.sleep(0.6)
        telegram_bot.sendMessage(chat_id, 'Секунду... 😊')

        response = send_request(chat_id, msg['text'])
        telegram_bot.sendMessage(chat_id, response)
        send_message_with_buttons(chat_id)


if 'data' not in listdir('./'):
    mkdir('data')

telegram_bot = telepot.Bot(TELEBOT_TOKEN)
MessageLoop(telegram_bot, handle).run_as_thread()

print('Listening ...')

while 1:
    time.sleep(10)



























































