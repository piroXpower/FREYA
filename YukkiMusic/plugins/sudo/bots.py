
#
# Copyright (C) 2021-2022 by TeamDeadly@Github, < https://github.com/TeamYukki >.
#
# This file is part of < https://github.com/TeamYukki/YukkiMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/YukkiMusicBot/blob/master/LICENSE >
#
# All rights reserved.

from pyrogram import filters
from pyrogram.types import Message

from config import BANNED_USERS, MONGO_DB_URI, OWNER_ID
from strings import get_command
from YukkiMusic import app
from YukkiMusic.misc import BOTS
from YukkiMusic.utils.database import add_bot, remove_bot
from YukkiMusic.utils.decorators.language import language

# Command
ADDBOT_COMMAND = get_command("ADDBOT_COMMAND")
DELBOT_COMMAND = get_command("DELBOT_COMMAND")
BOTLIST_COMMAND = get_command("BOTLIST_COMMAND")


@app.on_message(
    filters.command(ADDBOT_COMMAND) & filters.user(OWNER_ID)
)
@language
async def botadd(client, message: Message, _):
    if MONGO_DB_URI is None:
        return await message.reply_text(
            "**Due to bot's privacy issues, You can't manage bots when you're using Yukki's Database.\n\n Please fill your MONGO_DB_URI in your vars to use this feature**"
        )
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(_["general_1"])
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        if user.id in BOTS:
            return await message.reply_text(
                _["bot_1"].format(user.mention)
            )
        added = await add_bot(user.id)
        if added:
            BOTS.add(user.id)
            await message.reply_text(_["bot_2"].format(user.mention))
        else:
            await message.reply_text("Failed")
        return
    if message.reply_to_message.from_user.id in BOTS:
        return await message.reply_text(
            _["bot_1"].format(
                message.reply_to_message.from_user.mention
            )
        )
    added = await add_bot(message.reply_to_message.from_user.id)
    if added:
        BOTS.add(message.reply_to_message.from_user.id)
        await message.reply_text(
            _["bot_2"].format(
                message.reply_to_message.from_user.mention
            )
        )
    else:
        await message.reply_text("Failed")
    return


@app.on_message(
    filters.command(DELBOT_COMMAND) & filters.user(OWNER_ID)
)
@language
async def botdel(client, message: Message, _):
    if MONGO_DB_URI is None:
        return await message.reply_text(
            "**Due to bot's privacy issues, You can't manage bots when you're using Yukki's Database.\n\n Please fill your MONGO_DB_URI in your vars to use this feature**"
        )
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(_["general_1"])
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        if user.id not in BOTS:
            return await message.reply_text(_["bot_3"])
        removed = await remove_bot(user.id)
        if removed:
            BOTS.remove(user.id)
            await message.reply_text(_["bot_4"])
            return
        await message.reply_text(f"Something wrong happened.")
        return
    user_id = message.reply_to_message.from_user.id
    if user_id not in BOTS:
        return await message.reply_text(_["bot_3"])
    removed = await remove_bot(user_id)
    if removed:
        BOTS.remove(user_id)
        await message.reply_text(_["bot_4"])
        return
    await message.reply_text(f"Something wrong happened.")


@app.on_message(filters.command(BOTLIST_COMMAND) & ~BANNED_USERS)
@language
async def bot_list(client, message: Message, _):
    text = _["bot_5"]
    count = 0
    for x in OWNER_ID:
        try:
            user = await app.get_users(x)
            user = (
                user.first_name if not user.mention else user.mention
            )
            count += 1
        except Exception:
            continue
        text += f"{count}➤ {user}\n"
    smex = 0
    for user_id in BOTS:
        if user_id not in OWNER_ID:
            try:
                user = await app.get_users(user_id)
                user = (
                    user.first_name
                    if not user.mention
                    else user.mention
                )
                if smex == 0:
                    smex += 1
                    text += _["bot_6"]
                count += 1
                text += f"{count}➤ {user}\n"
            except Exception:
                continue
    if not text:
        await message.reply_text(_["bot_7"])
    else:
        await message.reply_text(text)
