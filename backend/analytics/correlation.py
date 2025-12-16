def rolling_correlation(series_a, series_b, window=100):
    if len(series_a) < window:
        return None

    return series_a[-window:].corr(series_b[-window:])
