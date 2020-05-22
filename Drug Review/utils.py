import re
import html
import numpy as np
import pandas as pd
from sklearn.base import TransformerMixin
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from nltk.stem import PorterStemmer, WordNetLemmatizer
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()


def nps_transformation(rating):
    if rating > 8:
        return 1
    if rating < 7:
        return -1
    return 0


def get_document_length(document):
    '''
    Return number of words in a document
    '''
    return len(document.split())


def get_num_stop_words(document, stop_words=ENGLISH_STOP_WORDS):
    '''
    Count the number of stop words in 
    a document
    '''
    stop_words = list(stop_words)
    num_stop_words = len(
        [token for token in document.lower().split() if token in stop_words]
    )
    return num_stop_words


def count_uppercase_words(document, min_word_length=3):
    '''
    Returns count of words that are all
    CAP within a document
    '''
    mapped_tokens = map(
        lambda w: w.isupper() and len(w) >= min_word_length,
        document.split()
    )
    return sum(mapped_tokens)


def impute_item_in_document(item, repl, document):
    '''
    Replace noun within a document with a more
    general name / category e.g:

    Just purchased a MacBook ==> Just purchased a laptop
    '''
    regex = re.compile(r"(\b)(%s)(s?)(\b)" % item, flags=re.IGNORECASE)

    document = re.sub(
        pattern=regex,
        repl=repl,
        string=document
    )
    return document


def lemmatize_document(document):
    '''
    Lemmatization is the process of grouping
    together the different inflected forms of
    a word so they can be analysed as a single
    item. This function applies this method to 
    the word / tokens in a document

    e.g "corpora" ==> "corpus"

    Parameters
    ----------
    document (str)

    Output
    ------
    document (str): lemmatized document
    '''
    tokens = str(document).split()
    tokens = [
        lemmatizer.lemmatize(word) for
        word in tokens if word
    ]
    document = ' '.join(tokens)
    return document


def stem_document(document):
    '''
    Stemming is the process of producing 
    morphological variants of a root/base 
    word. This function stems every word / 
    token in a document

    e.g "I like playing" ==> "i like play"

    Parameters
    ----------
    document (str): document

    Output
    ------
    document (str): stemmed document
    '''
    tokens = str(document).split()
    tokens = [
        stemmer.stem(word) for
        word in tokens if word
    ]
    document = " ".join(tokens)
    return document


def remove_non_characters(string):
    '''
    Remove punctuation from specified string
    '''
    string = ' '.join(
        re.sub(r'[^a-zA-Z ]', ' ', re.escape(string)).split()
    )
    return string


def clean_document(document, lemmatize=False, default="empty"):
    '''
    Function cleans document. Removes html, times,
    special characters, emails.

    If no words remain after cleaning return default
    '''
    document = str(document)
    # unescape html: e.g {'&lt;html&gt;' : '<html>'}
    document = html.unescape(document)

    # replace URLs
    document = re.sub(r"http\S+", "hyperlink", document)
    # replace email addresses
    document = re.sub(r"\S*@\S*", "email", document)
    # replace date
    document = re.sub(r"(\d+)/(\d+)/(\d+)", "date", document)
    document = re.sub(r"(\d+)-(\d+)-(\d+)", "date", document)
    # replace times
    document = re.sub(
        r"[0-2]?[0-9]:[0-6][0-9](\s)*(pm)?(am)?", "time",
        document, flags=re.IGNORECASE
    )
    # replace hypens with space
    document = re.sub(r"-", " ", document)
    # remove special characters, numbers, punctuations
    document = re.sub("[^a-zA-Z ]", " ", document)
    # lower case, strip, & remove small words
    document = ' '.join(
        filter(
            lambda w: len(w) > 3, document.lower().split()
        )
    )

    if document:
        if lemmatize:
            document = lemmatize_document(document)
        return document
    return default


def get_balanced_sample_data(df, target_key, random_state=None):
    '''
    Parameters
    ----------
    df: data frame to sample from
    target_key: Column to balance against
    random_state: Set random seed

    Output
    ------
    data: Balanced df w.r.t target_key
    '''
    # counts for each class
    class_value_counts = df[target_key].value_counts()
    # get smallest count
    sample_counts = class_value_counts.min()

    # iterate through each class
    data = []
    for class_value in class_value_counts.index:
        # sample the data
        sample_data = df[
            df[target_key] == class_value
        ].sample(
            n=sample_counts,
            replace=False,
            random_state=random_state,
        ).reset_index(drop=True)

        # append sample to data list
        data.append(sample_data)

    # concatenate all samples & shuffle data
    data = pd.concat(data, axis=0)\
        .sample(frac=1, random_state=random_state)\
        .reset_index(drop=True)

    return data


def get_classification_baseline(target_data):
    '''
    Parameters
    ----------
    target_data: iterable of classification
    target feature data

    Output
    ------
    baseline = summation([P(class i) * P(guess class i)])
    '''
    target_data = pd.Series(target_data)
    baseline = target_data\
        .value_counts(normalize=True)\
        .apply(lambda x: x**2).sum()
    return round(baseline, 3)


class FunctionFeaturizer(TransformerMixin):
    def __init__(self, *featurizers):
        self.featurizers = featurizers

    def fit(self, X, y=None):
        """All SciKit-Learn compatible transformers and classifiers have the
        same interface. `fit` always returns the same object."""
        return self

    def transform(self, X):
        """Given a list of original data, return a list of feature vectors."""
        fvs = []
        if len(self.featurizers) == 1:
            for datum in X:
                fvs.append(self.featurizers[0](datum))
        else:
            for datum in X:
                fv = [f(datum) for f in self.featurizers]
                fvs.append(fv)
        return np.array(fvs)

    
#Custom Transformer that extracts columns passed as argument to its constructor 
class FeatureSelector(TransformerMixin):
    #Class Constructor 
    def __init__( self, feature_names ):
        self._feature_names = feature_names 
    
    #Return self nothing else to do here    
    def fit( self, X, y = None ):
        return self 
    
    #Method that describes what we need this transformer to do
    def transform( self, X, y = None ):
        return X[ self._feature_names ]
