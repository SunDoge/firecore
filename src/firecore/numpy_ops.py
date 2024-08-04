import numpy as np


def fast_sigmoid(x: np.ndarray):
    return 0.5 + 0.5 * np.tanh(0.5 * x)


def sigmoid(x: np.ndarray):
    return 1.0 / (1.0 + np.exp(-x))
