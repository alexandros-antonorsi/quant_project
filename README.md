# Monte Carlo Exotic Option Pricing with Variance Reduction

## Overview
This project implements a Monte Carlo simulation engine for pricing exotic options, specifically the Asian arithmetic-average call option, under the Black–Scholes model.

The goal is to estimate option prices using simulated stock-price paths and demonstrate how variance-reduction techniques (Antithetic Variates and Control Variates) can dramatically improve accuracy for the same computational cost.

---

## Features
- Geometric Brownian Motion (GBM) price path simulator  
- Monte Carlo estimators for:
  - European vanilla call 
  - Asian arithmetic-average call 
- 95% confidence intervals 
- Variance-reduction methods:
  - Antithetic Variates — uses mirrored random samples to halve variance
  - Control Variates — uses the geometric-Asian’s closed-form price to cut variance 5–20×
- Benchmark script comparing methods by accuracy, runtime, and variance-reduction factor

---


## Project Structure
```
├── models/ # price path simulator (GBM)
├── payoffs/ # payoff types (vanilla, arithmetic asian, geometric asian) 
├── estimators/ # computational techniques (plain MC, MC + variance reductions)
├── utils/ # helper functions
├── benchmark/ # script to produce plots/tables
├── README.md # project description and instructions 
├── requirements.txt # Python dependencies
└── .gitignore # ignore rules (includes .venv, results/, pycache)
```