from typing import Dict, List


class Project():
    def __init__(self, root, content: Dict[str, List[str]], language):
        self.root = root
        self.content = content 
        self.language = language
