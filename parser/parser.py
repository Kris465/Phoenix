import re

from loguru import logger
from parser.collector import Collector

from parser.stepper import Stepper


class Parser:
    def __init__(self, task) -> None:
        self.task = task

    async def parse(self):
        webpage_name = re.sub(r'^https?://(?:www\.)?(.*?)/.*$', r'\1',
                              self.task["url"])
        logger.info(f"Webpage name is {webpage_name}")
        if self.task["mod"] == 1:
            stepper = Stepper(self.task, webpage_name)
            stepper.parse()
        elif self.task["mod"] == 2:
            collector = Collector(self.task, webpage_name)
            collector.parse()
