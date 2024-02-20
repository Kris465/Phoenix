import asyncio
from loguru import logger

from domain.controller import Controller
from user.user_menu import UserMenu


async def main():
    logger.add("file.log",
               format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
               rotation="3 days",
               backtrace=True, diagnose=True)

    user_menu = UserMenu()
    tasks = user_menu.menu()

    controller = Controller(tasks)
    await controller.run()

if __name__ == '__main__':
    asyncio.run(main())
