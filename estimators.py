import numpy as np
from gbm import GBM

def plain_mc(
    S_0, r, sigma, T, #hyperparameters
    num_paths, num_steps, #number of simulations and steps per simulation
    payoff_func, K, #payoff type and strike price
    rng: np.random.Generator = np.random.default_rng() #optional rng to control GBM path
):
    discounted_payoffs = np.empty(shape = num_paths)
    gbm = GBM(num_steps, num_paths, S_0, T, r, sigma, rng)
    data = gbm.get_data()
    for i in range(num_paths):
        payoff = payoff_func(data[i], K)
        discounted_payoffs[i] = np.exp(-r * T) * payoff 

    mean = discounted_payoffs.mean()
    std = discounted_payoffs.std(ddof=1)
    error = 1.96 * std / np.sqrt(num_paths)
    ci = (mean - error, mean + error)

    return mean, ci


def anti_mc(
    S_0, r, sigma, T, #hyperparameters
    num_paths, num_steps, #number of simulations and steps per simulation
    payoff_func, K, #payoff type and strike price
    rng: np.random.Generator = np.random.default_rng() #optional rng to control GBM path
):
    discounted_payoffs = np.empty(shape = num_paths)
    gbm = GBM(num_steps, num_paths, S_0, T, r, sigma, rng, anti=True)
    data, anti_data = gbm.get_data()

    for i in range(num_paths):
        payoff = payoff_func(data[i], K)
        anti_payoff = payoff_func(anti_data[i], K)

        avg_payoff = 0.5 * (payoff + anti_payoff)
        discounted_payoffs[i] = np.exp(-r * T) * avg_payoff

    mean = discounted_payoffs.mean()
    std = discounted_payoffs.std(ddof=1)
    error = 1.96 * std / np.sqrt(num_paths)
    ci = (mean - error, mean + error)

    return mean, ci

def control_mc(
    S_0, r, sigma, T, #hyperparameters
    num_paths, num_steps, #number of simulations and steps per simulation
    payoff_func, K, #payoff type and strike price
    control_payoff_func, control_price, #payoff function and known price to control against
    rng: np.random.Generator = np.random.default_rng() #optional rng to control GBM path 
):
    discounted_X = np.empty(shape = num_paths)
    discounted_Y = np.empty(shape = num_paths)
    gbm = GBM(num_steps, num_paths, S_0, T, r, sigma, rng)
    data = gbm.get_data()

    for i in range(num_paths):
        path = data[i]
        X_i = payoff_func(path, K)
        Y_i = control_payoff_func(path, K)

        discounted_X[i] = np.exp(-r * T) * X_i 
        discounted_Y[i] = np.exp(-r * T) * Y_i

    

    cov = np.cov(discounted_X, discounted_Y, ddof=1)
    cov_XY = cov[0,1] 
    var_Y = cov[1,1]

    b = cov_XY / var_Y
    Z = discounted_X - b * (discounted_Y - control_price)


    mean = Z.mean()
    std = Z.std(ddof = 1)
    error = 1.96 * std / np.sqrt(num_paths)
    ci = (mean - error, mean + error)

    return mean, ci


