import asyncio
from typing import List

from loguru import logger
from domain.filemanager import FileManager

from parser.parser import Parser
from translator.translator import TrManager


class Controller:
    def __init__(self, tasks: List[dict]) -> None:
        self.tasks = tasks

    async def execute_task(self, task) -> None:
        if task["action"] == "parse":
            try:
                pars = Parser(task)
                await pars.parse()
                logger.info(f"Parsing finished / {task['title']}")
            except Exception as e:
                logger.error(f'parsing error / {e}')
        elif task["action"] == "translate":
            try:
                trans = TrManager(task["title"],
                                  task["language"],
                                  task["config"])
                await asyncio.sleep(3)
                await trans.translate()
                logger.info(f"Translating task is created / {task['title']}")
            except Exception as e:
                logger.error(f'translating error / {e}')
        elif task["action"] == "save":
            try:
                fileManeger = FileManager(task)
                await fileManeger.save()
            except Exception as e:
                logger.error(f'saving error / {e}')

    async def run(self) -> None:
        tasks = [self.execute_task(task) for task in self.tasks]
        await asyncio.gather(*tasks)
