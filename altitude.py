import numpy as np
from gekko import GEKKO
import math
import matplotlib.pyplot as plt
from atmos1976 import density

m = GEKKO()

### Model parameters
# Earth
R_reenty = m.Param(value = 6455) # km
g0 = m.Param(value=9.80665) # m/s^2
mu_earth = m.Param(value=3.9860043543609598e5) # km^3/s^2
R_earth = m.Param(value=6371) # km

# Spacecraft
isp = m.Param(value=200) # s
sc_dry_mass = m.Param(value=1300) # kg
coefficient_drag = m.Param(value=2.2) # -
sc_cross_sectional_area = m.Param(value=3.8) # m^2
mission_lifepsan = m.Param(value=3.45) # years


### Model variables
# Earth
sma = m.Var(value=6750, lb=6378, ub=7200) # km

# Spacecraft
# sc_wet_mass = m.Var() # kg
propellant_mass = m.Var() # kg


### Intermediate variables
# Earth
V_reentry = m.Intermediate(m.sqrt(mu_earth / R_reenty)) # km/s
atmospheric_density = m.Intermediate(density(sma.value - R_earth.value)) # kg/km^3

# Spacecraft
orbital_velocity = m.Intermediate(m.sqrt(mu_earth / sma)) # km/s
#- Deorbit
delta_v_deorbit = m.Intermediate(V_reentry - orbital_velocity) # km/s
#- Maintenance
orbit_period = m.Intermediate(2 * math.pi * m.sqrt(sma ** 3 / mu_earth)) # s
orbits_per_year = m.Intermediate(365 * 24 * 60 * 60 / orbit_period) # orbits / year
delta_v_lost_drag = m.Intermediate((math.pi * (coefficient_drag * sc_cross_sectional_area / sc_dry_mass) * atmospheric_density * (sma*1000) * (orbital_velocity*1000)) / 1000) # km/rev
delta_v_maintenance = m.Intermediate(delta_v_lost_drag * orbits_per_year * mission_lifepsan) # km
#- Propellant
delta_v_total = m.Intermediate(delta_v_deorbit + delta_v_maintenance) # km
# propellant_mass = m.Intermediate(m.exp(delta_v_total / (isp * g0 / 1000)) * sc_dry_mass - sc_dry_mass) # kg

### Implicit equations
# m.Equation(sc_wet_mass == sc_dry_mass + propellant_mass)
m.Equation(propellant_mass == m.exp(delta_v_total / (isp * g0 / 1000)) * sc_dry_mass - sc_dry_mass)
m.Equation(propellant_mass > 0)
m.Equation(sma > R_reenty)


### Minimize
m.Minimize(propellant_mass)


### Solve
m.solve()


### Print solution
print('Optimal Solution (m)')
print('sma: ' + str(sma.value))
print('Altitude: ' + str(sma.value[0] - R_earth.value[0]))
# print('sc_wet_mass: ' + str(sc_wet_mass.value))
print('sc_dry_mass: ' + str(sc_dry_mass.value))
print('propellant_mass: ' + str(propellant_mass.value))
print('orbital_velocity: ' + str(orbital_velocity.value))
print('reentry_velocity: ' + str(V_reentry.value))
print('delta_v_deorbit: ' + str(delta_v_deorbit.value))
# - Maintenance
print('orbit_period: ' + str(orbit_period.value))
print('orbits_per_year: ' + str(orbits_per_year.value))
print('Delta V lost per orbit: ' + str(delta_v_lost_drag.value))
print('delta_v_maintenance: ' + str(delta_v_maintenance.value))
print('atmospheric_density: ' + str(atmospheric_density.value))
print('delta_v_total: ' + str(delta_v_total.value))
