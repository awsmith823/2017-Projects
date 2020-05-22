"""
Read in validation data, call predict method.
- The model itself is not just the estimator, but also
includes other data transformations
"""

import os
import pickle
import numpy as np
import pandas as pd
from sklearn.metrics import classification_report, accuracy_score

# constants
import settings
# UDFs
from utils import *

if __name__ == '__main__':

    # READ IN MODEL & VALIDATION DATA

    # Load Model
    with open(settings.MODEL, 'rb') as file:
        model = pickle.load(file)

    # Read in Test Data
    data = pd.read_csv(
        os.path.join(settings.DATA_DIR_RAW, settings.TEST_RAW),
        sep='\t',
    )

    columns = [
        'drugName',
        'condition',
        'review',
        'rating'
    ]

    data = data[columns]

    # NPS Transformation
    data['nps_rating'] = data['rating'].apply(nps_transformation)

    # MAKE PREDICTIONS
    target = 'nps_rating'
    predictors = ['review']

    # predictions
    print('\n... predictions: {:,} ...\n'.format(data.shape[0]))
    data['y_pred'] = model.predict(data[predictors])
    # Accuracy
    baseline_acc = get_classification_baseline(target_data=data[target])
    model_acc = accuracy_score(y_true=data[target], y_pred=data['y_pred'])

    # print summary
    print('Baseline Accuracy: {:.2%}'.format(baseline_acc))
    print('Model Accuracy: {:.2%}\n'.format(model_acc))
    print(classification_report(y_true=data[target], y_pred=data['y_pred']))
