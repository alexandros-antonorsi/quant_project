import os
import random
import string

import click
import numpy as np
import pandas as pd


class GBM:

    def __init__(
        self,
        start_date: str,
        end_date: str,
        init_price: float,
        mu: float,
        sigma: float,
        pareto: float,
        seed: int = 25
    ):
        self.start_date = start_date
        self.end_date = end_date
        self.init_price = init_price
        self.mu = mu
        self.sigma = sigma
        self.pareto = pareto

        self.rng = np.random.default_rng(seed)

    def _gen_ticker(self):
        return ''.join(self.rng.choice(list(string.ascii_uppercase), size=4))
    

    def _create_dataframe(self):
        date_range = pd.date_range(self.start_date, self.end_date, freq='B')
        df = pd.DataFrame(0, index=date_range, columns =['open', 'high', 'low', 'close', 'volume'])
        df.index.name = 'date'
        return df

    def _gbm_path(self, data):
        h = 1 / (252 * 4.0) #time step = 4 increments per business day in a year 

        increments = np.exp( (self.mu - self.sigma**2 / 2.0) * h + self.sigma * self.rng.normal(0, np.sqrt(h), size= 4*len(data)))

        return self.init_price * np.cumprod(increments)
    
    def _fill_data(self, data, path):
        days = np.stack(np.split(path, len(data)))
        data['open'] = days[:,0]
        data['close'] = days[:,-1]
        data['high'] = np.max(days, axis=1)
        data['low'] = np.min(days, axis=1)

        #simulate volume with pareto distr
        data['volume'] = np.astype(self.rng.pareto(self.pareto, size=len(data))*1e6, int)

    def _output_csv(self, ticker, data):
        data.to_csv(f'logs/{ticker}.csv', float_format='%.2f')


    def __call__(self):
        ticker = self._gen_ticker()
        data = self._create_dataframe()
        path = self._gbm_path(data)
        self._fill_data(data, path)
        self._output_csv(ticker, data)

        return ticker
        

@click.command()
@click.option('--num_stocks', 'num_stocks', default=1, help='number of stocks to simulate')
@click.option('--seed', 'seed', default=25, help='seed for rng')
@click.option('--start-date', 'start_date', default=None, help='starting date in YYYY-MM-DD format')
@click.option('--end-date', 'end_date', default=None, help='ending date in YYYY-MM-DD format')
@click.option('--init-price', 'init_price', default=100.0, help='initial stock price')
@click.option('--mu', 'mu', default=0.1, help='drift parameter for the GBM SDE')
@click.option('--sigma', 'sigma', default=0.3, help='volatility parameter for the GBM SDE')
@click.option('--pareto-shape', 'pareto_shape', default=1.5, help='shape of the Pareto distribution simulating the trading volume')
def cli(num_stocks, seed, start_date, end_date, init_price, mu, sigma, pareto_shape):

    gbm = GBM(start_date, end_date, init_price, mu, sigma, pareto_shape, seed)

    for i in range(num_stocks):
        print('Generated stock path for ' + gbm())



if __name__ == "__main__":
    cli()