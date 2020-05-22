import os
import numpy as np
import pandas as pd
# constants
import settings
# UDFs
from utils import remove_non_characters

if __name__ == '__main__':

    # Read in Raw Data
    data = pd.read_csv(
        os.path.join(settings.DATA_DIR_RAW, settings.TRAIN_RAW),
        sep='\t',
    )

    column = 'drugName'

    # clean
    data[column] = data[column].apply(remove_non_characters)
    # unique, sorted list of items
    items = sorted(data[column].unique())
    # write data to .txt
    FNAME = os.path.join(settings.DATA_DIR_DERIVED, settings.DRUGS)

    with open(FNAME, 'w') as f:
        for list_item in items:
            f.write('%s\n' % list_item)
