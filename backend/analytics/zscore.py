import numpy as np


def zscore(series, window=100):
    if len(series) < window:
        return None

    recent = series[-window:]
    mean = recent.mean()
    std = recent.std()

    if std == 0:
        return 0.0

    return (recent.iloc[-1] - mean) / std
