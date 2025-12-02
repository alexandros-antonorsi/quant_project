import numpy as np
from gbm import GBM

def plain_mc(
    S_0, r, sigma, T, #hyperparameters
    num_paths, num_steps, #number of simulations and steps per simulation
    payoff_func, K, #payoff type and strike price
    rng: np.random.Generator = np.random.default_rng() #optional rng to control GBM path
):
    gbm = GBM(num_steps, num_paths, S_0, T, r, sigma, rng)
    data = gbm.get_data()

    discounted_payoffs = np.exp(-r * T) * payoff_func(data, K) 

    mean = discounted_payoffs.mean()
    std = discounted_payoffs.std(ddof=1)
    error = 1.96 * std / np.sqrt(num_paths)

    return mean, error


def anti_mc(
    S_0, r, sigma, T, #hyperparameters
    num_paths, num_steps, #number of simulations and steps per simulation
    payoff_func, K, #payoff type and strike price
    rng: np.random.Generator = np.random.default_rng() #optional rng to control GBM path
):
    gbm = GBM(num_steps, num_paths, S_0, T, r, sigma, rng, anti=True)
    data, anti_data = gbm.get_data()

    discounted_payoffs = np.exp(-r * T) * 0.5 * (payoff_func(data, K) + payoff_func(anti_data, K))

    mean = discounted_payoffs.mean()
    std = discounted_payoffs.std(ddof=1)
    error = 1.96 * std / np.sqrt(num_paths)

    return mean, error

def control_mc(
    S_0, r, sigma, T, #hyperparameters
    num_paths, num_steps, #number of simulations and steps per simulation
    payoff_func, K, #payoff type and strike price
    control_payoff_func, control_price, #payoff function and known price to control against
    rng: np.random.Generator = np.random.default_rng() #optional rng to control GBM path 
):
    gbm = GBM(num_steps, num_paths, S_0, T, r, sigma, rng)
    data = gbm.get_data()

    discounted_X = np.exp(-r * T) * payoff_func(data, K)
    discounted_Y = np.exp(-r * T) * control_payoff_func(data, K)
    

    cov = np.cov(discounted_X, discounted_Y, ddof=1)
    cov_XY = cov[0,1] 
    var_Y = cov[1,1]

    b = cov_XY / var_Y
    Z = discounted_X - b * (discounted_Y - control_price)


    mean = Z.mean()
    std = Z.std(ddof = 1)
    error = 1.96 * std / np.sqrt(num_paths)

    return mean, error


