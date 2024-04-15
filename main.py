import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
import core.callback
import core.callback.callback_query
import utilites.cfg as cfg
from handlers import menu
import core


logging.basicConfig(level=logging.INFO)

bot = Bot(token=cfg.TOKEN)

dp = Dispatcher()

async def main():

    await bot.delete_webhook(drop_pending_updates=True)

    await bot.set_my_commands(commands=[types.BotCommand(command='genre', description='"/genre (жанр)", чтобы искать книги по жанру')], scope=types.BotCommandScopeDefault())


    dp.include_routers(menu.router, core.callback.callback_query.router)

    try:
        await dp.start_polling(bot)
    except Exception as e:
        print("ERROR : Failed to fetch updates!\n")
        print(e)

if __name__ == "__main__":
    asyncio.run(main())
