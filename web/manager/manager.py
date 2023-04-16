import os
import time
import random
import openai
import threading
from loader.project import *
from loader.loader import *
from manager.select import *
from loguru import logger
from typing import List
from utils.config import Config
from utils.mysql_utils import getAllKey

# Act as a web security expert and ready to receive project
SYSTEM_PROMPT_1 = "You are a web security expert and I will send you a project. If there is no vulnerability, say 'NoVulnH3r3' at the start of answer. If there is any vulnerabilities, say 'VulnRh3r3' at the start of answer."
# General security assessment
NEED_PROMPT_1 = "Please analyse code above and tell me vulnerabilities in it. Mark every vulnerability with info, warn, medium, high or critical by severity"
# A need prefix to make gpt work better
NEED_PREFIX = "Please analyse code above. "
# Find all taint chains from a given source
NEED_PROMPT_2 = "Can {} become input or parameter of dangerous function calls? Give me the function call chain in format of {}"
# Find all taint chains to a given sink
NEED_PROMPT_3 = "Can remote input in request become input or parameter of {} in a function call chain? Give me the function call chain in format of {}"
# One function call perline format
DEFUALT_TAINT_PROMPT = "one function call per line"
# Editor format
EDITOR_TAINT_PROMPT = "number\n function name\n file name\n line number\n code snippet less than 3 lines\n"
# Semgrep report format
SEMGREP_PROMPT = "semgrep report"
# CodeQL report format
CodeQL_PROMPT = "CodeQL report"


# General security assessment


def need_prompt_1() -> str:
    return NEED_PROMPT_1


# Find all taint chains from a given source


def need_prompt_2(source: str, prompt=DEFUALT_TAINT_PROMPT) -> str:
    return NEED_PREFIX + NEED_PROMPT_2.format(source, prompt)


# Find all taint chains to a given sink


def need_prompt_3(sink: str, prompt=DEFUALT_TAINT_PROMPT) -> str:
    return NEED_PREFIX + NEED_PROMPT_3.format(sink, prompt)


def match_include(path: str, include: List[str]) -> bool:
    from platform import platform
    if platform().startswith("Windows"):
        path = path[1:].replace("\\", "/")
    if len(include) == 0:
        return True
    for v in include:
        if path.startswith(v):
            return True
    return False


def _ask(messages):
    try:
        api_key = RateLimit.get_api_key()
        return openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            api_key=api_key
        )
    except openai.error.AuthenticationError as e:
        logger.error(e)
        RateLimit.remove_invalid_apikey(api_key)
        with open("error_log", "w+") as f:
            f.write(str(e) + "\n")
    except Exception as e:
        logger.error(e)


def build_message(messages, pro: Project, select: Select, dry=False):
    for path in pro.content:
        if match_include(path, select.include) and path not in select.exclude:
            if dry:
                logger.info(f'[build message] (dry is True) path: {path}')
            for k, v in enumerate(pro.content[path]):
                messages.append(
                    {"role": "user", "content": "relative path: {}, part number: {}\n{}".format(path, k, v)})


# add verify=False in openai/api_requestor.py#request_raw L524 to bypass ssl verification


