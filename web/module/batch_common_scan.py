from typing import List
from loguru import logger


def batch_common_scan(root: str, language: List[str], scheduler: str, exclude=[], key="", proxy="", output="", dry=False):
    import manager
    import loader
    import utils
    mgr = manager.Manager()
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
                if len(output):
                    utils.dump_file(res, output, name)
                else:
                    utils.dump(res)
            logger.info("[Batch Common Scan] [*] finish: {}, rest {} files".format(name, sch.length()))
        except Exception as e:
            logger.error(e)
    return None
