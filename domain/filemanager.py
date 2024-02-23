import json
import os


class FileManager:
    def __init__(self, task) -> None:
        self.task = task

    async def save(self):
        file_path = f"novels/{self.task['title']}/{self.task['title']}_translated.json"
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding="utf-8") as file:
                project = json.load(file)
            flag = True
        elif os.path.exists(f"novels/{self.task['title']}/{self.task['title']}.json"):
            file_path = f"novels/{self.task['title']}/{self.task['title']}.json"
            with open(file_path, 'r', encoding="utf-8") as file:
                project = json.load(file)
            flag = False
        else:
            return

        text = ' '
        match self.task['file']:
            case 1:
                if flag:
                    for chapter, data in project.items():
                        text += chapter + '\n'.join(
                            str(value) for dictionary in data
                            for value in dictionary.values())
                else:
                    for k, v in project.items():
                        text += k + "\n" + v + "\n"

                with open(
                    f'novels/{self.task["title"]}/{self.task["title"]}.txt',
                        'w', encoding="UTF-8") as file:
                    file.write(text)
            case 2:
                for chapter, data in project.items():
                    if flag:
                        text = '\n'.join(str(value) for dictionary in data
                                         for value in dictionary.values())
                    else:
                        text += chapter + "\n" + data + "\n"

                    with open(f'novels/{self.task["title"]}/{chapter}.txt',
                              'w', encoding="UTF-8") as file:
                        file.write(text)
