import asyncio
import json
import random
import requests
from bs4 import BeautifulSoup

from loguru import logger


class Stepper:
    def __init__(self, task, webpage) -> None:
        self.task = task
        self.webpage_name = webpage
        self.number = task["chapter"]

    async def parse(self):
        with open("StepperLibrary.json", encoding="UTF-8") as file:
            library = json.load(file)
        working_set = library[self.webpage_name]

        url = self.task["url"]
        chapters = {}
        next_link = ""
        page = ""
        while next_link and page is not None:
            await asyncio.sleep(random.randint(5, 15))
            try:
                page = await asyncio.to_thread(self.get_webpage, url)
                text = self.collect_chapter(page, working_set["tag"],
                                            working_set["extra_tag"])
                chapter = {self.number: url + text}
                next_link = self.get_next_link(page, working_set["word"],
                                               working_set["tool"],
                                               self.webpage_name)
                if next_link == url:
                    break
                logger.info(f"got text {self.task['title']}"
                            f"{self.number} / {next_link}")
                chapters.update(chapter)
                self.number += 1
                url = next_link
            except Exception as e:
                logger.error(e)
                break

    def get_webpage(self, url):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
                                AppleWebKit/537.36 (KHTML, like Gecko)\
                                Chrome/111.0.0.0 Safari/537.36'}
        response = requests.get(url, headers=headers)
        logger.info(f"{self.title} / {url} / {response.status_code}")
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            return soup
        else:
            return

    def collect_chapter(self, page, tag, extra_tag):
        try:
            result = page.find_all(tag, class_=extra_tag)
        except ValueError:
            result = page.find_all(tag, id=extra_tag)
            logger.info("id for extra-tag")
        text = "".join(set([i.text for i in result]))
        return text

    def get_next_link(self, page, word, webpage_name, tool=None):
        links = page.find_all("a")
        for link in links:
            # if word in link.text.lower():
            if word in link.text.lower() and link["href"] != "#":
                if webpage_name in link["href"]:
                    next_link = link['href']
                else:
                    next_link = f"https://{webpage_name}/{link['href']}"
                    # next_link = f"https://{webpage_name}{link['href']}"
                break
            else:
                next_link = None
        return next_link