class RateLimit:
    # 支持多token，只需要在这里面加一个openai.api_key = xxx就可以，因为key是从静态全局变量读取的，每次请求前修改就可以
    lock = threading.Lock()
    rate_limit = 60
    api_key_list: List[str] = Config().config["api_key"]
    available_api_key_list: List[str] = [api_key for api_key in api_key_list]
    count_dict: Dict[str, int] = {api_key: 0 for api_key in api_key_list}
    last_refresh_time_dict: Dict[str, float] = {api_key: time.time() for api_key in api_key_list}

    @classmethod
    @logger.catch
    def get_api_key(cls) -> str:
        cls.lock.acquire()
        cls.refresh_count()
        if len(cls.api_key_list) == 0:
            logger.warning(f"[Rate Limit] ATTENTION! There is no available api_key.")
            while True:
                time.sleep(6000)
        if len(cls.available_api_key_list) == 0:
            cls.wait_for_next_min()
        api_key = cls.choose_one()
        cls.lock.release()
        return api_key

    @classmethod
    @logger.catch
    def choose_one(cls) -> str:
        api_key = random.choice(cls.available_api_key_list)
        cls.count_dict[api_key] += 1
        if cls.count_dict[api_key] == cls.rate_limit:
            cls.available_api_key_list.pop(cls.available_api_key_list.index(api_key))
            logger.warning(f"[Rate Limit] api_key {api_key[:5]} reached rate limit, wait 60s to re-enable it.")
        return api_key

    @classmethod
    @logger.catch
    def refresh_count(cls):
        # 当前时间超过refresh_time，则刷新count
        now_time = time.time()
        for api_key in cls.api_key_list:
            if (now_time - cls.last_refresh_time_dict[api_key]) >= 60:
                cls.last_refresh_time_dict[api_key] = now_time
                cls.count_dict[api_key] = 0
                if api_key not in cls.available_api_key_list:
                    cls.available_api_key_list.append(api_key)

    @classmethod
    @logger.catch
    def wait_for_next_min(cls):
        most_recent_refresh_time = min(cls.last_refresh_time_dict.values())
        time_to_next_min = (60 - (time.time() - most_recent_refresh_time) + 1)
        if time_to_next_min > 0:
            logger.warning(f"[Rate Limit] all api_keys have reached rate limit. sleep {time_to_next_min} s to refresh count.")
            time.sleep(time_to_next_min)
        cls.refresh_count()

    @classmethod
    @logger.catch
    def remove_invalid_apikey(cls, api_key: str):
        if api_key in cls.available_api_key_list:
            cls.available_api_key_list.pop(cls.available_api_key_list.index(api_key))
        if api_key in cls.api_key_list:
            cls.api_key_list.pop(cls.api_key_list.index(api_key))
        logger.warning(f"[Rate Limit - Error] the api_key: {api_key} is invalid.")


class Manager:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
            cls.init(*args, **kwargs)
        return cls.__instance

    @classmethod
    def init(cls, from_db=False):
        if from_db:
            api_key_list = getAllKey()
            logger.info(f'[Manager] Get {len(api_key_list)} key from db.')
            RateLimit.api_key_list = api_key_list
            RateLimit.available_api_key_list = [api_key for api_key in api_key_list]
            RateLimit.count_dict = {api_key: 0 for api_key in api_key_list}
            RateLimit.last_refresh_time_dict = {api_key: time.time() for api_key in api_key_list}
        else:
            api_key = os.getenv("OPENAI_API_KEY")
            proxy = os.getenv("CHATGPT_PROXY")
            if api_key is not None:
                cls.set_key(api_key)
            if proxy is not None:
                cls.set_proxy(proxy)

    @staticmethod
    def set_key(api_key: str):
        RateLimit.api_key_list = [api_key]
        RateLimit.available_api_key_list = [api_key]
        RateLimit.count_dict = {api_key: 0}
        RateLimit.last_refresh_time_dict = {api_key: time.time()}

    @staticmethod
    def set_proxy(proxy: str):
        openai.proxy = proxy

    # ask by src, use with load_one
    @staticmethod
    def ask_src(src: List[str]):
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT_1}]
        for chunk in src:
            messages.append({"role": "user", "content": chunk})
        messages.append(
            {"role": "user", "content": NEED_PROMPT_1})

        return _ask(messages)

    # ask by project and select
    @staticmethod
    def ask(pro: Project, select: Select, dry=False):
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT_1}]
        build_message(messages, pro, select, dry)
        messages.append(
            {"role": "user", "content": NEED_PROMPT_1})
        if dry:
            return
        return _ask(messages)

    # ask by project, question and select
    @staticmethod
    def ask_question(pro: Project, select: Select, question: str, dry=False):
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT_1}]
        build_message(messages, pro, select, dry)
        messages.append(
            {"role": "user", "content": question}
        )
        if dry:
            return
        return _ask(messages)

    # load project by select pack and ask by question
    @classmethod
    def execute_task(cls, task: Task, dry=False):
        pro = load_project(task.root, task.language)
        return cls.ask(pro, task.select, dry)

    # load project by select pack and ask by question
    @classmethod
    def execute_task_question(cls, task: Task, question: str, dry=False):
        pro = load_project(task.root, task.language)
        return cls.ask_question(pro, task.select, question, dry)
