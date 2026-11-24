import os
import random
import asyncio
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import ChatAdminRequired
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong, PeerIdInvalid
from info import (
    ADMINS, LOG_CHANNEL, SUPPORT_CHAT, MELCOW_NEW_USERS, PICS,
    DATABASE_URI, DATABASE_URI2, DATABASE_URI3, DATABASE_URI4, DATABASE_URI5,
    POSTGRES_STORAGE_LIMIT_BYTES,
)
from database.users_chats_db import db
from database.ia_filterdb import Media
from utils import get_size, temp, get_settings
from Script import script

MONGO_DB_CAP_BYTES = 536870912
MONGO_DB_COUNT = len([u for u in (DATABASE_URI, DATABASE_URI2, DATABASE_URI3, DATABASE_URI4, DATABASE_URI5) if u])
ADDLIST_URL = "https://t.me/addlist/ueNwQploRbQ1MGM1"


def _get_support_url():
    if SUPPORT_CHAT:
        if SUPPORT_CHAT.startswith(("http://", "https://")):
            return SUPPORT_CHAT
        return f"https://t.me/{SUPPORT_CHAT.lstrip('@')}"
    return ADDLIST_URL


@Client.on_message(filters.new_chat_members & filters.group)
async def save_group(bot, message):
    r_j_check = [u.id for u in message.new_chat_members]
    if temp.ME in r_j_check:
        if not await db.get_chat(message.chat.id):
            total = await bot.get_chat_members_count(message.chat.id)
            r_j = message.from_user.mention if message.from_user else "Anonymous"
            await bot.send_message(
                LOG_CHANNEL,
                script.LOG_TEXT_G.format(message.chat.title, message.chat.id, total, r_j),
            )
            await db.add_chat(message.chat.id, message.chat.title)
        if message.chat.id in temp.BANNED_CHATS:
            buttons = [[
                InlineKeyboardButton('📢 ᴄʜᴀɴɴᴇʟs', url=_get_support_url())
            ]]
            reply_markup = InlineKeyboardMarkup(buttons)
            k = await message.reply(
                text='<b>❌ ဤ Group တွင် Bot အသုံးပြုခွင့် ပိတ်ထားပါသည်။</b>',
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML,
            )
            try:
                await k.pin()
            except Exception:
                pass
            await bot.leave_chat(message.chat.id)
            return
        buttons = [[
            InlineKeyboardButton('📢 ᴊᴏɪɴ ᴏᴜʀ ᴄʜᴀɴɴᴇʟs', url=ADDLIST_URL)
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_text(
            text=(
                f"<b>🎬 {message.chat.title} Group ထဲသို့ MZP Entertainment Bot ကို ထည့်သွင်းပေးသည့်အတွက် ကျေးဇူးတင်ပါတယ်။</b>\n\n"
                "⚡ Bot ကောင်းမွန်စွာ အလုပ်လုပ်နိုင်ရန် <b>Admin</b> အဖြစ် ခန့်ထားပေးပါ။"
            ),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML,
        )
    else:
        settings = await get_settings(message.chat.id)
        if settings["welcome"]:
            chat_id = message.chat.id
            welcome_markup = InlineKeyboardMarkup([[
                InlineKeyboardButton('📢 ᴊᴏɪɴ ᴏᴜʀ ᴄʜᴀɴɴᴇʟs', url=ADDLIST_URL)
            ]])
            for u in message.new_chat_members:
                if temp.MELCOW.get(chat_id) is not None:
                    try:
                        await temp.MELCOW[chat_id].delete()
                    except Exception:
                        pass
                welcome_caption = (
                    f"👋 မင်္ဂလာပါ {u.mention}\n\n"
                    f"🎬 <b>{message.chat.title}</b> မှ ကြိုဆိုပါတယ်။\n"
                    "ဇာတ်ကားနာမည် ရိုက်ထည့်ပြီး အလွယ်တကူ ရှာဖွေကြည့်ရှုနိုင်ပါတယ် 😉"
                )
                try:
                    temp.MELCOW[chat_id] = await message.reply_photo(
                        photo=random.choice(PICS),
                        caption=welcome_caption,
                        reply_markup=welcome_markup,
                        parse_mode=enums.ParseMode.HTML,
                    )
                except Exception:
                    temp.MELCOW[chat_id] = await message.reply_text(
                        text=welcome_caption,
                        reply_markup=welcome_markup,
                        parse_mode=enums.ParseMode.HTML,
                    )


@Client.on_message(filters.command('leave') & filters.user(ADMINS))
async def leave_a_chat(bot, message):
    if len(message.command) == 1:
        return await message.reply('Give me a chat id')
    chat = message.command[1]
    try:
        chat = int(chat)
    except Exception:
        chat = chat
    try:
        buttons = [[
            InlineKeyboardButton('📢 ᴊᴏɪɴ ᴏᴜʀ ᴄʜᴀɴɴᴇʟs', url=_get_support_url())
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await bot.send_message(
            chat_id=chat,
            text='<b>Admin ညွှန်ကြားချက်အရ ဤ Group မှ ထွက်ခွာလိုက်ပါပြီ။</b>',
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML,
        )
        await bot.leave_chat(chat)
        await message.reply(f"Left the chat `{chat}`")
    except Exception as e:
        await message.reply(f'Error - {e}')


@Client.on_message(filters.command('disable') & filters.user(ADMINS))
async def disable_chat(bot, message):
    if len(message.command) == 1:
        return await message.reply('Give me a chat id')
    r = message.text.split(None)
    if len(r) > 2:
        reason = message.text.split(None, 2)[2]
        chat = message.text.split(None, 2)[1]
    else:
        chat = message.command[1]
        reason = "No reason Provided"
    try:
        chat_ = int(chat)
    except Exception:
        return await message.reply('Give Me A Valid Chat ID')
    cha_t = await db.get_chat(int(chat_))
    if not cha_t:
        return await message.reply("Chat Not Found In DB")
    if cha_t['is_disabled']:
        return await message.reply(f"This chat is already disabled:\nReason-<code> {cha_t['reason']} </code>")
    await db.disable_chat(int(chat_), reason)
    if int(chat_) not in temp.BANNED_CHATS:
        temp.BANNED_CHATS.append(int(chat_))
    await message.reply('Chat Successfully Disabled')
    try:
        buttons = [[
            InlineKeyboardButton('📢 ᴊᴏɪɴ ᴏᴜʀ ᴄʜᴀɴɴᴇʟs', url=_get_support_url())
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await bot.send_message(
            chat_id=chat_,
            text=f'<b>Admin ညွှန်ကြားချက်အရ ဤ Group မှ ထွက်ခွာလိုက်ပါပြီ။</b>\nReason : <code>{reason}</code>',
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML,
        )
        await bot.leave_chat(chat_)
    except Exception as e:
        await message.reply(f"Error - {e}")


@Client.on_message(filters.command('enable') & filters.user(ADMINS))
async def re_enable_chat(bot, message):
    if len(message.command) == 1:
        return await message.reply('Give me a chat id')
    chat = message.command[1]
    try:
        chat_ = int(chat)
    except Exception:
        return await message.reply('Give Me A Valid Chat ID')
    sts = await db.get_chat(int(chat_))
    if not sts:
        return await message.reply("Chat Not Found In DB !")
    if not sts.get('is_disabled'):
        return await message.reply('This chat is not yet disabled.')
    await db.re_enable_chat(int(chat_))
    if int(chat_) in temp.BANNED_CHATS:
        temp.BANNED_CHATS.remove(int(chat_))
    await message.reply("Chat Successfully re-enabled")


@Client.on_message(filters.command('stats') & filters.incoming)
async def get_stats(bot, message):
    if message.from_user and message.from_user.id in ADMINS:
        rju = await message.reply('<b>𝙰𝙲𝙲𝙴𝚂𝚂𝙸𝙽𝙶 𝚂𝚃𝙰𝚃𝚄𝚂 𝙳𝙴𝚃𝙰𝙸𝙻𝚂...</b>')
        total_users = await db.total_users_count()
        totl_chats = await db.total_chat_count()
        files = await Media.count_documents()
        size = await db.get_db_size()
        if DATABASE_URI:
            free_value = max(0, (MONGO_DB_CAP_BYTES * max(MONGO_DB_COUNT, 1)) - size)
            free = get_size(free_value)
        else:
            if POSTGRES_STORAGE_LIMIT_BYTES > 0:
                free_value = max(0, POSTGRES_STORAGE_LIMIT_BYTES - size)
                free = get_size(free_value)
            else:
                free = "Plan based (set POSTGRES_STORAGE_LIMIT_BYTES)"
        size = get_size(size)
        await rju.edit(script.STATUS_TXT.format(files, total_users, totl_chats, size, free))
    else:
        k = await message.reply_text("<b>⚠️ ဤ Command သည် Admin များအတွက်သာ ဖြစ်ပါသည်။</b>")
        await asyncio.sleep(10)
        try:
            await k.delete()
            await message.delete()
        except Exception:
            pass


@Client.on_message(filters.command('invite') & filters.user(ADMINS))
async def gen_invite(bot, message):
    if len(message.command) == 1:
        return await message.reply('Give me a chat id')
    chat = message.command[1]
    try:
        chat = int(chat)
    except Exception:
        return await message.reply('Give Me A Valid Chat ID')
    try:
        link = await bot.create_chat_invite_link(chat)
    except ChatAdminRequired:
        return await message.reply("Invite Link Generation Failed, I am Not Having Sufficient Rights")
    except Exception as e:
        return await message.reply(f'Error {e}')
    await message.reply(f'Here is your Invite Link {link.invite_link}')


@Client.on_message(filters.command('ban') & filters.user(ADMINS))
async def ban_a_user(bot, message):
    if len(message.command) == 1:
        return await message.reply('Give me a user id / username')
    r = message.text.split(None)
    if len(r) > 2:
        reason = message.text.split(None, 2)[2]
        chat = message.text.split(None, 2)[1]
    else:
        chat = message.command[1]
        reason = "No reason Provided"
    try:
        chat = int(chat)
    except Exception:
        pass
    try:
        k = await bot.get_users(chat)
    except PeerIdInvalid:
        return await message.reply("This is an invalid user, make sure I have met him before.")
    except IndexError:
        return await message.reply("This might be a channel, make sure it's a user.")
    except Exception as e:
        return await message.reply(f'Error - {e}')
    else:
        jar = await db.get_ban_status(k.id)
        if jar['is_banned']:
            return await message.reply(f"{k.mention} is already banned\nReason: {jar['ban_reason']}")
        await db.ban_user(k.id, reason)
        if k.id not in temp.BANNED_USERS:
            temp.BANNED_USERS.append(k.id)
        await message.reply(f"Successfully banned {k.mention}")


@Client.on_message(filters.command('unban') & filters.user(ADMINS))
async def unban_a_user(bot, message):
    if len(message.command) == 1:
        return await message.reply('Give me a user id / username')
    r = message.text.split(None)
    if len(r) > 2:
        reason = message.text.split(None, 2)[2]
        chat = message.text.split(None, 2)[1]
    else:
        chat = message.command[1]
        reason = "No reason Provided"
    try:
        chat = int(chat)
    except Exception:
        pass
    try:
        k = await bot.get_users(chat)
    except PeerIdInvalid:
        return await message.reply("This is an invalid user, make sure I have met him before.")
    except IndexError:
        return await message.reply("This might be a channel, make sure it's a user.")
    except Exception as e:
        return await message.reply(f'Error - {e}')
    else:
        jar = await db.get_ban_status(k.id)
        if not jar['is_banned']:
            return await message.reply(f"{k.mention} is not yet banned.")
        await db.remove_ban(k.id)
        if k.id in temp.BANNED_USERS:
            temp.BANNED_USERS.remove(k.id)
        await message.reply(f"Successfully unbanned {k.mention}")


@Client.on_message(filters.command('users') & filters.user(ADMINS))
async def list_users(bot, message):
    raju = await message.reply('Getting List Of Users')
    users = await db.get_all_users()
    out = "Users Saved In DB Are:\n\n"
    async for user in users:
        out += f"<a href=tg://user?id={user['id']}>{user['name']}</a>"
        if user['ban_status']['is_banned']:
            out += ' (Banned User)'
        out += '\n'
    try:
        await raju.edit_text(out, parse_mode=enums.ParseMode.HTML)
    except MessageTooLong:
        with open('users.txt', 'w+', encoding='utf-8') as outfile:
            outfile.write(out)
        await message.reply_document('users.txt', caption="List Of Users")
        os.remove('users.txt')


@Client.on_message(filters.command('chats') & filters.user(ADMINS))
async def list_chats(bot, message):
    raju = await message.reply('Getting List Of Chats')
    chats = await db.get_all_chats()
    out = "Chats Saved In DB Are:\n\n"
    async for chat in chats:
        out += f"**Title:** `{chat['title']}`\n**- ID:** `{chat['id']}`"
        if chat['chat_status']['is_disabled']:
            out += ' (Disabled Chat)'
        out += '\n'
    try:
        await raju.edit_text(out)
    except MessageTooLong:
        with open('chats.txt', 'w+', encoding='utf-8') as outfile:
            outfile.write(out)
        await message.reply_document('chats.txt', caption="List Of Chats")
        os.remove('chats.txt')
