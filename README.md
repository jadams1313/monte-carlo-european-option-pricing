# Monte Carlo European Options Pricing

A Python implementation of Monte Carlo simulation methods for pricing European call and put options under the Black-Scholes framework.

## Overview

This project uses Monte Carlo simulation to estimate the fair value of European-style options by simulating thousands of potential price paths for the underlying asset and calculating the expected payoff at maturity. The implementation follows the risk-neutral valuation principle, where future payoffs are discounted at the risk-free rate.

## Theory

### Black-Scholes Model

Under the Black-Scholes assumptions, the stock price follows geometric Brownian motion:

```
dS(t) = μS(t)dt + σS(t)dW(t)
```

Where:
- S(t) is the stock price at time t
- μ is the expected return (drift)
- σ is the volatility
- W(t) is a Wiener process (Brownian motion)

### Risk-Neutral Valuation

In the risk-neutral world, the stock price evolution becomes:

```
S(T) = S(0) * exp((r - 0.5σ²)T + σ√T * Z)
```

Where:
- r is the risk-free interest rate
- T is time to maturity
- Z ~ N(0,1) is a standard normal random variable

### Option Payoffs

**Call Option:**
```
Payoff = max(S(T) - K, 0)
```

**Put Option:**
```
Payoff = max(K - S(T), 0)
```

Where K is the strike price.

The option price is the discounted expected payoff:
```
Option_Price = e^(-rT) * E[Payoff]
```

## Features

- European call and put option pricing
- Configurable simulation parameters (paths, time steps)
- Variance reduction techniques (antithetic variates, control variates)
- Convergence analysis and confidence intervals
- Greeks calculation (Delta, Gamma, Vega, Theta, Rho)
- Comparison with analytical Black-Scholes formula
- Visualization of price distributions and convergence


For questions or feedback, please open an issue on GitHub.

---

**Note:** This implementation is for educational and research purposes. Always validate results and consult with financial professionals before making trading decisions.
