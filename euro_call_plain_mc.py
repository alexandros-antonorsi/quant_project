import time

import click
import numpy as np
import matplotlib.pyplot as plt

from estimators import plain_mc
from payoffs import euro_call, euro_call_closed_form


@click.command()
@click.option('--num-steps', 'num_steps', default=52, help='number of steps for each GBM path simulation')
@click.option('--num-paths', 'num_paths', default=10**5, help='max number of paths to simulate')
@click.option('--num-iters', 'num_iters', default=100, help='amount of experiments to run. each experiment simulates num-paths/num-iters more paths than the last')
@click.option('--S_0', 'S_0', default=100.0, help='initial stock price')
@click.option('--T', 'T', default=1.0, help='number of years to simulate')
@click.option('--r', 'r', default=0.03, help='risk-free rate')
@click.option('--sigma', 'sigma', default=0.2, help='volatility')
@click.option('--K', 'K', default=100.0, help='strike price')
@click.option('--seed', 'seed', default=None, help='optional seed for rng')
def run_demo(num_steps, num_paths, num_iters, S_0, T, r, sigma, K, seed):
    start = time.time()
    path_counts = np.arange(start = num_paths//num_iters, stop = num_paths+1, step = num_paths//num_iters)
    if seed is not None:
        rng = np.random.default_rng(int(seed))
    else:
        rng = np.random.default_rng()

    prices = np.empty(shape = num_iters)
    cis = np.empty(shape = (num_iters,2))

    for i in range(num_iters):
        price, ci = plain_mc(S_0, r, sigma, T, path_counts[i], num_steps, euro_call, K, rng)
        prices[i] = price
        cis[i,0] = ci[0]
        cis[i,1] = ci[1]

    closed_form_price = euro_call_closed_form(S_0, r, sigma, T, K)

    end = time.time()
    print(f'Completed simulation in {end - start:.2f} seconds.')

    plt.figure()
    plt.plot(path_counts, prices, marker='o', label='Plain MC estimates')
    plt.axhline(closed_form_price, linestyle='--', label='Closed form price')
    plt.title("Plain MC estimates for European call prices")
    plt.legend()
    plt.grid(True)
    plt.show()




if __name__ == "__main__":
    
    run_demo()
   



