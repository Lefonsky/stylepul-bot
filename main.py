import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import BaseFilter
from aiogram import Router

API_TOKEN = "7514927244:AAHY3z5PgbCWOj7L0u8M43HFtT6ovZKGetE"
TARGET_CHANNEL = "@stylepul"
SOURCE_CHANNELS = [
    "@fashionverge", "@clothona_news", "@fashionhub", "@styleinspo", "@trend_alerts",
    "@luxuryfashion", "@streetstyle_daily", "@fashionmagazine", "@moda_russia", "@fashiondeals"
]

# Настройка логов
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
from aiogram.client.default import DefaultBotProperties

bot = Bot(
    token=API_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher(storage=MemoryStorage())
router = Router()

# Фильтр по каналу
class SourceChannelFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.chat.username:
            return f"@{message.chat.username}" in SOURCE_CHANNELS
        return False

@router.channel_post(SourceChannelFilter())
async def repost_handler(message: Message):
    try:
        if message.text:
            await bot.send_message(chat_id=TARGET_CHANNEL, text=message.text)
        elif message.photo:
            await bot.send_photo(chat_id=TARGET_CHANNEL, photo=message.photo[-1].file_id, caption=message.caption or "")
        elif message.video:
            await bot.send_video(chat_id=TARGET_CHANNEL, video=message.video.file_id, caption=message.caption or "")
    except Exception as e:
        logging.error(f"Ошибка при репосте: {e}")

dp.include_router(router)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())