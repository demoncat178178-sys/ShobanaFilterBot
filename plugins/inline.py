import logging
from pyrogram import Client, enums
from pyrogram.errors.exceptions.bad_request_400 import QueryIdInvalid
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultCachedDocument,
    InlineQueryResultCachedPhoto,
    InlineQuery,
)
from database.ia_filterdb import get_search_results
from utils import is_subscribed, get_size, temp
from info import CACHE_TIME, AUTH_USERS, CUSTOM_FILE_CAPTION

logger = logging.getLogger(__name__)
cache_time = 0 if AUTH_USERS else CACHE_TIME
ADDLIST_URL = "https://t.me/addlist/ueNwQploRbQ1MGM1"


async def inline_users(query: InlineQuery):
    if AUTH_USERS:
        if query.from_user and query.from_user.id in AUTH_USERS:
            return True
        return False
    if query.from_user and query.from_user.id not in temp.BANNED_USERS:
        return True
    return False


@Client.on_inline_query()
async def answer(bot, query):
    """Show search results for given inline query"""

    if not await inline_users(query):
        await query.answer(
            results=[],
            cache_time=0,
            switch_pm_text="🚫 အသုံးပြုခွင့် မရှိပါ",
            switch_pm_parameter="start",
        )
        return

    if not await is_subscribed(query.from_user.id, bot):
        await query.answer(
            results=[],
            cache_time=0,
            switch_pm_text="📢 ချန်နယ်များကို အရင် Join ပေးပါ",
            switch_pm_parameter="subscribe",
        )
        return

    results = []
    if '|' in query.query:
        string, file_type = query.query.split('|', maxsplit=1)
        string = string.strip()
        file_type = file_type.strip().lower()
    else:
        string = query.query.strip()
        file_type = None

    try:
        offset = int(query.offset or 0)
    except ValueError:
        offset = 0

    reply_markup = get_reply_markup(query=string)
    files, next_offset, total, search_time = await get_search_results(
        string,
        file_type=file_type,
        max_results=10,
        offset=offset,
        fast=True,
        return_time=True,
    )

    for file in files:
        title = file.file_name or "MZP Entertainment"
        size = get_size(file.file_size)
        f_type = getattr(file, 'file_type', None)
        f_caption = file.caption
        send_id = (
            file.file_ref
            if f_type == 'photo' and getattr(file, 'file_ref', None)
            else file.file_id
        )

        if f_type != 'photo' and CUSTOM_FILE_CAPTION:
            try:
                f_caption = CUSTOM_FILE_CAPTION.format(
                    file_name='' if title is None else title,
                    file_size='' if size is None else size,
                    file_caption='' if f_caption is None else f_caption,
                )
            except Exception as e:
                logger.exception(e)

        if f_caption is None:
            f_caption = f"{title}"
        if len(f_caption) > 1024:
            f_caption = f_caption[:1021] + "..."

        if f_type == 'photo':
            results.append(
                InlineQueryResultCachedPhoto(
                    photo_file_id=send_id,
                    title=title,
                    description=f"🎬 {title}"[:100],
                    caption=f_caption,
                    parse_mode=enums.ParseMode.HTML,
                    reply_markup=reply_markup,
                )
            )
        else:
            results.append(
                InlineQueryResultCachedDocument(
                    title=title,
                    document_file_id=send_id,
                    caption=f_caption,
                    parse_mode=enums.ParseMode.HTML,
                    description=f"Size: {size} | Type: {f_type}",
                    reply_markup=reply_markup,
                )
            )

    if results:
        switch_pm_text = f"🎬 Results ({search_time:.2f}s)"
        if string:
            switch_pm_text = f"🎬 {string} • {search_time:.2f}s"
        switch_pm_text = switch_pm_text[:64]
        try:
            await query.answer(
                results=results,
                is_personal=True,
                cache_time=cache_time,
                switch_pm_text=switch_pm_text,
                switch_pm_parameter="start",
                next_offset=str(next_offset),
            )
        except QueryIdInvalid:
            pass
        except Exception as e:
            logger.exception(str(e))
    else:
        switch_pm_text = "❌ ဇာတ်ကား ရှာမတွေ့ပါ"
        if string:
            switch_pm_text = f'❌ ရှာမတွေ့ပါ: "{string}"'
        switch_pm_text = switch_pm_text[:64]

        await query.answer(
            results=[],
            is_personal=True,
            cache_time=cache_time,
            switch_pm_text=switch_pm_text,
            switch_pm_parameter="okay",
        )


def get_reply_markup(query):
    buttons = [
        [
            InlineKeyboardButton('🔍 ထပ်မံရှာဖွေရန်', switch_inline_query_current_chat=query),
            InlineKeyboardButton('📢 MZP Channels', url=ADDLIST_URL),
        ]
    ]
    return InlineKeyboardMarkup(buttons)
