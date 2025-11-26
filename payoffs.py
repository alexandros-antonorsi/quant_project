import numpy as np
from scipy.stats import norm

def euro_call(path: np.array, K: float):
    return max(path[-1] - K, 0.0)

def asian_arith_call(path: np.array, K: float):
    return max(np.mean(path) - K, 0.0)

def asian_geom_call(path: np.array, K: float):
    return max(np.exp(np.mean(np.log(path))) - K, 0.0)

def euro_call_closed_form(S_0: float, r: float, sigma: float, T: float, K: float):
    d_1 = (np.log(S_0/K) + (r + 0.5 * sigma**2) * T ) / (sigma * np.sqrt(T))
    d_2 = (np.log(S_0/K) + (r - 0.5 * sigma**2) * T ) / (sigma * np.sqrt(T))
    
    return S_0 * norm.cdf(d_1) - K * np.exp(-r * T) * norm.cdf(d_2)


def asian_geom_closed_form(num_steps: int, S_0: float, r: float, sigma: float, T: float, K: float):
    sigma_G = sigma / np.sqrt(3)
    b = 0.5 * (r - 0.5 * sigma_G**2)
    d1 = (np.log(S_0/K) + T * (b + 0.5 * sigma_G**2)) / (sigma_G * np.sqrt(T))
    d2 = d1 - sigma_G * np.sqrt(T)

    return S_0 * np.exp((b - r) * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)