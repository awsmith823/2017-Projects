import os
import re
import pandas as pd
from unidecode import unidecode
# constants
import settings


def split_text(text, sep="|"):
    """
    Parameters
    ----------
    - text (str): e.g 'chapel, n | ligilisi (li-gi-li-si), n | capilla, n'
    - sep (str): Delimeter to separate text

    Output
    ------
    - tokens (list): e.g ['chapel, n', 'ligilisi (li-gi-li-si), n', 'capilla, n']
    """
    tokens = [
        t.strip() for t in text.split(sep)
    ]
    return tokens


def process_word_item(word_item):
    """
    Parameters
    ----------
    - word_item (str): word / term + (phonetic?) + part of speech
        e.g 'lémeri gumuleli (lé-me-ri- gu-mu-le-li), n'

    Output
    ------
    - word: Extracted word (decoded)
        e.g 'lemeri gumuleli'
    """
    word = re.sub(r"(\(.+\))", "", string=word_item).split(",")[0].strip()
    word = unidecode(word)
    return word


def process_search_term(search_term):
    """
    Parameters
    ----------
    - search_term (str)

    Output
    ------
    - processed search_term (str)
    """
    # decode
    search_term = unidecode(search_term)
    # remove non-alpha
    search_term = re.sub(r"[^a-zA-Z\s]", "", search_term)
    # strip
    search_term = search_term.strip()
    return search_term


def print_suggested(suggested_output):
    """
    Parameters
    ----------
    - suggested_output (dict): {"search_term": "...", "suggested": [...]}
    """
    print(
        "No search results found for: '{}'"
        .format(suggested_output["search_term"])
    )
    print("\nTry:")
    for w in suggested_output["suggested"]:
        print("-", "'{}'".format(w))


def print_results(results_output):
    """
    Parameters
    ----------
    - results_output (dict): {"search_term": "...", "results": DataFrame}
    """
    print(results_output["results"])


def print_output(output):
    """
    Parameters
    ----------
    - output (dict): 
        {"search_term": "...", "results": DataFrame?, "suggested": [...]?}
    """
    if "results" in output:
        print_results(results_output=output)
    elif "suggested" in output:
        print_suggested(suggested_output=output)
    else:
        print(
            "No search results found for:",
            output["search_term"],
        )
