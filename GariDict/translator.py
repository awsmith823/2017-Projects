# import packages
import pandas as pd
import sys
import argparse
# whoosh
from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
# constansts / UDFs
import settings
from utils import split_text, process_search_term, print_output

"""
Run in the terminal as example:
python3 translator.py --t "child" --lang "english"
"""


def load_schema_index(dirname=settings.DIR_SCHEMA):
    """
    Parameters
    ----------
    - dirname (str)
    """
    # open search index
    schema_index = open_dir(dirname)
    return schema_index


def translate_term(
        search_term,
        language,
        schema_index=load_schema_index(),
        params=settings.search_params,
):
    """
    Parameters
    ----------
    - search_term (str): 
    - language (str): "english" | "garifuna" | "spanish"
    - schema_index:
    - params (dict):

    Output
    ------
    - translated results | suggestions | None
    """

    # pre-process
    language = language.lower()
    search_term = process_search_term(search_term)
    len_term = len(search_term)

    # instantiate parser
    parser = QueryParser(fieldname=language, schema=schema_index.schema)
    query = parser.parse(search_term)

    # search
    with schema_index.searcher() as searcher:

        suggested = searcher.suggest(
            fieldname=language,
            text=search_term,
            limit=params["limit"],
            maxdist=params["maxdist"],
            prefix=min(len_term, params["prefix"]),
        )

        if suggested and (search_term not in suggested):
            return {"search_term": search_term, "suggested": suggested}
        else:
            results = searcher.search(query, limit=5)
            if results:
                # format results
                results = pd.DataFrame(
                    data=[
                        split_text(results[r]["output"], sep="|")
                        for r in range(len(results))
                    ],
                    columns=params["languages"]
                )
                return {"search_term": search_term, "results": results}
            else:
                return {"search_term": search_term}


parser = argparse.ArgumentParser()

if __name__ == '__main__':
    parser.add_argument(
        "--term",
        type=str,
        help="Search Term",
        default="child"
    )

    parser.add_argument(
        "--lang",
        type=str,
        help="Language",
        default="english"
    )

    args = parser.parse_args()

    supported_langs = [lang.lower() for lang in settings.LANG_LIST]

    if args.lang not in supported_langs:
        sys.exit("supported language(s): {}".format(supported_langs))

    # search & translate
    output = translate_term(
        search_term=args.term,
        language=args.lang,
    )

    print_output(output)
