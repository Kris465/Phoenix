import re

from loguru import logger


class Parser:
    def __init__(self, task) -> None:
        self.task = task

    async def parse(self):
        webpage_name = re.sub(r'^https?://(?:www\.)?(.*?)/.*$', r'\1',
                              self.task["url"])
        logger.info(f"Webpage name is {webpage_name}")
        # Скорректировать аргументы для будущих классов
        if self.task["mod"] == 1:
            stepper = Stepper()
        elif self.task["mod"] == 2:
            collector = Collector()
