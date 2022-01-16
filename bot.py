import asyncio
import logging
from pathlib import Path
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.files import JSONStorage

from config import load_config
from TransferBot import register_handlers_transfers
from common import register_handlers_common
from PretrainedBot import register_handlers_pred
from GanBot import register_handlers_gan
logger = logging.getLogger(__name__)


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/trans", description="Создать по своему стилю"),
        BotCommand(command="/pretrained", description="Использовать предобученную модель"),
        BotCommand(command="/gan", description="Выбрать имеющийся стиль"),
        BotCommand(command="/cancel", description="Отменить текущее действие"),
        BotCommand(command="/help", description="Начальное меню"),
    ]
    await bot.set_my_commands(commands)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")

    # Парсинг файла конфигурации
    config = load_config("bot.ini")

    # Объявление и инициализация объектов бота и диспетчера
    bot = Bot(token=config.tg_bot.token)
    storage = JSONStorage(Path('states.json'))
    dp = Dispatcher(bot, storage=storage)

    register_handlers_common(dp, config.tg_bot.admin_id)
    register_handlers_gan(dp)
    register_handlers_pred(dp)
    register_handlers_transfers(dp)

    await set_commands(bot)
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())
