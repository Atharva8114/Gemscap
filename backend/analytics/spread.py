import numpy as np


def compute_spread(price_a, price_b, hedge_ratio):
    if hedge_ratio is None:
        return None

    return price_a - hedge_ratio * price_b
