# -*- coding: utf-8 -*-

import re
from typing import Dict, List, Union

from settings import PARSER_STOP_CHARS, PARSER_STOP_WORDS


class ParsedData:
    def __init__(self, page_url: str, title: str, content: str, urls: List[str]):
        self._page_url = page_url
        self._title = title
        self._content = content
        self._urls = urls
        self._occurences = None  # Lazy calculation

    @property
    def urls(self):
        return self._urls

    @staticmethod
    def _calculate_words_occurences(content: str) -> Dict[str, int]:
        occurences = {}
        for word in content.split(" "):
            occurences[word] = occurences.get(word, 0) + 1
        return occurences

    def to_dict(self) -> Dict:
        if not self._occurences:
            self._occurences = self._calculate_words_occurences(self._content)
        return {
            "_id": self._page_url,
            "title": self._title,
            "content": self._content,
            "content_occurences": self._occurences,
        }


class Parser:
    @classmethod
    def parse_html(cls, page_url: str, html_content: str) -> ParsedData:
        html_content = cls._clean_javascript_code_from_html(html_content)
        page_title: Union[str, None] = cls._get_html_title(html_content)
        if page_title is not None:
            page_title = cls._spacing_strip(page_title)
        page_urls: List[str] = cls._get_page_urls_list(html_content)
        clean_content = cls._extract_cleaned_text_from_html(html_content)
        return ParsedData(page_url, page_title, clean_content, page_urls)

    @staticmethod
    def _clean_javascript_code_from_html(html_content: str) -> str:
        return re.sub(
            r"<script(.)*>[^<]*</script>",
            r"",
            html_content,
            flags=re.IGNORECASE | re.MULTILINE,
        )

    @staticmethod
    def _get_html_title(html_content: str) -> Union[str, None]:
        html_titles = re.findall(r"<title>[^<]*</title>", html_content, re.IGNORECASE)
        if not html_titles:
            return None

        text_title = re.sub(
            r"<title>([^<]*)</title>", r"\1", html_titles[0], re.IGNORECASE
        )
        return text_title.lower()

    @staticmethod
    def _get_page_urls_list(html_content: str) -> List[str]:
        html_anchors = re.findall(
            'a href="((http|/)[^"]*)"', html_content, flags=re.IGNORECASE | re.DOTALL
        )
        return [
            re.sub('a href="((http|/)[^"]*)"', r"\1", anchor[0], re.IGNORECASE)
            for anchor in html_anchors
        ]

    @staticmethod
    def _remove_html_tags(html_content: str) -> str:
        return re.sub(r"<[^>]*>", r"", html_content, flags=re.IGNORECASE | re.MULTILINE)

    @staticmethod
    def _remove_useless_numbers(text_content: str) -> str:
        # Removing all numbers, except years
        return re.sub(
            r"(\s)+(?!((19[0-9]{2}|20[0-9]{2})))([0-9]+)(\s)+",
            r" ",
            text_content,
            flags=re.IGNORECASE | re.MULTILINE,
        )

    @staticmethod
    def _remove_stop_chars(text_content: str) -> str:
        stop_chars_regex = f'(\s)*({"|".join(PARSER_STOP_CHARS)})(\s)*'
        return re.sub(
            stop_chars_regex, " ", text_content, flags=re.IGNORECASE | re.MULTILINE
        )

    @staticmethod
    def _filter_stop_words(text_content: str) -> str:
        stop_words_regex = f'(\s)+({"|".join(PARSER_STOP_WORDS)})(\s)+'
        return re.sub(
            stop_words_regex, " ", text_content, flags=re.IGNORECASE | re.MULTILINE
        )

    @staticmethod
    def _spacing_strip(text_content: str) -> str:
        """ Replaces multiple spaces by only one """
        return re.sub("(\s)+", " ", text_content)

    @classmethod
    def _extract_cleaned_text_from_html(cls, html_content: str) -> str:
        text = cls._remove_html_tags(html_content)
        text = text.lower()
        text = cls._remove_useless_numbers(text)
        text = cls._remove_stop_chars(text)
        text = cls._filter_stop_words(text)
        text = cls._spacing_strip(text)
        return text
