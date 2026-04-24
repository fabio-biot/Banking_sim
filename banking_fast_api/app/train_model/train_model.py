import numpy as np
from sklearn.ensemble import IsolationForest


def train_model(feature_list):
    X = np.array(feature_list)

    model = IsolationForest(contamination=0.05)
    model.fit(X)

    return model