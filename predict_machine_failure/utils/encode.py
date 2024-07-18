from typing import Dict, List, Optional, Tuple

from pandas import DataFrame
import scipy
from sklearn.feature_extraction import DictVectorizer


def vectorize_features(training_set, validation_set):
    dv = DictVectorizer()
    train_dicts = training_set.to_dict(orient="records")
    X_train = dv.fit_transform(train_dicts)

    val_dicts = validation_set[training_set.columns].to_dict(orient="records")
    X_val = dv.transform(val_dicts)

    return X_train, X_val, dv
