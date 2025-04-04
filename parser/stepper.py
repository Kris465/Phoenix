import asyncio
import json
import os
import random
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from loguru import logger


class Stepper:
    def __init__(self, task, webpage) -> None:
        self.task = task
        self.webpage_name = webpage
        self.number = task["chapter"]

    async def parse(self):
        with open("parser/StepperLibrary.json", encoding="UTF-8") as file:
            library = json.load(file)
        try:
            working_set = library[self.webpage_name][0]
        except KeyError:
            logger.debug(f"Add {self.webpage_name} into StepperLibrary.json")
            return

        url = self.task['url']
        chapters = {}
        next_link = " "
        page = " "
        while next_link and page is not None:
            await asyncio.sleep(random.randint(1, 60))
            page = await asyncio.to_thread(self.get_webpage, url,
                                           working_set['tool'])
            logger.info(f"got PAGE / {self.task['title']} / {url}")
            if page is not None:
                text = self.collect_chapter(page, working_set["tag"],
                                            working_set["extra_tag"])
                chapter = {self.number: url + text}
                next_link = self.get_next_link(page, working_set["word"],
                                               self.webpage_name)
                logger.info(f"got TEXT / {self.task['title']} / "
                            f"{self.number} / {next_link}")
                chapters.update(chapter)
                self.number += 1
                if next_link == url:
                    break
                else:
                    url = next_link
            else:
                break

        novel_folder = os.path.join("novels", self.task['title'])
        os.makedirs(novel_folder, exist_ok=True)
        novel_file_path = os.path.join(novel_folder,
                                       f"{self.task['title']}.json")
        with open(novel_file_path, "w", encoding="UTF-8") as file:
            json.dump(chapters, file, ensure_ascii=False, indent=4)

    def get_webpage(self, url, tool=None):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
        }

        try:
            response = requests.get(url, headers=headers)
            logger.info(f"{self.task['title']} / "
                        f"{url} / {response.status_code}")
        except Exception as e:
            logger.error(e)
            return
        if response.status_code != 200:
            logger.debug(f"Connection problem / "
                         f"{response.status_code} / {url}")
        match tool:
            case "requests":
                soup = BeautifulSoup(response.text, 'lxml')
                return soup
            case "zh":
                response.encoding = response.apparent_encoding
                soup = BeautifulSoup(response.text, 'html.parser')
                return soup
            case "selenium":
                options = webdriver.ChromeOptions()
                options.add_argument("--headless")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                driver = webdriver.Chrome(
                    service=Service(ChromeDriverManager().install()),
                    options=options)
                driver.get(url)

                def slow_scroll(driver):
                    last_height = driver.execute_script(
                        "return document.body.scrollHeight")

                    while True:
                        driver.execute_script(
                            "window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(2)
                        new_height = driver.execute_script(
                            "return document.body.scrollHeight")
                        if new_height == last_height:
                            break
                        last_height = new_height

                slow_scroll(driver)
                html_code = driver.page_source
                soup = BeautifulSoup(html_code, 'html.parser')
                return soup

    def collect_chapter(self, page, tag, extra_tag):
        try:
            result = page.find_all(tag, class_=extra_tag)
        except ValueError:
            result = page.find_all(tag, id=extra_tag)
            logger.info("id for extra-tag")
        text = "".join(set([i.text for i in result]))
        return text

    def get_next_link(self, page, word, webpage_name):
        links = page.find_all("a")
        for link in links:
            # Сделать код для chapter + number
            if word in link.text:
                if webpage_name in link["href"] and link['href'] != '#':
                    next_link = link['href']
                    next_link.strip()
                else:
                    next_link = f"https://{webpage_name}/{link['href']}"
                    # next_link = f"https://{webpage_name}{link['href']}"
                    next_link.strip()
                break
            else:
                next_link = None
        return next_link
