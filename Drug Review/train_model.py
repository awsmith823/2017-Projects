"""
Read in training data, create pipeline, call fit method.
- Training data balanced w.r.t the target variable
- GridSearch code is commented out.
"""

import os
import pickle
import numpy as np
import pandas as pd

# scikit learn
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.base import TransformerMixin
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.model_selection import cross_val_score, GridSearchCV
from sklearn.metrics import classification_report, f1_score, accuracy_score

# constants
import settings
# UDFs
from utils import *

if __name__ == '__main__':

    # READ IN TRAINING DATA
    data = pd.read_csv(
        os.path.join(settings.DATA_DIR_DERIVED, settings.TRAIN_BALANCED),
        sep='\t',
    )

    # SPLIT (X, y)
    target = 'nps_rating'
    predictors = ['review']

    X = data[predictors].reset_index(drop=True)
    y = data[target].reset_index(drop=True)

    # MAKE PIPELINE
    document_feature = 'review'

    # Structural Pipeline (Review Length, Stop Words, All caps)
    structural_featurizer = FunctionFeaturizer(
        get_document_length,
        get_num_stop_words,
        count_uppercase_words,
    )

    structural_pipe = Pipeline(
        steps=[
            ('doc_selector', FeatureSelector(document_feature)),
            ('structural_features', structural_featurizer),
            ('minmax_scaler', MinMaxScaler(feature_range=(0, 1))),
        ]
    )

    # BOW transformer
    bow_pipe = Pipeline(
        steps=[
            ('doc_selector', FeatureSelector(document_feature)),
            ('clean_doc', FunctionFeaturizer(clean_document)),
            ('tfidf', TfidfVectorizer(min_df=0.01, max_df=0.99)),
        ]
    )

    # Combining piepline(s) into one horizontally
    # using FeatureUnion
    transformer_pipe = FeatureUnion(
        transformer_list=[
            ('structural_pipe', structural_pipe),
            ('bow_pipe', bow_pipe),
            # ('categorical_pipe', categorical_pipe),
        ]
    )

    # The transformer pipeline as a step in another
    # pipeline with an estimator as the final step
    full_pipeline = Pipeline(
        steps=[
            ('transformer_pipe', transformer_pipe),
            ('feature_selection', SelectKBest(score_func=chi2, k='all')),
            ('multinomialnb', MultinomialNB(alpha=0.25)),
        ]
    )

    # # GRID-SEARCH
    # parameters = {
    #     # 'transformer_pipe__bow_pipe__tfidf__min_df': (0.01, 0.025),
    #     # 'transformer_pipe__bow_pipe__tfidf__max_df': (0.99, 0.975),
    #     'feature_selection__k': (200, 300, 500, 'all'),
    #     'multinomialnb__alpha': (0.25, 1.0),
    # }

    # # GridSearch
    # grid_search = GridSearchCV(
    #     estimator=full_pipeline,
    #     param_grid=parameters,
    #     n_jobs=-1,
    #     verbose=1,
    #     cv=5
    # )

    # grid_search.fit(X, y)
    # # Print Grid Search Results
    # print('Baseline Accuracy: {:.2%}\n'.format(get_classification_baseline(y)))
    # # Best score is Mean cross-validated score of the best_estimator
    # print("Best score: %0.3f" % grid_search.best_score_)
    # print("Best parameters set:")

    # best_parameters = grid_search.best_estimator_.get_params()
    # for param_name in sorted(parameters.keys()):
    #     print("\t%s: %r" % (param_name, best_parameters[param_name]))

    # model = grid_search.best_estimator_

    # TRAIN MODEL
    model = full_pipeline.fit(X, y)

    # SAVE MODEL
    with open(settings.MODEL, 'wb') as file:
        pickle.dump(model, file)
