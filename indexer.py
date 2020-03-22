# -*- coding: utf-8 -*-

import requests
from logging import getLogger
from threading import Thread
from typing import List
from urllib.parse import urlparse

from database_manager import DatabaseManager
from parser import ParsedData, Parser
from settings import (
    INDEXER_MAX_ACTIVE_THREAD,
    INDEXER_PROXY_SETTINGS,
    INDEXER_THREADS_MAX_DEPTH,
)

logger = getLogger(__name__)


class IndexingNode(Thread):
    # we use mutable object to conserve the same memory address (more on: https://dzone.com/articles/python-class-attributes-vs-instance-attributes)
    _active_threads_number = [0]

    @classmethod
    def _increment_active_threads(cls):
        cls._active_threads_number[0] += 1

    @classmethod
    def _decrement_active_threads(cls):
        cls._active_threads_number[0] -= 1

    def __init__(
        self, target_url: str = None, current_thread_depth: int = 0,
    ):
        super(IndexingNode, self).__init__()
        self._target_url = target_url
        self._current_thread_depth = current_thread_depth
        self._increment_active_threads()

    def _fetch_html_content_or_raise_exception(self) -> str:
        response = requests.get(self._target_url, proxies=INDEXER_PROXY_SETTINGS)
        content_encoding = response.encoding if response.encoding else "utf-8"
        return response.content.decode(content_encoding)

    def _insert_content_into_database(self, parsed_data: ParsedData) -> None:
        db_manager = DatabaseManager()
        # Granting not having a duplicate key error in case the script is run multiple times
        if db_manager.find({"_id": self._target_url}).count() == 0:
            db_manager.insert(parsed_data.to_dict())
            logger.info(f"> Inserted successfully into db: {self._target_url}")
            logger.info(f"> Number of objects in db: {db_manager.inserts_count}")
        else:
            logger.info(f"> URL already existing in the db: {self._target_url}")

    def _create_child_indexing_nodes(self, urls_list: List[str]) -> None:
        db_manager = DatabaseManager()
        current_parsed_url = urlparse(self._target_url)
        hostname = f"{current_parsed_url.scheme}://{current_parsed_url.netloc}"
        for url in urls_list:
            if self._active_threads_number[0] <= INDEXER_MAX_ACTIVE_THREAD:
                if url.startswith("/"):  # Relative paths
                    url = f"{hostname}/{url[1:]}"
                # Making sure not handling an already existing URL (in the same runtime)
                if db_manager.find({"_id": url}).count() == 0:
                    child_node_args = {
                        "target_url": url,
                        "current_thread_depth": self._current_thread_depth + 1,
                    }
                    indexing_node = IndexingNode(**child_node_args)
                    indexing_node.start()

    def run(self) -> None:
        logger.info(
            f"> New thread started for {self._target_url} (tree depth={self._current_thread_depth}, active threads={self._active_threads_number[0]}))"
        )
        try:
            html_content: str = self._fetch_html_content_or_raise_exception()
        except requests.exceptions.RequestException as e:
            logger.warning(e)
        else:
            parsed_data: ParsedData = Parser.parse_html(self._target_url, html_content)
            self._insert_content_into_database(parsed_data)
            if self._current_thread_depth < INDEXER_THREADS_MAX_DEPTH:
                self._create_child_indexing_nodes(parsed_data.urls)

        self._decrement_active_threads()
