from main import _calculate_result_score_for_given_query


def test_init():
    # Just to trigger travis tests
    query_words = ["first", "second"]
    result_element = {
        "_id": "https://first-word.org/",
        "title": "this is my first and second words",
        "content": "this is the second text for the day",
        "content_occurences": {"this": 1, "is": 1, "second": 1, "text": 1},
    }
    assert _calculate_result_score_for_given_query(result_element, query_words) == 71
