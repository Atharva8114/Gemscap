import numpy as np
import statsmodels.api as sm


def ols_hedge_ratio(y, x):
    """
    Computes hedge ratio using OLS regression.
    y = dependent price series
    x = independent price series
    """
    if len(y) < 5:
        return None

    x = sm.add_constant(x)
    model = sm.OLS(y, x).fit()
    return model.params[1]
