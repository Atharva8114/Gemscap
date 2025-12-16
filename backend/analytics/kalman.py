import numpy as np


def kalman_hedge_ratio(y, x):
    """
    Computes dynamic hedge ratio using a 1D Kalman Filter.
    y = dependent series (BTC)
    x = independent series (ETH)
    Returns latest hedge ratio.
    """

    if len(y) < 10:
        return None

    # Convert to numpy
    y = np.array(y)
    x = np.array(x)

    # Kalman parameters
    delta = 1e-5
    R = 0.001

    # Initial state
    beta = 0.0
    P = 1.0

    for t in range(len(y)):
        # Predict
        P = P + delta

        # Observation
        if x[t] == 0:
            continue

        # Kalman gain
        K = P * x[t] / (x[t] * x[t] * P + R)

        # Update state
        beta = beta + K * (y[t] - beta * x[t])

        # Update uncertainty
        P = P - K * x[t] * P

    return float(beta)
