from typing import List, Union, Literal

# Task types
ParsingMod = Literal["Stepper", "Collector"]
TaskAction = Literal["parse", "translate", "save"]
Language = Literal["zh", "en"]
FileOption = Literal[1, 2]


class BaseTask:
    title: str
    action: TaskAction


class ParseTask(BaseTask):
    action: Literal["parse"]
    mod: ParsingMod
    chapter: int
    url: Union[str, List[str]]


class TranslateTask(BaseTask):
    action: Literal["translate"]
    language: Language
    config: List[int]


class SaveTask(BaseTask):
    action: Literal["save"]
    file: FileOption


Task = Union[ParseTask, TranslateTask, SaveTask]
Tasks = List[Task]
