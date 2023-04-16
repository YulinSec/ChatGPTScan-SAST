from typing import List


class Select:
    def __init__(self, include: List[str], exclude=[]):
        self.include = include
        self.exclude = exclude


class Task:
    def __init__(self, root: str, language: List[str], include: List[str], exclude=[]):
        self.root = root
        self.language = language
        self.select = Select(include, exclude)
