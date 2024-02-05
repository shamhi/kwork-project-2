from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.enums import ParseMode

from app.utils import logger
from app.config import Config
from app.routers import private
from app.middlewares import InfoLoggerMiddleware, ConnectDB


async def setup_commands(bot: Bot):
    commands = [
        BotCommand(command='start', description='Запуск'),
        BotCommand(command='cancel', description='Отмена'),
    ]

    await bot.set_my_commands(commands=commands)


async def aiogram_on_startup(dispatcher: Dispatcher, bot: Bot):
    await bot.delete_webhook(drop_pending_updates=True)
    await setup_aiogram(dp=dispatcher, bot=bot)
    dispatcher['aiogram_logger'].info("Started polling")


async def aiogram_on_shutdown(dispatcher: Dispatcher, bot: Bot):
    dispatcher['aiogram_logger'].debug("Stopping polling")
    await bot.session.close()
    await dispatcher.storage.close()
    dispatcher['aiogram_logger'].info("Stopped polling")


async def setup_aiogram(dp: Dispatcher, bot: Bot):
    await setup_commands(bot=bot)
    setup_logging(dp=dp)
    logger = dp['aiogram_logger']
    logger.debug("Configure aiogram")
    setup_routers(dp=dp)
    setup_middlewares(dp=dp)
    logger.info("Configured aiogram")


def setup_routers(dp: Dispatcher):
    dp.include_router(private)


def setup_logging(dp: Dispatcher):
    dp['aiogram_logger'] = logger.bind(type='aiogram')
    dp['info_logger'] = logger.bind(type='info')


def setup_middlewares(dp: Dispatcher):
    dp.update.outer_middleware(InfoLoggerMiddleware(dp['info_logger']))
    dp.message.middleware(ConnectDB('db'))
    dp.callback_query.middleware(ConnectDB('db'))


def main():
    bot = Bot(token=Config.MAIN_BOT_TOKEN, parse_mode=ParseMode.HTML)

    dp = Dispatcher()

    dp.startup.register(aiogram_on_startup)
    dp.shutdown.register(aiogram_on_shutdown)

    dp.run_polling(bot)


if __name__ == '__main__':
    main()
