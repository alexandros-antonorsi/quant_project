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
    errors = {method: np.empty(shape = num_iters) for method in methods}
    vr_factors = {method: np.empty(shape = num_iters) for method in methods}

    control_price = asian_geom_closed_form(S_0, r, sigma, T, K)



    for i in range(num_iters):


        price_plain, error_plain = plain_mc(S_0, r, sigma, T, path_counts[i], num_steps, asian_arith_call, K, rng)



        prices['plain'][i] = price_plain
        errors['plain'][i] = error_plain
        vr_factors['plain'][i] = 1.0



        price_anti, error_anti = anti_mc(S_0, r, sigma, T, path_counts[i], num_steps, asian_arith_call, K, rng)



        prices['anti'][i] = price_anti
        errors['anti'][i] = error_anti
        vr_factors['anti'][i] = (error_anti / error_plain)**2



        price_control, error_control = control_mc(S_0, r, sigma, T, path_counts[i], num_steps, asian_arith_call, K, asian_geom_call, control_price, rng)


        prices['control'][i] = price_control
        errors['control'][i] = error_control
        vr_factors['control'][i] = (error_control / error_plain)**2

    end = time.time()
    print(f'Completed simulations in {end - start:.2f} seconds.')

    plt.figure(figsize=(8,5))
    plt.plot(path_counts, prices['plain'], label='Plain MC')
    plt.plot(path_counts, prices['anti'], label='Antithetic variate', color='red')
    plt.plot(path_counts, prices['control'], label='Control variate', color='green')
    plt.legend()
    plt.xlabel("Number of paths")
    plt.ylabel("Stock price")
    plt.title(f"Simulated stock prices (Asian arithmetic call) (seed={seed})")
    plt.grid(True)
    plt.savefig("plots/asian_prices.png")

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8,6))
    ax1.fill_between(path_counts, y1=errors['plain'], y2= -1*errors['plain'], alpha=0.5, color='blue', label="Plain MC")
    ax2.fill_between(path_counts, y1=errors['anti'], y2= -1*errors['anti'], alpha=0.5, color='red', label="Antithetic variate")
    ax3.fill_between(path_counts, y1=errors['control'], y2= -1*errors['control'], alpha=0.5, color='green', label="Control variate")
    fig.legend()
    max_error = max(np.max(errors['plain'][1:]),  np.max(errors['anti'][1:]), np.max(errors['control'][1:]))
    ax1.set_ylim(max_error*-1, max_error)
    ax2.set_ylim(max_error*-1, max_error)
    ax3.set_ylim(max_error*-1, max_error)
    fig.suptitle(f"Width of confidence intervals vs. number of paths (seed={seed})")
    
    fig.supxlabel("Number of paths")
    fig.supylabel("CI widths")
    fig.savefig("plots/asian_errors.png")


    fig, (ax1, ax2) = plt.subplots(1,2, figsize=(10,3))
    n = np.arange(start=1, stop=num_iters+1)
    ax1.plot(path_counts, np.cumsum(vr_factors['anti']) / n, color='red')
    ax2.plot(path_counts, np.cumsum(vr_factors['control']) / n, color='green')
    ax1.grid(True)
    ax2.grid(True)
    ax1.set_title("Average VR of antithetic variate")
    ax2.set_title("Average VR of control variate")
    fig.supxlabel("Number of paths")
    fig.supylabel("Variance reduction")
    fig.tight_layout()
    fig.savefig("plots/asian_vr.png")
    fig.suptitle(f"Variance reduction factors (seed={seed})")
    
    print("Saved plots to plots/")
  
if __name__ == "__main__":
    run_demo()
