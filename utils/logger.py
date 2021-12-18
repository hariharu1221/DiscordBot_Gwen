from datetime import datetime
import os
import traceback

from config import Config


def err(error):
    try:
        raise error
    except Exception:
        error_message = traceback.format_exc()
        log(f'[오류] {error_message}\n\n', True)
        return error_message


def warn(msg: str):
    log(f'[경고] {msg}')


def info(msg: str):
    log(f'[정보] {msg}')


def debug(msg: str):
    if Config.is_debug:
        log(f'[디버그] {msg}')


def msg(message):
    if message.content == '':
        return
    author = message.author
    if 'DM' in str(type(message.channel)):
        log_msg = f'DM <{author.name}> {message.content}'
    else:
        guild = message.guild
        channel = message.channel
        log_msg = f'{guild.name} <{channel.name} | {author.name} | {author.id}> {message.content}'

    log(log_msg)


def log(msg: str, iserror=False):
    now = datetime.now()
    hour = now.strftime("%H")
    minute = now.strftime("%M")
    log_msg = f'{hour}시 {minute}분 / {msg}'
    print(log_msg)
    save(log_msg)
    if iserror:
        save_error(log_msg)


def save(msg):
    if not(os.path.isdir('logs')):
        os.makedirs(os.path.join('logs'))
    now = datetime.now()
    time_text = now.strftime('%Y-%m-%d')
    if not os.path.isfile("logs/log_" + time_text + ".txt"):
        f = open("logs/log_" + time_text + ".txt", 'w', encoding='utf-8')
    else:
        f = open("logs/log_" + time_text + ".txt", 'a', encoding='utf-8')
    f.write(msg + '\n')
    f.close()


def save_error(msg):
    now = datetime.now()
    time_text = now.strftime('%Y-%m-%d')
    if not os.path.isfile("logs/error_log_" + time_text + ".txt"):
        f = open("logs/error_log_" + time_text + ".txt", 'w', encoding='utf-8')
    else:
        f = open("logs/error_log_" + time_text + ".txt", 'a', encoding='utf-8')
    f.write(msg + '\n')
    f.close()
