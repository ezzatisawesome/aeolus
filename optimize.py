import numpy as np
from gekko import GEKKO
import math

m = GEKKO()

### Model parameters
# Earth
earth_mu = m.Param(value=3.9860043543609598e5) # km^3/s^2

# Vehicle
payload_mass = m.Param(value=450) # kg

# Orbit
ecc = m.Param(value=0.0) # eccentricity
inc = m.Param(value=0.0) # inclination
raan = m.Param(value=0.0) # right ascension of the ascending node
aop = m.Param(value=0.0) # argument of periapsis
ta = m.Param(value=0.0) # true anomaly


### Model variables

# Vehicle
dry_mass = m.Var(value=1000, lb=800, ub=1200) # kg
mass_spacecraft = m.Var(value=1000, lb=800, ub=1200)

# Orbit
sma = m.Var(value=7000, lb=6000, ub=8000) # km




# Intermediate variables

orbital_velocity = m.Intermediate(math.sqrt(earth_mu / sma)) # km/s
drag_pert = m.Intermediate((2.2 * 3.8 * 1e-12 * orbital_velocity**2) / mass_spacecraft) # drag perturbation