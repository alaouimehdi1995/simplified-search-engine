#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from typing import Dict, List

from database_manager import DatabaseManager
from settings import DISPLAYED_DESCRIPTION_LENGTH

logger = logging.getLogger(__name__)


def _calculate_result_score_for_given_query(
    result_element: Dict, query_words: List[str]
) -> int:
    """
    `result_element` structure:
    {
        "_id": "https://example.com/",
        "title": "page title here",
        "content": "cleaned page text here",
        "content_occurences": {"word1": 3, "word2": 5,...}
    }
    """
    matches = {
        "url": 0,
        "title": 0,
        "text_content": 0,
    }

    for query_word in query_words:
        if query_word in result_element["_id"].lower():
            matches["url"] += 1
        if (
            result_element["title"] is not None
            and query_word in result_element["title"].lower()
        ):
            matches["title"] += 1
        matches["text_content"] += result_element["content_occurences"].get(
            query_word, 0
        )

    final_score = 10 * (5 * matches["url"] + matches["title"]) + matches["text_content"]

    return final_score


def _get_query_results(query: str) -> List[Dict]:
    query_words = query.split(" ")
    db_manager = DatabaseManager()
    query_results = db_manager.find_text(query)
    # TODO: using generator instead ?
    scored_results = [
        {
            **result,
            "score": _calculate_result_score_for_given_query(result, query_words),
        }
        for result in query_results
    ]
    return sorted(scored_results, key=lambda x: x["score"], reverse=True)


if __name__ == "__main__":
    while True:
        print("Enter your query (empty query to exit):")
        query = str(input()).lower()
        if not query:
            break
        results = _get_query_results(query)

        if not results:
            print("No results found for your query")
        else:
            # TODO: add pagination
            for i, result in enumerate(results):
                title = result["title"] if result["title"] is not None else ""
                url = result["_id"]
                score = result["score"]
                content = result["content"]
                desc = (
                    content
                    if len(content) <= DISPLAYED_DESCRIPTION_LENGTH
                    else f"{content[:DISPLAYED_DESCRIPTION_LENGTH - 3]}..."
                )
                print(f"\n== {i + 1} - {title} {url}\n\t {desc} ({score})\n")
