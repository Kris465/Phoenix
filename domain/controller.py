import asyncio
from typing import List

from loguru import logger

from parser.parser import Parser


class Controller:
    def __init__(self, tasks: List[dict]) -> None:
        self.tasks = tasks

    async def execute_task(self, task) -> None:
        if task["action"] == "parse":
            pars = Parser(task)
            await pars.parse()
            logger.info(f"Parsing finished / {task['title']}")
        elif task["action"] == "translate":
            trans = TrManager(task["title"], task["language"], task["config"])
            await asyncio.sleep(3)
            await trans.translate()
            logger.info(f"Translating task is created / {task['title']}")
        elif task["action"] == "save":
            # Дописать обработку файлов и папок
            pass

    async def run(self) -> None:
        tasks = [self.execute_task(task) for task in self.tasks]
        await asyncio.gather(*tasks)
