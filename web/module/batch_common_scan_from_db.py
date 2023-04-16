from typing import List
from loguru import logger


def batch_common_scan_from_db(project_id: int, repo: str, root: str, language: List[str], scheduler: str, exclude=[], key="", proxy="", dry=False):
    import manager
    import loader
    import utils
    mgr = manager.Manager(from_db=True)
    if len(key):
        mgr.set_key(key)
    if len(proxy):
        mgr.set_proxy(proxy)
    pro = loader.load_project(root, language)
    sch = manager.DefaultScheduler([k for k in pro.content])
    while not sch.null():
        name = sch.next()
        select = manager.Select([name], exclude)
        try:
            res = mgr.ask(pro, select, dry)
            if res:
                utils.dump2db(project_id, res, name)
            logger.info("[Batch Common Scan] [*] finish: {}, rest {} files".format(name, sch.length()))
        except Exception as e:
            logger.error(e)
    return None
