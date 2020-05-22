import os
import numpy as np
import pandas as pd
import settings
from utils import get_balanced_sample_data, nps_transformation

if __name__ == '__main__':

    # Read in Raw Data
    data = pd.read_csv(
        os.path.join(settings.DATA_DIR_RAW, settings.TRAIN_RAW),
        sep='\t',
    )

    # columns of interest
    columns = [
        'drugName',
        'condition',
        'review',
        'rating'
    ]

    # Remove tiny reviews
    mask = data['review'].apply(lambda r: len(r.strip('\"')) < 3)
    data = data.loc[~mask, columns].reset_index(drop=True)

    # NPS transformation
    data['nps_rating'] = data['rating'].apply(nps_transformation)

    # Create balanced training data
    sample_data = get_balanced_sample_data(
        df=data,
        target_key='nps_rating',
        random_state=settings.RAND_STATE,
    )

    # save csv
    sample_data.to_csv(
        os.path.join(settings.DATA_DIR_DERIVED, settings.TRAIN_BALANCED),
        sep='\t',
        index=False,
    )
