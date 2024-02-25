import asyncio
import json
import os
import random
from bs4 import BeautifulSoup

from loguru import logger
import requests


class Collector:
    def __init__(self, task, webpage) -> None:
        self.task = task
        self.webpage_name = webpage
        self.number = task['chapter']

    async def parse(self):
        with open("parser/CollectorLibrary.json", encoding="UTF-8") as file:
            library = json.load(file)
        try:
            working_set = library[self.webpage_name][0]
        except KeyError:
            logger.debug(f"Add {self.webpage_name} into StepperLibrary.json")
            return

        match working_set['sort']:
            case "noSort":
                links = self.task['url']
            case "area_sort":
                page = self.get_webpage(self.task['url'][0],
                                        working_set['tool'])
                area = page.find(working_set["area_tag"],
                                 working_set["area_extra_tag"])
                links = [link["href"] for link in area.find_all("a")]
            case "tail_sort":
                pass

        chapters = {}
        for link in links:
            await asyncio.sleep(random.randint(5, 15))
            page = self.get_webpage(link, working_set['tool'])
            text = self.collect_chapter(page, working_set['tag'],
                                        working_set['extra_tag'])
            chapter = {self.number: link + text}
            self.number += 1
            chapters.update(chapter)

        novel_folder = os.path.join("novels", self.task['title'])
        os.makedirs(novel_folder, exist_ok=True)
        novel_file_path = os.path.join(novel_folder,
                                       f"{self.task['title']}.json")
        with open(novel_file_path, "w", encoding="UTF-8") as file:
            json.dump(chapters, file, ensure_ascii=False, indent=4)

    def get_webpage(self, url, tool=None):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
                                AppleWebKit/537.36 (KHTML, like Gecko)\
                                Chrome/111.0.0.0 Safari/537.36'}
        response = requests.get(url, headers=headers)
        logger.info(f"{self.task['title']} / {url} / {response.status_code}")
        if response.status_code != 200:
            logger.debug("Connection problem")
        match tool:
            case "requests":
                soup = BeautifulSoup(response.text, 'lxml')
                return soup
            case "zh":
                response.encoding = response.apparent_encoding
                soup = BeautifulSoup(response.text, 'html.parser')
                return soup
            case "selenium":
                pass

    def collect_chapter(self, page, tag, extra_tag):
        try:
            result = page.find_all(tag, class_=extra_tag)
        except ValueError:
            result = page.find_all(tag, id=extra_tag)
            logger.info("id for extra-tag")
        text = "".join(set([i.text for i in result]))
        return text
