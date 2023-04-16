import os
import threading
from queue import Queue

import module
import utils
import time
from typing import List
from loguru import logger


class ChatGPTScan:
    """
    ChatGPTScan help summary page

    A white box code scan powered by ChatGPT

    Example:

        python chatgptscan.py common_scan --conf conf/common_scan_python_example.yaml --key <your-openai-api-key>

        python chatgptscan.py common_scan --project ./benchmark/python_demo --language "['python']" --include "['directory']" --proxy http://127.0.0.1:7890

        python chatgptscan.py taint_sink_scan --project ./benchmark/python_demo --language "['python']" --sink "os.system()"  --exclude "['directory/exclude.go']"

    Note:
        --conf          use config file to set command option
        --project       path to target project
        --language      languages of the project, decide which file extension will be loaded
        --include       files send to ChatGPT, relative directory or relative filepath, match by prefix
        --exclude       files not send to ChatGPT, relative directory or relative filepath, match by prefix
        --sink          decrible your sink, only works in taint_sink_scan
        --question      custom question
        --output        output file path, only support batch_common_scan
        --key           openai api key, also get from environment variable OPENAI_API_KEY
        --proxy         openai api proxy
        --dry           dry run, not send files to ChatGPT

    """

    @staticmethod
    def common_scan(project: str = "", language: List[str] = [], include: List[str] = [], exclude: List[str] = [], conf="", key="", proxy="", dry=False):
        """
        scan project file and output report
        """
        # parameters are all from cli, passed by module Fire
        params = utils.load_conf(project=project, language=language,
                                 include=include, exclude=exclude, conf=conf, key=key, proxy=proxy, dry=dry)

        utils.check_params(
            project=params["project"], language=params["language"])

        res = module.common_scan(params["project"], params["language"],
                                 params["include"], params["exclude"], params["key"], params["proxy"], params["dry"])
        if res:
            utils.dump(res)

    @staticmethod
    def batch_common_scan(project: str = "", language: List[str] = [], scheduler: str = "", exclude: List[str] = [], conf="", key="", proxy="", output="", dry=False):
        """
        scan all projects  and output report
        """
        # parameters are all from cli, passed by module Fire
        params = utils.load_conf(project=project, language=language, scheduler=scheduler,
                                 exclude=exclude, conf=conf, key=key, proxy=proxy, output=output, dry=dry)

        utils.check_params(
            project=params["project"], language=params["language"])

        module.batch_common_scan(params["project"], params["language"],
                                 params["scheduler"], params["exclude"], params["key"], params["proxy"], params["output"], params["dry"])

    @staticmethod
    def taint_sink_scan(project: str = "", language: List[str] = [], sink: str = "", include: List[str] = [], exclude: List[str] = [], conf="", key="", proxy="", dry=False):
        """
        scan project and output taint path to sink
        """
        # parameters are all from cli, passed by module Fire
        params = utils.load_conf(project=project, language=language, sink=sink,
                                 include=include, exclude=exclude, conf=conf, key=key, proxy=proxy, dry=dry)

        utils.check_params(
            project=params["project"], language=params["language"], sink=params["sink"])

        res = module.taint_sink_scan(
            params["project"], params["language"], params["sink"], params["include"], params["exclude"], params["key"], params["proxy"], params["dry"])

        if res:
            utils.dump(res)

    @staticmethod
    def custom_query(project: str = "", language: List[str] = [], question: str = "", include: List[str] = [], exclude: List[str] = [], conf="", key="", proxy="", dry=False):
        """
        scan project with a custom query question
        """
        # parameters are all from cli, passed by module Fire
        params = utils.load_conf(project=project, language=language, question=question,
                                 include=include, exclude=exclude, conf=conf, key=key, proxy=proxy, dry=dry)

        utils.check_params(
            project=params["project"], language=params["language"], question=params["question"])

        res = module.custom_query(
            params["project"], params["language"], params["question"], params["include"], params["exclude"], params["key"], params["proxy"], params["dry"])

        if res:
            utils.dump(res)

    @staticmethod
    def github_scan(repo: str = "", language: List[str] = [], include: List[str] = [], exclude: List[str] = [], conf="", key="", proxy="", dry=False) -> None:
        """
        scan open-source project from GitHub. Need Git installed.
        """
        # Download project, save to directory and scan by batch_common_scan
        utils.check_params(repo=repo)
        utils.prepare_dir()
        repo_params = utils.generate_repo_params(repo=repo)
        logger.info(f'[GitHub Scan] start - repo: {repo_params["repo_name"]}, url: {repo}')
        start_time = time.time()
        utils.clone_repo_from_github(repo=repo, project_path=repo_params["project_path"])
        ChatGPTScan.batch_common_scan(project=repo_params["project_path"], language=language,
                                      exclude=exclude, conf=conf, key=key, proxy=proxy, output=repo_params["output"], dry=dry)
        end_time = time.time()
        logger.info(f'[GitHub Scan] finish - repo: {repo_params["repo_name"]}, url: {repo}, took time: {end_time - start_time} s')

    @staticmethod
    def batch_github_scan(threads=10, conf="", key="", proxy="") -> None:
        """
        automatically download the repo from GitHub and scan source codes.
        load source from file in github_source.
        dir tree:
        github_source:
            languag1e(dir)
                category1: (file)
                category1: (file)
            ...
        Examples:
        github_source:
            java:
                framework: there is GitHub URL ending with .git in each line.
        """
        utils.start_multi_threading(threads=threads, func=ChatGPTScan.github_scan, conf=conf, key=key, proxy=proxy)
        logger.info(f'[Batch GitHub Scan] Finished.')

    @staticmethod
    def _github_scan_from_db(project_id: int, repo: str = "", language: List[str] = [], include: List[str] = [], exclude: List[str] = [],scheduler: str = "", conf="", key="", proxy="", dry=False) -> None:
        """
        scan open-source project from GitHub. Need Git installed.
        todo: record update time to db.
        """
        # Download project, save to directory and scan by batch_common_scan
        utils.check_params(repo=repo)
        utils.prepare_dir()
        repo_params = utils.generate_repo_params(repo=repo)
        logger.info(f'[GitHub Scan] start - repo: {repo_params["repo_name"]}, url: {repo}')
        start_time = time.time()
        utils.clone_repo_from_github(repo=repo, project_path=repo_params["project_path"])

        params = utils.load_conf(repo=repo, project=repo_params["project_path"], language=language, scheduler=scheduler, exclude=exclude, conf=conf, key=key, proxy=proxy, dry=dry)

        utils.check_params(project=params["project"], language=params["language"])

        module.batch_common_scan_from_db(project_id, params["repo"], params["project"], params["language"], params["scheduler"], params["exclude"], params["key"], params["proxy"], params["dry"])
        end_time = time.time()
        logger.info(f'[GitHub Scan] finish - repo: {repo_params["repo_name"]}, url: {repo}, took time: {end_time - start_time} s')
        utils.del_project(project_path=repo_params["project_path"])

    @staticmethod
    def automatic_scan(threads=10, conf="", key="", proxy="") -> None:
        utils.start_automatic_multi_threading(threads=threads, func=ChatGPTScan._github_scan_from_db, conf=conf, key=key, proxy=proxy)

