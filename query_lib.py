import time
import pyaimp
from loguru import logger


def go_prev(bot, amp, call, get_keyboard):
    logger.info(f"Prev track. Chat id: {call.message.chat.id}")
    amp.prev()
    time.sleep(.7)
    info = amp.get_current_track_info()
    msg = f"Зараз грає\n{info['artist']} {info['title']}."
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.id,
        text=msg,
        reply_markup=get_keyboard()
    )


def go_next(bot, amp, call, get_keyboard):
    logger.info(f"Next track. Chat id: {call.message.chat.id}")
    amp.next()
    time.sleep(.7)
    info = amp.get_current_track_info()
    msg = f"Зараз грає\n{info['artist']} {info['title']}."
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.id,
        text=msg,
        reply_markup=get_keyboard()
    )


def go_update(bot, amp, call, get_keyboard):
    logger.info(f"Update info. Chat id: {call.message.chat.id}")
    time.sleep(.7)
    info = amp.get_current_track_info()
    msg = f"Зараз грає\n{info['artist']} {info['title']}."
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.id,
        text=msg + "\nUpdated.",
        reply_markup=get_keyboard()
    )


def go_play_pause(bot, amp, call, get_keyboard):
    logger.info(f"Play or pause. Chat id: {call.message.chat.id}")
    time.sleep(.7)
    state = amp.get_playback_state()
    if state == pyaimp.PlayBackState.Playing:
        amp.pause()
        msg = 'На паузі ...'
    elif state == pyaimp.PlayBackState.Paused:
        amp.play()
        info = amp.get_current_track_info()
        msg = f"Зараз грає\n{info['artist']} {info['title']}."
    else:
        msg = "ХЗ..."
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.id,
        text=msg,
        reply_markup=get_keyboard()
    )


def go_shuffle(bot, amp, call, get_keyboard):
    logger.info(f"Shuffled enable/disable. Chat id: {call.message.chat.id}")
    amp.set_shuffled(not (amp.is_shuffled()))
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.id,
        text=call.message.text + " SHUFFLE MODE",
        reply_markup=get_keyboard()
    )


def go_set_volume(vol_percent: int, bot, amp, call, get_keyboard):
    logger.info(f"Volume set {vol_percent}%. Chat id: {call.message.chat.id}")
    amp.set_volume(vol_percent)
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.id,
        text=call.message.text + f"\nVolume: {vol_percent}%",
        reply_markup=get_keyboard()
    )


def go_no_command(bot, call, get_keyboard):
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.id,
        text="Немає такої команди",
        reply_markup=get_keyboard()
    )
