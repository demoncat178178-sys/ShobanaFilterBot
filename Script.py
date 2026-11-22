class script(object):
    START_TXT = """👋 မင်္ဂလာပါ {}!

🎬 <b>MZP Entertainment Bot</b> မှ ကြိုဆိုပါတယ်။
ဒီ Bot ထဲမှာ ဇာတ်ကားနာမည် ရိုက်ထည့်ပြီး အလွယ်တကူ ရှာဖွေကြည့်ရှုနိုင်ပါတယ်။

📢 ဇာတ်ကားအသစ်တွေ အမြဲကြည့်ရှုဖို့ အောက်က <b>Join Our Channels</b> ခလုတ်ကို နှိပ်ပြီး Join ထားပေးပါနော်။"""

    HELP_TXT = """<b>👋 မင်္ဂလာပါ {}</b>

Bot အသုံးပြုနည်းနဲ့ Command များကို အောက်ပါခလုတ်များနှိပ်ပြီး ကြည့်ရှုနိုင်ပါတယ်။"""

    HELP_PAGES = [
"""<b>📘 Help (1/6): အဓိကလုပ်ဆောင်ချက်များ</b>
• ဇာတ်ကားနာမည် ရိုက်ထည့်ရုံဖြင့် အလိုအလျောက် ရှာဖွေပေးခြင်း
• IMDB အချက်အလက်နှင့် Poster ကြည့်ရှုနိုင်ခြင်း
• စာလုံးပေါင်းမှားလျှင် အလိုအလျောက် ပြန်ညွှန်းပေးခြင်း
• Channel များမှ ဇာတ်ကားဖိုင်များ အလိုအလျောက် Index လုပ်ပေးခြင်း
• Group နှင့် PM နှစ်မျိုးလုံးတွင် အသုံးပြုနိုင်ခြင်း""",
"""<b>📘 Help (2/6): အသုံးများသော Command များ</b>
• /start - Bot စတင်အသုံးပြုရန်
• /movies - နောက်ဆုံးတင်ထားသော ရုပ်ရှင်များ
• /series - နောက်ဆုံးတင်ထားသော ဇာတ်လမ်းတွဲများ
• /connect - Group ကို PM နှင့် ချိတ်ဆက်ရန်
• /disconnect - ချိတ်ဆက်မှု ဖြုတ်ရန်
• /connections - ချိတ်ဆက်ထားသော Group များကြည့်ရန်
• /settings - Group Settings ဖွင့်ရန်
• /filter or /add - Manual Filter ထည့်ရန်
• /filters - Filter စာရင်းကြည့်ရန်
• /del and /delall - Filter ဖျက်ရန်""",
"""<b>📘 Help (3/6): အထောက်အကူပြု Command များ</b>
• /imdb - ဇာတ်ကားအချက်အလက် ရှာရန်
• /id - User / Chat ID ကြည့်ရန်
• /info - User အချက်အလက် ကြည့်ရန်
• /bug or /feedback - အကြံပြုချက် / Error ပို့ရန်
• /tr - စာသားဘာသာပြန်ရန်
• /font - စာလုံးဒီဇိုင်းပြောင်းရန်""",
"""<b>📘 Help (4/6): Media / Extra Commands</b>
• /tts - Text to Speech
• /stickerid - Sticker File ID ယူရန်
• /json - Message JSON ကြည့်ရန်
• /share - စာသား Share Link လုပ်ရန်
• /pin - Message Pin လုပ်ရန်
• /unpin - Pin ဖြုတ်ရန်
• /unpin_all - Pin အားလုံးဖြုတ်ရန်""",
"""<b>📘 Help (5/6): Group / Admin Commands</b>
• /promote - Admin ခန့်ရန်
• /demote - Admin ဖြုတ်ရန်
• /stats - Bot Database အခြေအနေကြည့်ရန်
• /invite - Group Invite Link ထုတ်ရန်
• /ban - User ကို Ban ရန်
• /unban - Ban ပြန်ဖြုတ်ရန်
• /leave - Group မှ ထွက်ရန်
• /disable - Chat ပိတ်ရန်
• /enable - Chat ပြန်ဖွင့်ရန်
• /deletefiles & /deleteall - ဖိုင်များအစုလိုက်ဖျက်ရန်""",
"""<b>📘 Help (6/6): Owner / Admin-Only</b>
• /users - Bot အသုံးပြုသူစာရင်း
• /chats - ချိတ်ဆက်ထားသော Group စာရင်း
• /channel - Index လုပ်ထားသော Channel စာရင်း
• /broadcast - User အားလုံးထံ စာပို့ရန်
• /grpbroadcast - Group အားလုံးထံ စာပို့ရန်
• /logs - Bot Log ဖိုင်ယူရန်
• /delete - ဖိုင်တစ်ခုချင်းဖျက်ရန်
• /fsub - Force-Sub Channel ပြင်ရန်
• /restart, /ping, /usage - System Tools"""
    ]

    ABOUT_TXT = """<b>🎬 Bot Name: MZP Entertainment
📢 Channels: <a href="https://t.me/addlist/ueNwQploRbQ1MGM1">MZP Channels</a>
💻 Language: Python 3
🗄️ Database: MongoDB
☁️ Server: Render</b>"""

    SOURCE_TXT = """<b>🎬 MZP Entertainment Bot</b>

ဇာတ်ကားအစုံအလင်ကို တစ်နေရာတည်းမှာ အလွယ်တကူ ရှာဖွေကြည့်ရှုနိုင်ဖို့ ပြုလုပ်ထားတဲ့ Bot ဖြစ်ပါတယ်။

📢 <b>Our Channels:</b> <a href="https://t.me/addlist/ueNwQploRbQ1MGM1">Join MZP Channels</a>"""

    MANUELFILTER_TXT = """Help: <b>Filters</b>
- သတ်မှတ်ထားသော စကားလုံးရိုက်ထည့်လျှင် အလိုအလျောက် ပြန်ဖြေပေးမည့်စနစ် ဖြစ်ပါသည်။

<b>NOTE:</b>
1. Bot ကို Group Admin ပေးထားရန် လိုအပ်ပါသည်။
2. Admin များသာ Filter ထည့်သွင်းနိုင်ပါသည်။

<b>Commands and Usage:</b>
• /filter - <code>Filter အသစ်ထည့်ရန်</code>
• /filters - <code>Filter စာရင်းကြည့်ရန်</code>
• /del - <code>Filter တစ်ခုဖျက်ရန်</code>
• /delall - <code>Filter အားလုံးဖျက်ရန်</code>"""

    BUTTON_TXT = """Help: <b>Buttons</b>

- URL Button နှင့် Alert Inline Button နှစ်မျိုးလုံး အသုံးပြုနိုင်ပါသည်။

<b>URL buttons:</b>
<code>[Button Text](buttonurl:https://t.me/addlist/ueNwQploRbQ1MGM1)</code>

<b>Alert buttons:</b>
<code>[Button Text](buttonalert:This is an alert message)</code>"""

    AUTOFILTER_TXT = """<b>📌 File Index လုပ်နည်း</b>
1. Bot ကို Channel ထဲတွင် Admin အဖြစ် ထည့်သွင်းပါ။
2. Channel ထဲမှ နောက်ဆုံးပို့စ်ကို Bot ဆီ Forward ပို့ပြီး Index လုပ်နိုင်ပါသည်။

<b>📌 AutoFilter ဖွင့်နည်း</b>
1. Bot ကို Group ထဲတွင် Admin ထည့်ပါ။
2. /connect ဖြင့် Group ကို ချိတ်ဆက်ပါ။
3. /settings ဖြင့် AutoFilter Settings များ ပြင်ဆင်နိုင်ပါသည်။"""

    CONNECTION_TXT = """Help: <b>Connections</b>

- Group Settings များကို Bot PM မှတစ်ဆင့် ထိန်းချုပ်နိုင်ရန် ချိတ်ဆက်ပေးသည့်စနစ် ဖြစ်ပါသည်။

<b>Commands and Usage:</b>
• /connect - <code>Group ကို PM နှင့် ချိတ်ဆက်ရန်</code>
• /disconnect - <code>ချိတ်ဆက်မှု ဖြုတ်ရန်</code>
• /connections - <code>ချိတ်ဆက်ထားသော Group များကြည့်ရန်</code>"""

    EXTRAMOD_TXT = """Help: <b>Extra Modules</b>

<b>MZP Entertainment Bot</b> ၏ အပိုလုပ်ဆောင်ချက်များ-

<b>Commands and Usage:</b>
• /id - <code>User / Chat ID ကြည့်ရန်</code>
• /info - <code>User အချက်အလက်ကြည့်ရန်</code>
• /imdb - <code>IMDb မှ ဇာတ်ကားအချက်အလက်ရှာရန်</code>
• /start - <code>Bot အလုပ်လုပ်မလုပ် စစ်ရန်</code>
• /ping - <code>Bot မြန်နှုန်းစစ်ရန်</code>
• /usage - <code>Bot အသုံးပြုမှုအခြေအနေ</code>
• /broadcast - <code>Broadcast ပို့ရန် (Owner only)</code>"""

    ADMIN_TXT = """Help: <b>Admin Mods</b>

<b>NOTE:</b> Bot Admin များအတွက်သာ အသုံးပြုနိုင်ပါသည်။

<b>Commands and Usage:</b>
• /logs - <code>Error log ဖိုင်ယူရန်</code>
• /stats - <code>Database အခြေအနေကြည့်ရန်</code>
• /delete - <code>ဖိုင်တစ်ခုဖျက်ရန်</code>
• /users - <code>User စာရင်းကြည့်ရန်</code>
• /chats - <code>Group စာရင်းကြည့်ရန်</code>
• /leave - <code>Group မှထွက်ရန်</code>
• /disable - <code>Chat ပိတ်ရန်</code>
• /ban - <code>User Ban ရန်</code>
• /unban - <code>User Unban ရန်</code>
• /channel - <code>Index Channel စာရင်းကြည့်ရန်</code>
• /broadcast - <code>User အားလုံးထံ စာပို့ရန်</code>"""

    STATUS_TXT = """★ <b>TOTAL FILES:</b> <code>{}</code>
★ <b>TOTAL USERS:</b> <code>{}</code>
★ <b>TOTAL CHATS:</b> <code>{}</code>
★ <b>USED STORAGE:</b> <code>{}</code>
★ <b>FREE STORAGE:</b> <code>{}</code>"""

    LOG_TEXT_G = """#NewGroup
Group = {} (<code>{}</code>)
Total Members = <code>{}</code>
Added By - {}"""

    RESULT_TXT = """🎬 မင်္ဂလာပါ {mention}
ရှာဖွေထားသော ဇာတ်ကားများကို အောက်တွင် ရွေးချယ်ကြည့်ရှုပါ 👇"""

    CUSTOM_FILE_CAPTION = """🎬 <b>Title:</b> <code>{file_name}</code>
📦 <b>Size:</b> {file_size}

📢 <b>ဇာတ်ကားအစုံကြည့်ရန်:</b> <a href="https://t.me/addlist/ueNwQploRbQ1MGM1">MZP Entertainment Channels</a>"""

    RESTART_GC_TXT = """<b>✅ Bot Restarted!</b>

📅 Date: <code>{}</code>
⏰ Time: <code>{}</code>
🛠️ Status: <code>Online [Stable]</code>"""

    LOG_TEXT_P = """#NewUser
ID - <code>{}</code>
Name - {}"""

    SPOLL_NOT_FND = """❌ ရှာဖွေသော ဇာတ်ကားကို မတွေ့ရှိပါ။
အောက်ပါအချက်များကို စစ်ဆေးပြီး ပြန်လည်ရှာဖွေကြည့်ပါ 👇
<blockquote>
1️⃣ ဇာတ်ကားနာမည် စာလုံးပေါင်း မှန်ကန်စွာ ရိုက်ထည့်ပါ။
2️⃣ ဇာတ်ကားနာမည် တိုတိုတုတ်တုတ် (သို့) ခုနှစ်တွဲပြီး ရှာကြည့်ပါ (ဥပမာ - Steps 2026)။
3️⃣ ဇာတ်ကားမရှိသေးပါက Admin ထံ /bugs ဖြင့် တောင်းဆိုနိုင်ပါသည်။
</blockquote>"""

    ENG_SPELL = """📓 ဇာတ်ကားရှာဖွေရာတွင် သတိပြုရန်
1️⃣ စာလုံးပေါင်း မှန်ကန်စွာ ရိုက်ထည့်ပါ။
2️⃣ ဇာတ်ကားနာမည် (သို့) ခုနှစ်တွဲပြီး ရှာကြည့်ပါ။
3️⃣ မရှိသေးပါက /bugs ဖြင့် Admin ထံ အကြောင်းကြားနိုင်ပါသည်။"""

    MAL_SPELL = ENG_SPELL
    HIN_SPELL = ENG_SPELL
    TAM_SPELL = ENG_SPELL

    CHK_MOV_ALRT = """♻️ Database ထဲတွင် ဇာတ်ကားရှာဖွေနေပါသည်... ♻️"""

    OLD_MES = """⚠️ Message အဟောင်း ဖြစ်နေပါပြီ။ ဇာတ်ကားနာမည်ကို အသစ်ပြန်ရိုက်ရှာပေးပါ။"""

    MOV_NT_FND = """<b>❌ ဒီဇာတ်ကားကို Database ထဲမှာ မတင်ရသေးပါ။</b>
<pre>Admin ထံ တောင်းဆိုရန် /bugs command ကို အသုံးပြုပါ</pre>"""

    RESTART_TXT = """<b><u>✅ Bot Restarted</u></b>"""
