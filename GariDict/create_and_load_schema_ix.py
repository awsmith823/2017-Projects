# import packages
import os
import pandas as pd
# whoosh
from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
# constants
import settings
from utils import process_word_item, split_text, process_search_term

if __name__ == '__main__':
    # read in data
    data = pd.read_csv(
        os.path.join(settings.DIR_DATA, settings.DATA_FNAME_SEP_TUP[0]),
        sep=settings.DATA_FNAME_SEP_TUP[1],
    )

    # define schema
    schema = Schema(
        english=TEXT(stored=False, sortable=True),
        garifuna=TEXT(stored=False),
        spanish=TEXT(stored=False),
        output=TEXT(stored=True),
    )

    # create index
    ix = create_in(dirname=settings.DIR_SCHEMA, schema=schema)

    # open index writer
    writer = ix.writer()
    # write to schema index
    for idx, row in enumerate(data.values):
        writer.add_document(
            english=process_word_item(row[0]),
            garifuna=process_word_item(row[1]),
            spanish=process_word_item(row[2]),
            output=u" | ".join(row)
        )
    # commit
    writer.commit()
