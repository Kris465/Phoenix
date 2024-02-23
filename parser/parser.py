import re

from loguru import logger
from parser.collector import Collector

from parser.stepper import Stepper


class Parser:
    def __init__(self, task) -> None:
        self.task = task

    async def parse(self):
        if isinstance(self.task['url'], str):
            webpage_name = re.sub(r'^https?://(?:www\.)?(.*?)/.*$', r'\1',
                                  self.task["url"])
        elif isinstance(self.task['url'], list):
            webpage_name = re.sub(r'^https?://(?:www\.)?(.*?)/.*$', r'\1',
                                  self.task["url"][0])
        else:
            return
        logger.info(f"Webpage name is {webpage_name}")
        if self.task["mod"] == "Stepper":
            stepper = Stepper(self.task, webpage_name)
            await stepper.parse()
        elif self.task["mod"] == "Collector":
            collector = Collector(self.task, webpage_name)
            await collector.parse()
