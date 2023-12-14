import numpy as np
from gekko import GEKKO
import math
import matplotlib.pyplot as plt
from atmos1976 import density

m = GEKKO()

### Model parameters
# Earth
R_reenty = m.Param(value = 6455) # km
g0 = m.Param(value=9.81) # m/s^2
earth_mu = m.Param(value=3.9860043543609598e5) # km^3/s^2

# Spacecraft
isp = m.Param(value=200) # s
sc_dry_mass = m.Param(value=1000) # kg
coefficient_drag = m.Param(value=2.0) # -
sc_cross_sectional_area = m.Param(value=3.8) # m^2
mission_lifepsan = m.Param(value=3.45) # years


### Model variables
# Earth
sma = m.Var(value=7000, lb=6378, ub=8000) # km

# Spacecraft
sc_wet_mass = m.Var() # kg


### Intermediate variables
# Earth
V_reentry = m.Intermediate(m.sqrt(earth_mu / R_reenty)) # km/s
atmospheric_density = m.Intermediate(density(sma.value - 6371)) # kg/m^3 

# Spacecraft
orbital_velocity = m.Intermediate(m.sqrt(earth_mu / sma)) # km/s
orbit_period = m.Intermediate(2 * math.pi * sma / orbital_velocity) # s
delta_v_deorbit = m.Intermediate(orbital_velocity - V_reentry) # km/s
propellant_mass = m.Intermediate(m.exp(delta_v_deorbit / (isp * g0)) * sc_dry_mass - sc_dry_mass) # kg

pert_drag_sma = m.Intermediate(-1 * sma**2 * atmospheric_density * coefficient_drag * sc_cross_sectional_area / (2 * math.pi * sc_wet_mass)) # km/s
time_to_degrade =  (1 / pert_drag_sma) * orbit_period # s
burns_a_year = 365 * 24 * 60 * 60 / time_to_degrade # -
burns_total = mission_lifepsan * burns_a_year # -
delta_v_per_burn = delta_v_deorbit / burns_total # km/s


### Implicit equations
m.Equation(sc_wet_mass == sc_dry_mass + propellant_mass)
m.Equation(delta_v_deorbit > 0)
m.Equation(sma > R_reenty)
m.Equation(propellant_mass > 0)

### Objective function
m.Obj(sc_wet_mass)

# Solve
m.solve(disp=False)

### Print solution
print('Optimal Solution (m)')
print('sma: ' + str(sma.value))
print('sc_wet_mass: ' + str(sc_wet_mass.value))
print('sc_dry_mass: ' + str(sc_dry_mass.value))
print('propellant_mass: ' + str(propellant_mass.value))
print(pert_drag_sma.value)