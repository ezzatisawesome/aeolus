import numpy as np
from gekko import GEKKO
import math
import matplotlib.pyplot as plt

m = GEKKO()

# Model parameters
R_reenty = m.Param(value = 6455) # km
earth_mu = m.Param(value=3.9860043543609598e5) # km^3/s^2
isp = m.Param(value=200) # s
g0 = m.Param(value=9.81) # m/s^2
sc_dry_mass = m.Param(value=1000) # kg

# Model variables
sma = m.Var(value=7000, lb=6000, ub=8000) # km
sc_wet_mass = m.Var() # kg

# Intermediate variables
orbital_velocity = m.Intermediate(m.sqrt(earth_mu / sma)) # km/s
V_reentry = m.Intermediate(m.sqrt(earth_mu / R_reenty)) # km/s
delta_v_deorbit = m.Intermediate(orbital_velocity - V_reentry) # km/s
propellant_mass = m.Intermediate(m.exp(delta_v_deorbit / (isp * g0)) * sc_dry_mass - sc_dry_mass) # kg

# Implicit equations
m.Equation(sc_wet_mass == sc_dry_mass + propellant_mass)
m.Equation(delta_v_deorbit > 0)
m.Equation(sma > R_reenty)
m.Equation(propellant_mass > 0)

# Objective function
m.Obj(sc_wet_mass)

# Solve
m.solve(disp=False)

# Print solution
print('Optimal Solution (m)')
print('sma: ' + str(sma.value))
print('sc_wet_mass: ' + str(sc_wet_mass.value))
print('sc_dry_mass: ' + str(sc_dry_mass.value))
print('propellant_mass: ' + str(propellant_mass.value))