import matplotlib.pyplot as plt
import pandas as pd
import click


@click.command()
@click.option("--ticker", 'ticker', default = None, help = 'ticker symbol to plot results of')
def plot_log(ticker):
    df = pd.read_csv(f'logs/{ticker}.csv').set_index('date')
    df[['open', 'high', 'low', 'close']].plot()
    plt.show()
    


if __name__ == "__main__":
    plot_log()