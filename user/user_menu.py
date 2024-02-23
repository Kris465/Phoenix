from loguru import logger


class UserMenu:
    def __init__(self) -> None:
        self.tasks = []

    def menu(self):
        print("What is your will, Master?\n")
        task = {}
        option = ''
        while option != 4:
            title = input("Title: ")
            if not title:
                break
            option = int(input("1.Parse\n2.Translate\n3.Save\n4.Exit\n"))
            task = self.create_task(title, option)
            self.tasks.append(task)
        return self.tasks

    def url_generator(self):
        while True:
            url = input("urls: \n")
            if not url:
                break
            if url.strip():
                yield url

    def create_task(self, title, option):
        match option:
            case 1:
                mod = int(input("Mod:\n1.Stepper\n2.Collector\n"))
                chapter = int(input("Chapter: "))
                if mod == 1:
                    url = input("url: ")
                    return {"action": "parse",
                            "title": title,
                            "mod": "Stepper",
                            "chapter": chapter,
                            "url": url}
                elif mod == 2:
                    urls = list(self.url_generator())
                    return {"action": "parse",
                            "title": title,
                            "mod": "Collector",
                            "chapter": chapter,
                            "url": urls}
                else:
                    logger.warning(
                        "Unknown parsing mod / UserMenu / create_task()")
            case 2:
                language = input("language: ")
                print("Input config data in spaces\n"
                      "1.All\n2.From\n3.From-To")
                config = [int(num) for num in input().split()]

                if language in ["zh", "en"]:
                    return {"action": "translate",
                            "title": title,
                            "language": language,
                            "config": config}
                else:
                    logger.warning(
                        "Unknown language / UserMenu / create_task()")
            case 3:
                file = int(input("1.in-one-file\n"
                                 "2.for-chapters\n"))
                doc_type = int(input("1.txt\n"
                                     "2.docx\n"))
                if file and doc_type in [1, 2]:
                    return {"action": "save",
                            "title": title,
                            "file": file,
                            "doc_type": doc_type}
                else:
                    logger.warning("Unknown files / UserMenu / create_task()")
