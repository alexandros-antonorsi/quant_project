# Monte Carlo Exotic Option Pricing with Variance Reduction

This project implements a Monte Carlo simulation engine for pricing Asian arithmetic-average call options under the Black–Scholes model. The goal is to estimate these option prices using simulated Geometric Brownian Motion stock-price paths and demonstrate how Antithetic and Control Variate techniques can dramatically improve accuracy for the same computational cost.

---

## Features

- Geometric Brownian Motion (GBM) price path simulator class
- Script for plain Monte Carlo (MC) pricing of European vanilla calls (for the purpose of validating GBM and MC simulations by comparing to Black-Scholes closed form)
- Benchmark script simulating plain MC against variance-reduction methods for Asian arithmetic-average calls and generating comparison outputs
- Writeup detailing performance results and analysis

---


## Project Structure
```
├── gbm.py # GBM price path simulator 
├── payoffs.py # functions for each payoff type (vanilla, arithmetic asian, geometric asian) 
├── estimators.py # functions for estimation techniques (plain MC, antithetic variates, control variates)
├── plain_vanilla.py # plain MC + vanilla call validation script
├── asian_arith_pricing.py # plain MC vs variance-reduction comparison script
├── plots/ # generated plots/figures
├── logs/ # output .csv files (gitignored)
├── README.md # project description and instructions 
├── requirements.txt # Python dependencies
└── .gitignore # ignore rules (includes .venv, results/, pycache)
```