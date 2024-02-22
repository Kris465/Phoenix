class Collector:
    def __init__(self, task, webpage) -> None:
        self.task = task
        self.webpage_name = webpage

    async def parse(self):
        # читаем библиотеку, берем теги и название сортировки -
        # разветвление для подключения или нет сортировки
        # Собираем текст по ссылкам в цикле
        pass
