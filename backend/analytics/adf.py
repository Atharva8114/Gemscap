from statsmodels.tsa.stattools import adfuller


def adf_test(series):
    if len(series) < 20:
        return None

    result = adfuller(series)
    return {
        "adf_stat": result[0],
        "p_value": result[1],
        "is_stationary": result[1] < 0.05
    }
