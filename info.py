import re
from os import environ
from Script import script
from time import time

id_pattern = re.compile(r'^.\d+$')
def is_enabled(value, default): return True if str(value).lower() in ["true", "yes", "1", "enable", "y"] else (False if str(value).lower() in ["false", "no", "0", "disable", "n"] else default)
def parse_size_to_bytes(value, default=0): return int(float(m.group(1)) * {"": 1, "k": 1024, "m": 1024**2, "g": 1024**3, "t": 1024**4, "p": 1024**5}.get((m.group(2) or "b").rstrip("b"), 1)) if (value is not None and (m := re.fullmatch(r"(\d+(?:\.\d+)?)\s*([kmgtp]?b?)?", str(value).strip().lower()))) else default

SESSION = environ.get('SESSION', 'Media_search')
API_ID = int(environ.get('API_ID', '0'))
API_HASH = environ.get('API_HASH', '')
BOT_TOKEN = environ.get('BOT_TOKEN', '')

KEEP_ALIVE_URL = environ.get("KEEP_ALIVE_URL", "https://mzpentertainmentbot.onrender.com/")
HYPER_MODE = is_enabled(environ.get('HYPER_MODE', 'False'), False)
REQUEST_FSUB_MODE = is_enabled(environ.get('REQUEST_FSUB_MODE', 'True'), True)

BOT_START_TIME = time()
CACHE_TIME = int(environ.get('CACHE_TIME', 300))
USE_CAPTION_FILTER = is_enabled(environ.get('USE_CAPTION_FILTER', 'True'), True)
PICS = (environ.get('PICS', 'https://graph.org/file/2ed90a79eb533d86f8a0f.jpg')).split()

ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', '').split()]
CHANNELS = [int(ch) if id_pattern.search(ch) else ch for ch in environ.get('CHANNELS', '').split()]
auth_users = [int(user) if id_pattern.search(user) else user for user in environ.get('AUTH_USERS', '').split()]
AUTH_USERS = (auth_users + ADMINS) if auth_users else []
auth_grp = environ.get('AUTH_GROUP')
DEFAULT_AUTH_CHANNELS = [int(x) for x in environ.get("AUTH_CHANNEL", "").split() if x.lstrip('-').isdigit()]
AUTH_GROUPS = [int(ch) for ch in auth_grp.split()] if auth_grp else None

DATABASE_URI = environ.get('DATABASE_URI', "")
DATABASE_NAME = environ.get('DATABASE_NAME', "Cluster0")
COLLECTION_NAME = environ.get('COLLECTION_NAME', 'mn_files')
DATABASE_URI2 = environ.get('DATABASE_URI2', "")
DATABASE_URI3 = environ.get('DATABASE_URI3', "")
DATABASE_URI4 = environ.get('DATABASE_URI4', "")
DATABASE_URI5 = environ.get('DATABASE_URI5', "")
DATABASE_NAME2 = environ.get('DATABASE_NAME2', DATABASE_NAME)
DATABASE_NAME3 = environ.get('DATABASE_NAME3', DATABASE_NAME)
DATABASE_NAME4 = environ.get('DATABASE_NAME4', DATABASE_NAME)
DATABASE_NAME5 = environ.get('DATABASE_NAME5', DATABASE_NAME)
POSTGRES_URI = environ.get('POSTGRES_URI', '')
POSTGRES_STORAGE_LIMIT_BYTES = parse_size_to_bytes(environ.get('POSTGRES_STORAGE_LIMIT_BYTES', '1GB'), 0)

FILE_CHANNELS = [int(ch) for ch in environ.get('FILE_CHANNELS', '').split() if ch.lstrip('-').isdigit()]
FILE_CHANNEL_SENDING_MODE = is_enabled(environ.get('FILE_CHANNEL_SENDING_MODE', 'False'), False)
FILE_AUTO_DELETE_SECONDS = int(environ.get('FILE_AUTO_DELETE_SECONDS', 600))

PM_SEARCH_GROUP_LINK = environ.get('PM_SEARCH_GROUP_LINK', 'https://t.me/addlist/ueNwQploRbQ1MGM1')
PM_SEARCH_REDIRECT_TEXT = environ.get('PM_SEARCH_REDIRECT_TEXT', '🎬 ဇာတ်ကားရှာဖွေရန် အောက်ပါ Group ထဲတွင် ဇာတ်ကားနာမည် ရိုက်ထည့်ရှာဖွေပါ။\n\n👇 Group သို့ဝင်ရန်\n{group_link}')
DELETE_USER_SEARCH_MESSAGE = is_enabled(environ.get('DELETE_USER_SEARCH_MESSAGE', 'False'), False)

LOG_CHANNEL = int(environ.get('LOG_CHANNEL', '0'))
SUPPORT_CHAT = environ.get('SUPPORT_CHAT', '')
P_TTI_SHOW_OFF = is_enabled((environ.get('P_TTI_SHOW_OFF', 'False')), False)
IMDB = is_enabled((environ.get('IMDB', 'False')), False)
SINGLE_BUTTON = is_enabled((environ.get('SINGLE_BUTTON', 'True')), True)
CUSTOM_FILE_CAPTION = environ.get("CUSTOM_FILE_CAPTION", "🎬 <b>Title:</b> <code>{file_name}</code>\n📦 <b>Size:</b> {file_size}\n\n📢 <b>ဇာတ်ကားအစုံကြည့်ရန်:</b> <a href='https://t.me/addlist/ueNwQploRbQ1MGM1'>MZP Entertainment Channels</a>")
BATCH_FILE_CAPTION = environ.get("BATCH_FILE_CAPTION", "📂 <em>File Name</em>: <code>{file_name}</code>\n\n♻ <em>File Size</em>: {file_size}")
IMDB_TEMPLATE = environ.get("IMDB_TEMPLATE", "🏷 𝖳𝗂𝗍𝗅𝖾: <a href={url}>{title}</a> \n🔮 𝖸𝖾𝖺𝗋: {year} \n⭐️ 𝖱𝖺𝗍𝗂𝗇𝗀𝗌: {rating}/ 10 \n🎭 𝖦𝖾𝗇𝖾𝗋𝗌: {genres}")
LONG_IMDB_DESCRIPTION = is_enabled(environ.get("LONG_IMDB_DESCRIPTION", "False"), False)
SPELL_CHECK_REPLY = is_enabled(environ.get("SPELL_CHECK_REPLY", "True"), True)
MAX_LIST_ELM = environ.get("MAX_LIST_ELM", None)
INDEX_REQ_CHANNEL = int(environ.get('INDEX_REQ_CHANNEL', LOG_CHANNEL))
FILE_STORE_CHANNEL = [int(ch) for ch in (environ.get('FILE_STORE_CHANNEL', '')).split() if ch.lstrip('-').isdigit()]
MELCOW_NEW_USERS = is_enabled((environ.get('MELCOW_NEW_USERS', "True")), True)
PROTECT_CONTENT = is_enabled((environ.get('PROTECT_CONTENT', "False")), False)
PUBLIC_FILE_STORE = is_enabled((environ.get('PUBLIC_FILE_STORE', "False")), True)

LOG_STR = "Current Customized Configurations are:-\n"
