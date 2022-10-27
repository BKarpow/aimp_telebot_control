import pyaimp
import telebot
import query_lib as q
from os import getenv
from telebot import types
from loguru import logger
from pathlib import Path

log_file = Path('accsss.log')
logger.add(str(log_file.absolute()), rotation="20 KB", compression="zip")
# Access control from chat id
verify_chat_ids = getenv("ACCESS_CHAT_IDS").split(',')
bot = telebot.TeleBot(getenv("TG_TOKEN"))


def client_aimp():
    return pyaimp.Client()


def is_verify_user(message) -> bool:
    return str(message.chat.id) in verify_chat_ids


def get_keyboard():
    amp = client_aimp()
    shuff_button = "🔀 Увімкнути" if not amp.is_shuffled() else "🔀 Вимкнути"
    markup = types.InlineKeyboardMarkup(row_width=4)
    prev = types.InlineKeyboardButton('<<<', callback_data='prev')
    play = types.InlineKeyboardButton('▶ ⏸', callback_data='play_pause')
    next_track = types.InlineKeyboardButton('>>>', callback_data='next')
    shuff = types.InlineKeyboardButton(shuff_button, callback_data='shuffle')
    vol_25 = types.InlineKeyboardButton("🔈 25%", callback_data='vol_25')
    vol_50 = types.InlineKeyboardButton("🔈 50%", callback_data='vol_50')
    vol_75 = types.InlineKeyboardButton("🔈 75%", callback_data='vol_75')
    vol_100 = types.InlineKeyboardButton("🔈 100%", callback_data='vol_100')
    update = types.InlineKeyboardButton("🗘 Оновити", callback_data='update')
    markup.add(prev, play, next_track, shuff, vol_25, vol_50, vol_75, vol_100, update)
    return markup


@bot.message_handler(commands=['start'])
def cmd_start(message):
    logger.info(f"Run command start. Chat id: {message.chat.id}")
    if not is_verify_user(message):
        logger.error(f"Немає у Вас доступу, шановний. Chat id: {message.chat.id}")
        bot.send_message(message.chat.id, "Немає у Вас доступу, шановний!")
        return
    try:
        aimp = client_aimp()
        info = aimp.get_current_track_info()
        msg = f"Зараз грає\n{info['artist']} {info['title']}."
        bot.send_message(message.chat.id, msg, reply_markup=get_keyboard())
    except RuntimeError as e:
        logger.error(f"AIMP not running: {e}")
        bot.send_message(
            message.chat.id,
            "AIMP не запушено! Запустіть AIMP та виконаййте крманду /start ."
        )


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    try:
        amp = client_aimp()
        if call.message:
            if call.data == 'prev':
                q.go_prev(bot, amp, call, get_keyboard)
            elif call.data == 'update':
                q.go_update(bot, amp, call, get_keyboard)
            elif call.data == 'next':
                q.go_next(bot, amp, call, get_keyboard)
            elif call.data == 'play_pause':
                q.go_play_pause(bot, amp, call, get_keyboard)
            elif call.data == "shuffle":
                q.go_shuffle(bot, amp, call, get_keyboard)
            elif call.data == "vol_25":
                q.go_set_volume(25, bot, amp, call, get_keyboard)
            elif call.data == "vol_50":
                q.go_set_volume(50, bot, amp, call, get_keyboard)
            elif call.data == "vol_75":
                q.go_set_volume(75, bot, amp, call, get_keyboard)
            elif call.data == "vol_100":
                q.go_set_volume(100, bot, amp, call, get_keyboard)
            else:
                q.go_no_command(bot, call, get_keyboard)
    except RuntimeError as e:
        logger.error(f"AIMP not running: {e}")
        bot.send_message(
            call.message.chat.id,
            "AIMP не запушено! Запустіть AIMP та виконаййте крманду /start ."
        )


@bot.message_handler(commands=['mute'])
def com_mute(message):
    try:
        c = client_aimp()
        c.set_muted(not(c.is_muted()))
        bot.send_message(message.chat.id, "Мут ...")
    except RuntimeError as e:
        logger.error(f"AIMP not running: {e}")
        bot.send_message(
            message.chat.id,
            "AIMP не запушено! Запустіть AIMP та виконаййте крманду /start ."
        )


@bot.message_handler(commands=['info'])
def com_info(message):
    try:
        c = client_aimp()
        info = c.get_current_track_info()
        msg = f"Зараз грає\n{info['artist']} {info['title']}."
        bot.send_message(message.chat.id, msg)
    except RuntimeError as e:
        logger.error(f"AIMP not running: {e}")
        bot.send_message(
            message.chat.id,
            "AIMP не запушено! Запустіть AIMP та виконаййте крманду /start ."
        )


if __name__ == '__main__':
    logger.info("Bot running!")
    logger.debug(f"Verify access from chat ids {verify_chat_ids}")
    try:
        bot.infinity_polling()
    except:
        logger.error('Помилка в пулінгу Telegram...')

