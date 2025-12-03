import numpy as np 
import pandas as pd 
from scipy.stats import norm
#const: Euler's number in float64 
e = np.e
class Option: 
    
    def __init__(self, K: float, T: float, S_0: float, r: float, sigma: float, putOrCall: str) -> None: 
        self.K = K 
        self.T = T
        self.S_0 = S_0 
        self.r = r
        self.sigma = sigma
        self.putOrcall = putOrCall.lower()


    #return BSM solution to the price of the option given the object's instatiation params. 
    def calc_black_scholes_merton(self) -> float: 
        d_1 = (np.log(self.S_0/self.K) + (self.r + (self.sigma**2)/2) * self.T) / (self.sigma * np.sqrt(self.T))
        d_2 = d_1 - (self.sigma* np.sqrt(self.T))

        if self.putOrcall == 'call':
            discount_factor = -self.r * self.T
            return (self.S_0 * norm.cdf(d_1)) - (self.K * np.float_power(e, discount_factor) * norm.cdf(d_2))
        else:
            return (self.K * np.float_power(e, discount_factor) * norm.cdf(-d_2)) - (self.S_0 * norm.cdf(-d_1))
    def __repr__(self) -> str:
        option_type = self.putOrcall.capitalize()
        return (f"{option_type} Option: Strike=${self.K:.2f}, Spot=${self.S_0:.2f}, "
            f"Expiry={self.T:.2f}y, Rate={self.r:.2%}, Vol={self.sigma:.2%}")
    
#Monte Carlo Section

def simulate(num_simulations: int, option: Option, dt: float, theta: float = None, omega: float = None, xi: float = None, nu_0: float = None) -> np.array:
    steps = int(option.T / dt)
    S = np.zeros((num_simulations, steps + 1))
    S[:, 0] = option.S_0
    
    if theta is not None:
        # heston model
        nu = np.zeros((num_simulations, steps + 1))
        nu[:, 0] = nu_0
        
        for t in range(steps):
            dz1 = np.random.normal(0, np.sqrt(dt), num_simulations)  # for s
            dz2 = np.random.normal(0, np.sqrt(dt), num_simulations)  # for vol
            
            
            nu[:, t + 1] = nu[:, t] + theta * (omega - nu[:, t]) * dt + xi * np.sqrt(np.maximum(nu[:, t], 0)) * dz2
            nu[:, t + 1] = np.maximum(nu[:, t + 1], 0)  # keep non-negative
            
            S[:, t + 1] = S[:, t] * np.exp((option.r - 0.5 * nu[:, t]) * dt + 
                                            np.sqrt(np.maximum(nu[:, t], 0)) * dz1)
    else:
        for t in range(steps):
            delta_z = np.random.normal(0, np.sqrt(dt), num_simulations)
            S[:, t + 1] = S[:, t] * np.exp((option.r - 0.5 * option.sigma**2) * dt + 
                                            option.sigma * delta_z)
    
    return S[:, -1]
def calc_expected_price(simulated_paths: np.array, option: Option) -> float:
    
    payoffs = np.maximum(simulated_paths - option.K, 0) if option.putOrcall == 'call' else np.maximum(option.K - simulated_paths, 0)      
    discount_factor =  -1 * option.r * option.T
    expected_payoff = np.average(payoffs) * np.float_power(e, discount_factor)

    return expected_payoff

