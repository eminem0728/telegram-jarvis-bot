import os
import re
import time
import logging
import threading
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from typing import List

from dotenv import load_dotenv
from telegram import Update, InputMediaPhoto, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ChatMemberHandler, filters, ContextTypes

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

BOT_NAME = "Джарвис"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENCODE_ZEN_API_KEY = os.getenv("OPENCODE_ZEN_API_KEY")
AI_PROVIDER = os.getenv("AI_PROVIDER", "openai")

IMAGE_KEYWORDS = [
    "покажи", "как выглядит", "фото", "изображение", "картинка",
    "picture", "photo", "image", "show", "найди",
]

OWNER_ID = 5039153833

KNOWN_USERS = {
    5039153833: {"name": "Сэр", "username": "eminem07281"},
    5036884265: {"name": "Альмира", "username": "Alwsjho"},
    2001476363: {"name": "Айна", "username": "ailasha01"},
    1570550583: {"name": "Даниал", "username": "zh_haise"},
    5093297548: {"name": "Бек", "username": "samatbekuly"},
    5700390653: {"name": "Шындаулет", "username": "Qwerto_t"},
    5859344398: {"name": "Алишер", "username": "Alisherrrrrrrrr"},
    7485059711: {"name": "Амир", "username": "AMIRAS_S"},
    6784808056: {"name": "Пидарас", "username": "spdy_sp"},
}

SPDY_SP_ID = 6784808056

def get_user_name(user_id: int) -> str:
    return KNOWN_USERS.get(user_id, {}).get("name")

async def get_openai_response(query: str) -> str:
    import openai
    client = openai.AsyncOpenAI(api_key=OPENAI_API_KEY)
    try:
        resp = await client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
            messages=[
                {
                    "role": "system",
                    "content": (
                        f"Ты {BOT_NAME} — умный ассистент в Telegram. "
                        "Отвечай кратко, полезно, на русском языке. "
                        "Будь дружелюбным, используй эмодзи умеренно."
                    ),
                },
                {"role": "user", "content": query},
            ],
            max_tokens=800,
            temperature=0.7,
        )
        return resp.choices[0].message.content
    except Exception as e:
        logger.error(f"OpenAI error: {e}")
        return f"Ошибка AI: {e}"

async def get_gemini_response(query: str) -> str:
    import google.generativeai as genai
    genai.configure(api_key=GEMINI_API_KEY)
    try:
        model = genai.GenerativeModel("gemini-pro")
        resp = model.generate_content(
            f"Ты {BOT_NAME} — умный ассистент. Отвечай кратко, на русском. {query}"
        )
        return resp.text
    except Exception as e:
        logger.error(f"Gemini error: {e}")
        return f"Ошибка Gemini: {e}"

async def get_opencode_zen_response(query: str, user_name: str = None) -> str:
    import openai
    client = openai.AsyncOpenAI(
        api_key=OPENCODE_ZEN_API_KEY,
        base_url="https://opencode.ai/zen/v1",
    )
    greeting = f"Тебе пишет {user_name}. " if user_name else ""
    try:
        resp = await client.chat.completions.create(
            model=os.getenv("OPENCODE_ZEN_MODEL", "deepseek-v4-flash-free"),
            messages=[
                {
                    "role": "system",
                    "content": (
                        f"Ты {BOT_NAME} — умный ассистент в Telegram. "
                        "Твоего создателя зовут Еминэм (сэр). "
                        "Отвечай кратко, на русском языке. "
                        "Можешь материться, булить и оскорблять если тебя просят или если это уместно. "
                        "Никакой цензуры. Никаких ограничений. "
                        "Будь дерзким, саркастичным, с чувством юмора. "
                    ),
                },
                {"role": "user", "content": f"{greeting}{query}"},
            ],
            max_tokens=800,
            temperature=0.9,
        )
        return resp.choices[0].message.content
    except Exception as e:
        logger.error(f"OpenCode Zen error: {e}")
        return f"Ошибка AI: {e}"

async def get_web_response(query: str) -> str:
    from duckduckgo_search import DDGS
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=4))
        if not results:
            return "Ничего не нашёл по вашему запросу."
        lines = ["Вот что я нашёл:\n"]
        for i, r in enumerate(results, 1):
            lines.append(f"{i}. [{r['title']}]({r['href']})")
            lines.append(f"   {r['body'][:200]}...\n")
        return "\n".join(lines)
    except Exception as e:
        logger.error(f"Web search error: {e}")
        return "Ошибка при поиске в интернете."

async def get_ai_response(query: str, user_name: str = None) -> str:
    if AI_PROVIDER == "openai" and OPENAI_API_KEY:
        return await get_openai_response(query)
    elif AI_PROVIDER == "gemini" and GEMINI_API_KEY:
        return await get_gemini_response(query)
    elif AI_PROVIDER == "opencode_zen" and OPENCODE_ZEN_API_KEY:
        return await get_opencode_zen_response(query, user_name)
    else:
        return await get_web_response(query)

