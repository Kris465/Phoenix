import json


class Collector:
    def __init__(self, task, webpage) -> None:
        self.task = task
        self.webpage_name = webpage
        self.number = task['chapter']

    async def parse(self):
        with open("parser/CollectorLibrary.json", encoding="UTF-8") as file:
            library = json.load(file)
        working_set = library[self.webpage_name][0]
        
        # читаем библиотеку, берем теги и название сортировки -
        # разветвление для подключения или нет сортировки
        # Собираем текст по ссылкам в цикле
        pass
