
import html
import re
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.errors import MessageNotModified
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from database.ia_filterdb import get_movie_list, get_series_grouped

PAGE_SIZE = 10
MOVIE_CACHE = {}
SERIES_CACHE = {}
ADDLIST_URL = "https://t.me/addlist/ueNwQploRbQ1MGM1"
LANGS = {
    "mm": "Myanmar Sub",
    "mmsub": "Myanmar Sub",
    "eng": "English",
    "chi": "Chinese",
    "kor": "Korean",
    "jpn": "Japanese",
    "tha": "Thai",
}


def cleaned_movie_title(name: str) -> str:
    clean = re.sub(r"[._]+", " ", name or "")
    clean = re.sub(
        r"\b(2160p|1080p|720p|480p|x264|x265|hevc|webrip|hdrip|web-dl|blu ?ray|aac|esub|mkv|mp4)\b",
        "",
        clean,
        flags=re.I,
    )
    clean = re.sub(r"\s+", " ", clean).strip(" -._")
    year = re.search(r"\b(19\d{2}|20\d{2})\b", clean)
    if year:
        before_year = re.split(rf"\b{year.group(1)}\b", clean, maxsplit=1)[0].strip(" -._()")
        if before_year:
            return f"{before_year} ({year.group(1)})"
    return clean


def extract_lang_quality(raw: str):
    low = (raw or "").lower()
    langs = sorted({v for k, v in LANGS.items() if re.search(rf"\b{k}\b", low)})
    q = re.search(r"\b(2160p|4k|1080p|720p|480p|hq|hd)\b", low)
    return langs, (q.group(1).upper() if q else None)


def build_page(items, page, head, kind):
    total_pages = max(1, -(-len(items) // PAGE_SIZE))
    start = page * PAGE_SIZE
    chunk = items[start : start + PAGE_SIZE]
    text = f"<b>{head}</b>  <i>({page + 1}/{total_pages})</i>\n\n" + "\n".join(chunk)

    buttons = []
    row = []
    if page > 0:
        row.append(InlineKeyboardButton("◀️ Prev", callback_data=f"{kind}_pg#{page - 1}"))
    if start + PAGE_SIZE < len(items):
        row.append(InlineKeyboardButton("Next ▶️", callback_data=f"{kind}_pg#{page + 1}"))
    if row:
        buttons.append(row)
    buttons.append([InlineKeyboardButton("📢 MZP Entertainment Channels", url=ADDLIST_URL)])
    return text, InlineKeyboardMarkup(buttons)


@Client.on_message(filters.private & filters.command("movies"))
async def list_movies(bot: Client, message: Message):
    movies = await get_movie_list(limit=120)
    if not movies:
        return await message.reply("❌ လတ်တလော တင်ထားသော ဇာတ်ကားများ မရှိသေးပါ။")

    grouped = {}
    for raw in movies:
        if not raw:
            continue
        low = raw.lower()
        if re.search(r"\b(episode|ep\s*\d+|e\d{1,3}|s\d{1,2}|season\s*\d+)\b", low):
            continue
        title = cleaned_movie_title(raw)
        if not title:
            continue
        langs, quality = extract_lang_quality(raw)
        data = grouped.setdefault(title, {"langs": set(), "qualities": set()})
        data["langs"].update(langs)
        if quality:
            data["qualities"].add(quality)

    lines = []
    for title, data in grouped.items():
        ln = f"🎬 <b>{html.escape(title)}</b>"
        extras = []
        if data["langs"]:
            extras.append(", ".join(sorted(data["langs"])))
        if data["qualities"]:
            extras.append(", ".join(sorted(data["qualities"])))
        if extras:
            ln += f" — {' | '.join(extras)}"
        lines.append(ln)

    if not lines:
        return await message.reply("❌ လတ်တလော တင်ထားသော ဇာတ်ကားများ မရှိသေးပါ။")

    MOVIE_CACHE[message.from_user.id] = lines
    text, markup = build_page(lines, 0, "🎬 နောက်ဆုံးတင်ထားသော ဇာတ်ကားများ", "mv")
    await message.reply(text[:4096], parse_mode=ParseMode.HTML, reply_markup=markup)


@Client.on_message(filters.private & filters.command("series"))
async def list_series(bot: Client, message: Message):
    series_data = await get_series_grouped(limit=80)
    if not series_data:
        return await message.reply("❌ လတ်တလော တင်ထားသော ဇာတ်လမ်းတွဲများ မရှိသေးပါ။")

    lines = [
        f"📺 <b>{html.escape(title)}</b> — Ep {', '.join(f'{e:02d}' for e in episodes)}"
        for title, episodes in series_data.items()
    ]
    SERIES_CACHE[message.from_user.id] = lines
    text, markup = build_page(lines, 0, "📺 နောက်ဆုံးတင်ထားသော ဇာတ်လမ်းတွဲများ", "sr")
    await message.reply(text[:4096], parse_mode=ParseMode.HTML, reply_markup=markup)


@Client.on_callback_query(filters.regex(r"^(mv|sr)_pg#"))
async def movies_series_pages(bot: Client, query: CallbackQuery):
    kind, page = query.data.split("#")
    page = int(page)
    items = MOVIE_CACHE.get(query.from_user.id, []) if kind == "mv_pg" else SERIES_CACHE.get(query.from_user.id, [])
    if not items:
        return await query.answer("စာရင်းသက်တမ်းကုန်သွားပါပြီ။ /movies သို့ /series ပြန်ရိုက်ပေးပါ။", show_alert=True)

    head = "🎬 နောက်ဆုံးတင်ထားသော ဇာတ်ကားများ" if kind == "mv_pg" else "📺 နောက်ဆုံးတင်ထားသော ဇာတ်လမ်းတွဲများ"
    prefix = "mv" if kind == "mv_pg" else "sr"
    text, markup = build_page(items, page, head, prefix)
    try:
        await query.message.edit_text(text[:4096], parse_mode=ParseMode.HTML, reply_markup=markup)
    except MessageNotModified:
        pass
    await query.answer()