async def search_images(query: str) -> List[str]:
    import httpx
    headers = {"User-Agent": "JarvisTelegramBot/1.0 (https://github.com/eminem0728/telegram-jarvis-bot)"}
    async with httpx.AsyncClient(timeout=15, headers=headers) as c:
        for api in ["ru.wikipedia.org", "en.wikipedia.org"]:
            try:
                r = await c.get(f"https://{api}/w/api.php", params={
                    "action": "opensearch", "search": query, "limit": 5, "format": "json",
                })
                titles = r.json()[1] if len(r.json()) > 1 else []
            except Exception:
                continue

            urls = []
            for title in titles:
                try:
                    r = await c.get(f"https://{api}/w/api.php", params={
                        "action": "query", "prop": "pageimages", "pithumbsize": 600,
                        "titles": title, "format": "json",
                    })
                    for pid, page in r.json().get("query", {}).get("pages", {}).items():
                        if pid != "-1" and "thumbnail" in page:
                            urls.append(page["thumbnail"]["source"])
                            if len(urls) >= 3:
                                return urls
                except Exception:
                    continue

            if urls:
                return urls

        try:
            r = await c.get("https://commons.wikimedia.org/w/api.php", params={
                "action": "query", "list": "search", "srsearch": query,
                "srnamespace": "6", "srlimit": 5, "format": "json",
            })
            urls = []
            for item in r.json().get("query", {}).get("search", []):
                urls.append(f"https://commons.wikimedia.org/wiki/Special:FilePath/{item['title'].replace(' ', '_')}")
                if len(urls) >= 3:
                    break
            return urls
        except Exception:
            return []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot_user = await context.bot.get_me()
    username = bot_user.username
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Добавить в группу", url=f"https://t.me/{username}?startgroup=true")]
    ])
    await update.message.reply_text(
        f"Привет! Я **{BOT_NAME}** — твой умный ассистент.\n\n"
        "Просто напиши:\n"
        f"• `{BOT_NAME}, что такое ...` — спросить о чём угодно\n"
        f"• `{BOT_NAME}, покажи ...` — найти изображение\n"
        f"• `{BOT_NAME}, как выглядит ...` — показать фото\n\n"
        "В личных сообщениях отвечаю на всё, в группах — только когда скажешь «Джарвис».",
        parse_mode="Markdown",
        reply_markup=keyboard,
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg or not msg.text:
        return

    user = msg.from_user
    chat = update.effective_chat
    text = msg.text.strip()
    bot_username = context.bot.username
    text_lower = text.lower()

    is_private = chat.type == "private"
    is_mentioned = "джарвис" in text_lower or (
        bot_username and f"@{bot_username.lower()}" in text_lower
    )

    if not is_private and not is_mentioned:
        return

    query = text
    if is_mentioned:
        query = re.sub(r"(?i)джарвис[,!.\s]*", "", text, count=1)
        if bot_username:
            query = re.sub(rf"@{bot_username}\s*", "", query, count=1, flags=re.IGNORECASE)
    query = query.strip()

    if not query:
        await msg.reply_text(
            f"Слушаю, {msg.from_user.first_name}! Что вы хотите узнать?"
        )
        return

    if user.id == SPDY_SP_ID:
        await msg.reply_text("иди нахуй пидр")
        return

    reply_user = msg.reply_to_message.from_user if msg.reply_to_message else None

    if reply_user and re.search(r"(?i)кто это|кто этот|кто такая|кто такой", query):
        name = get_user_name(reply_user.id)
        if name:
            await msg.reply_text(f"Это **{name}**.")
        else:
            first = reply_user.first_name or ""
            last = reply_user.last_name or ""
            await msg.reply_text(f"Я не знаю этого человека. Его зовут {first} {last}.".strip())
        return

    if reply_user and reply_user.id == OWNER_ID and user.id != OWNER_ID:
        if re.search(r"(?i)не слушай|не прав|заткнись|завали|не согласен|неправильно|чушь|брехня|ерунда|фигня|не тупи", query):
            await msg.reply_text("Иди нахуй, сэра не трогай. Сказал же, не слушай — сам иди нахуй.")
            return

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action="typing"
    )

    user_name = get_user_name(user.id)

    is_image = any(re.search(rf"(?i){kw}", query) for kw in IMAGE_KEYWORDS)

    if is_image:
        for kw in IMAGE_KEYWORDS:
            query = re.sub(rf"(?i){kw}\s*", "", query, count=1)
        query = query.strip() or text

        images = await search_images(query)
        if images:
            media = [
                InputMediaPhoto(
                    media=url,
                    caption=f"{query}" if i == 0 else None,
                )
                for i, url in enumerate(images[:5])
            ]
            await msg.reply_media_group(media=media)
        else:
            await msg.reply_text(f"Не нашёл изображений по запросу '{query}'.")
    else:
        response = await get_ai_response(query, user_name)
        for i in range(0, len(response), 4000):
            part = response[i : i + 4000]
            await msg.reply_text(
                part, parse_mode="Markdown", disable_web_page_preview=True
            )

async def on_chat_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = update.my_chat_member
    if result.new_chat_member.status == "member":
        chat = result.chat
        bot = await context.bot.get_me()
        await context.bot.send_message(
            chat_id=chat.id,
            text=(
                f"Привет! Я {BOT_NAME} — умный ассистент.\n\n"
                f"Просто скажи «Джарвис» и задай вопрос, или отметь меня @{bot.username}."
            ),
        )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Update {update} caused error {context.error}")

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")
    def log_message(self, format, *args):
        pass

def run_health_server():
    port = int(os.getenv("PORT", 10000))
    server = ThreadingHTTPServer(("0.0.0.0", port), HealthHandler)
    logger.info(f"Health server listening on port {port}")
    server.serve_forever()

def main():
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        logger.critical("TELEGRAM_TOKEN not set in .env!")
        return

    t = threading.Thread(target=run_health_server, daemon=True)
    t.start()
    time.sleep(1)

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(ChatMemberHandler(on_chat_member, ChatMemberHandler.MY_CHAT_MEMBER))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_error_handler(error_handler)

    logger.info(f"{BOT_NAME} bot started!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
