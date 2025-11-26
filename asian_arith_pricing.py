import time
import numpy as np
import matplotlib.pyplot as plt
import click

from estimators import plain_mc, anti_mc, control_mc
from payoffs import asian_arith_call, asian_geom_call, asian_geom_closed_form

@click.command()
@click.option('--num-steps', 'num_steps', default=52, help='number of steps for each GBM path simulation')
@click.option('--num-paths', 'num_paths', default=10**4, help='max number of paths to simulate')
@click.option('--num-iters', 'num_iters', default=100, help='amount of experiments to run. each experiment simulates num-paths/num-iters more paths than the last')
@click.option('--S_0', 'S_0', default=100.0, help='initial stock price')
@click.option('--T', 'T', default=1.0, help='number of years to simulate')
@click.option('--r', 'r', default=0.08, help='risk-free rate')
@click.option('--sigma', 'sigma', default=0.3, help='volatility')
@click.option('--K', 'K', default=100.0, help='strike price')
@click.option('--seed', 'seed', default=None, help='optional seed for rng')
def run_demo(num_steps, num_paths, num_iters, S_0, T, r, sigma, K, seed):
    start = time.time()
    path_counts = np.arange(start = num_paths//num_iters, stop = num_paths+1, step = num_paths//num_iters)
    if seed is not None:
        rng = np.random.default_rng(int(seed))
    else:
        rng = np.random.default_rng()

    methods = ['plain', 'anti', 'control']
    prices = {method: np.empty(shape = num_iters) for method in methods}
    cis = {method: np.empty(shape = (num_iters,2)) for method in methods}
    runtimes = {method: np.empty(shape = num_iters) for method in methods}
    vr_factors = {method: np.empty(shape = num_iters) for method in methods}

    control_price = asian_geom_closed_form(num_steps, S_0, r, sigma, T, K)

    plain_time = 0
    anti_time = 0 
    control_time = 0

    for i in range(num_iters):

        t0 = time.time()
        price_plain, ci_plain = plain_mc(S_0, r, sigma, T, path_counts[i], num_steps, asian_arith_call, K, rng)
        t1 = time.time()
        plain_time = plain_time + t1 - t0

        prices['plain'][i] = price_plain
        cis['plain'][i,0] = ci_plain[0]
        cis['plain'][i,1] = ci_plain[1]
        runtimes['plain'][i] = plain_time
        vr_factors['plain'][i] = 1.0


        t0 = time.time()
        price_anti, ci_anti = anti_mc(S_0, r, sigma, T, path_counts[i], num_steps, asian_arith_call, K, rng)
        t1 = time.time()
        anti_time = anti_time + t1 - t0

        prices['anti'][i] = price_anti
        cis['anti'][i,0] = ci_anti[0]
        cis['anti'][i,1] = ci_anti[1]
        runtimes['anti'][i] = anti_time
        vr_factors['anti'][i] = ((ci_anti[1]-ci_anti[0]) / (ci_plain[1]-ci_plain[0]))**2


        t0 = time.time()
        price_control, ci_control = control_mc(S_0, r, sigma, T, path_counts[i], num_steps, asian_arith_call, K, asian_geom_call, control_price, rng)
        t1 = time.time()
        control_time = control_time + t1 - t0

        prices['control'][i] = price_control
        cis['control'][i,0] = ci_control[0]
        cis['control'][i,1] = ci_control[1]
        runtimes['control'][i] = control_time
        vr_factors['control'][i] = ((ci_control[1]-ci_control[0]) / (ci_plain[1]-ci_plain[0]))**2


    plt.figure()
    plt.plot(runtimes['plain'], prices['plain'], label='plain MC price')
    plt.fill_between(runtimes['plain'], y1=cis['plain'][:,0], y2=cis['plain'][:,1], label='plain MC CIs', alpha=.15)
    plt.plot(runtimes['anti'], prices['anti'], label='anti MC price', color='red')
    plt.fill_between(runtimes['anti'], y1=cis['anti'][:,0], y2=cis['anti'][:,1], label='anti MC CIs', color='red', alpha=.15)
    plt.plot(runtimes['control'], prices['control'], label='control MC price', color='green')
    plt.fill_between(runtimes['control'], y1=cis['control'][:,0], y2=cis['control'][:,1], label='control MC CIs', color='green', alpha=.15)
    plt.legend()
    plt.xlabel("Runtime (seconds)")
    plt.ylabel("Price")


    plt.figure()
    #put each of these in their own subplot but same figure. have them stacked vertically
    plt.plot(path_counts, vr_factors['anti'], label='anti VR factors', color='red')
    plt.plot(path_counts, vr_factors['control'], label='control VR factors', color='green')
    plt.legend()
    plt.grid(True)

    end = time.time()
    print(f'Completed simulations in {end - start:.2f} seconds.')

    plt.show()

if __name__ == "__main__":
    run_demo()
