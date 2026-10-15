import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.types import *
from datetime import timedelta
from aiogram.utils import executor

logging.basicConfig(level=logging.INFO)

API_TOKEN = '6082663790:AAEqFqwLSIl3kqEZ12d0SFMCqEuIZBoDBs4'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

warnings = 0


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    print(message.chat.type)
    if message.chat.type in ["supergroup", "group"]:
        await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")



@dp.message_handler(commands=['help'])
async def echo(message: types.Message):
    if message.chat.type in ["supergroup", "group"]:
        await message.reply("I'm bot group. My commands:\n"
                        "/start - begin bot\n"
                        "/mute - Give you mute 30 minutes\n"
                        "/ban - Ban user\n"
                        "/warn - give you warn")

@dp.message_handler(commands=['mute'], is_chat_admin=True)
async def cmd_mute(message: types.Message):
    if message.chat.type in ["supergroup", "group"]:
        if not message.reply_to_message or not message.reply_to_message:
            await message.reply("Please answer to message user")
            return

        user_to_mute = message.reply_to_message.from_user

        perm = ChatPermissions(
            can_send_messages=False,
        )
        await bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=user_to_mute.id,
            permissions=perm,
            until_date=message.date + timedelta(minutes=30)
        )
        await message.reply("")

@dp.message_handler(commands=['unban'], is_chat_admin=True)
async def cmd_mute(message: types.Message):
    if message.chat.type in ["supergroup", "group"]:
        if not message.reply_to_message or not message.reply_to_message:
            await message.reply("Please answer to message user")
            return

        user_to_ban = message.reply_to_message.from_user

        await bot.unban_chat_member(message.chat.id, user_to_ban.id, only_if_banned=True)
        await message.reply("")


@dp.message_handler(commands=['unmute'], is_chat_admin=True)
async def cmd_mute(message: types.Message):
    if message.chat.type in ["supergroup", "group"]:
        if not message.reply_to_message or not message.reply_to_message:
            await message.reply("Please answer to message user")
            return

        user_to_mute = message.reply_to_message.from_user

        perm = ChatPermissions(
            can_send_messages=True,
        )
        await bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=user_to_mute.id,
            permissions=perm,
            until_date=message.date + timedelta(minutes=30)
        )
        await message.reply("")

@dp.message_handler(commands=['ban'], is_chat_admin=True)
async def cmd_mute(message: types.Message):
    if message.chat.type in ["supergroup", "group"]:
        if not message.reply_to_message or not message.reply_to_message:
            await message.reply("Please answer to message user")
            return

        user_to_ban = message.reply_to_message.from_user

        await bot.kick_chat_member(message.chat.id, user_to_ban.id)

        await message.reply(f"User {user_to_ban.mention} to be ban.")

@dp.message_handler(commands=['warn'], is_chat_admin=True)
async def cmd_warn(message: types.Message):
     global warnings

     if not message.reply_to_message or not message.reply_to_message.from_user:
        await message.reply("Пожалуйста, ответьте на сообщение пользователя, чтобы выдать предупреждение.")
        return

    user_to_warn = message.reply_to_message.from_user

if warnings >= 3:
        perm = ChatPermissions(
                can_send_messages=False,
        )
        await bot.restrict_chat_member(
                    message.chat.id,
                    user_to_warn.id,
                    permissions=perm,
                    until_date=message.date + timedelta(minutes=5)
        )
    await message.reply(f"Пользователь {user_to_warn.mention} получил мут на 5 минут за нарушение правил.")
    warnings = 0
    return

warnings += 1


     await message.reply(f"Пользователь {user_to_warn.mention} получил предупреждение ({warnings}/3).")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)