import string

import numpy as np

class GBM:

    def __init__(
        self,
        num_steps: int = 52,
        num_paths: int = 10**5,
        init_price: float = 100.0 , 
        T: float = 1.0, 
        r: float = 0.03,
        sigma: float = 0.2,
        rng: np.random.Generator = np.random.default_rng(), #optional rng to control GBM path
        #if true, generates an additional dataframe of the corresponding antithetic paths for antithetic variate calculations
        anti: bool = False  
    ):
        self.num_steps = num_steps
        self.num_paths = num_paths
        self.init_price = init_price
        self.T = T
        self.r = r
        self.sigma = sigma
        self.rng = rng
        self.anti = anti

        self.data = None
        self.ticker = None
        self.anti_data = None

        self._gen_ticker()
        self._gen_data()

    def _gen_ticker(self):
        self.ticker= ''.join(self.rng.choice(list(string.ascii_uppercase), size=4))
    

    def _gen_data(self):
        dt = self.T / self.num_steps 
        Z = self.rng.normal(0, np.sqrt(dt), size= (self.num_paths, self.num_steps))

        increments = np.exp((self.r - self.sigma**2 / 2) * dt + self.sigma * Z)
        self.data = self.init_price * np.cumprod(increments, axis=1)

        if self.anti:
            anti_increments = np.exp((self.r - self.sigma**2 / 2) * dt + self.sigma * (-1 * Z))
            self.anti_data = self.init_price * np.cumprod(anti_increments, axis=1)


    def get_data(self):
        if self.anti:
            return self.data, self.anti_data

        return self.data
        
