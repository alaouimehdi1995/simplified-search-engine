# -*- coding: utf-8 -*-
"""
Simplified Searching Engine, conceived and implemented by: ALAOUI Mehdi 2017
"""
import json
import logging
import os

logging.basicConfig(
    level=logging.INFO
)  # For more 'verbose' mode, use level=logging.DEBUG

# Search result displaying #############
DISPLAYED_RESULTS_PER_PAGE = 15
DISPLAYED_DESCRIPTION_LENGTH = 150

# Database settings ###################

DB_HOST = os.environ.get("DB_HOST", "database")
DB_PORT = os.environ.get("DB_PORT", 27017)
DB_NAME = os.environ.get("DB_NAME", "search_engine")

DATABASE_CONFIG = {
    "host": DB_HOST,
    "port": DB_PORT,
    "db_name": DB_NAME,
    "db_table_name": "search_engine",
}

# Indexer settings ###################

INDEXER_HTTP_PROXY = os.environ.get(
    "INDEXER_HTTP_PROXY", None
)  # could be, for example: 'http://10.23.201.11:3128'
INDEXER_HTTPS_PROXY = os.environ.get("INDEXER_HTTP_PROXY", None)
INDEXER_PROXY_SETTINGS = {
    "http": INDEXER_HTTP_PROXY,
    "https": INDEXER_HTTPS_PROXY,
}

INDEXER_START_URL = os.environ.get(
    "INDEXER_START_URL", "https://en.wikipedia.org/wiki/Main_Page"
)
INDEXER_THREADS_MAX_DEPTH = os.environ.get("INDEXER_THREADS_MAX_DEPTH", 5)
INDEXER_MAX_ACTIVE_THREAD = os.environ.get("INDEXER_MAX_ACTIVE_THREAD", 1200)


# Parser settings ####################

PARSER_STOP_WORDS_FILENAME = "stop_words.json"
PARSER_STOP_CHARS_FILENAME = "stop_chars.json"

with open(PARSER_STOP_WORDS_FILENAME, "r") as f:
    PARSER_STOP_WORDS = json.load(f)

with open(PARSER_STOP_CHARS_FILENAME, "r") as f:
    UNESCAPED_STOP_CHARS = json.load(f)

# All the characters in this list should be escaped with an '\\'
CHARS_LIST_TO_BE_ESCAPED = [
    "^",
    "$",
    "?",
    "!",
    "+",
    "*",
    ".",
    "(",
    ")",
    "[",
    "]",
    "{",
    "}",
    "|",
    "\\",
]

PARSER_STOP_CHARS = [
    f"\\{char}" if char in CHARS_LIST_TO_BE_ESCAPED else char
    for char in UNESCAPED_STOP_CHARS
]
