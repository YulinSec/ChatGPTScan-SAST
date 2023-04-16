from typing import List


def custom_query(root: str, language: List[str], question: str, include=[], exclude=[], key="", proxy="", dry=False):
    import manager
    mgr = manager.Manager()
    if len(key):
        mgr.set_key(key)
    if len(proxy):
        mgr.set_proxy(proxy)
    task = manager.Task(root, language, include, exclude)
    return mgr.ask_question(task, question, dry)