import math
from constants import earth_radius, earth_mu, g0, R_reentry
from atmos1976 import density
from spacecraft_constants import coefficient_drag, hydrazine_density, allowable_tensile_ultimate_strength_titanium, density_ti
from orbit import get_orbital_velocity, get_period
from utils import arctic_period


def get_sma_degradation(altitude, sc_mass):
    sma = altitude + earth_radius
    return (-2 * math.pi * (coefficient_drag * sc_cross_sectional_area / sc_mass) * density(altitude) * ((sma*1000) ** 2)) / 1000

def get_propellant_need(delta_v, sc_mass, isp):
    return math.exp(delta_v / (isp * g0 / 1000)) * sc_mass - sc_mass

def get_delta_v_maintenance(altitude, sc_mass):
    return (math.pi * (coefficient_drag * sc_cross_sectional_area / sc_mass) * density(altitude) * (sma*1000) * (get_orbital_velocity(altitude+earth_radius)*1000)) / 1000 # km/rev

def get_delta_v_deorbit(altitude):
    V_reentry = math.sqrt(earth_mu / R_reentry) # km/s
    delta_v_deorbit = V_reentry - get_orbital_velocity(altitude + earth_radius) # km/s
    return delta_v_deorbit

# Function to calculate thrust
def get_thrust_force(sc_wet_mass, delta_t, delta_v):
    thrust = (sc_wet_mass * delta_v) / delta_t
    return thrust 

def get_propellant_volume(mass, density):
    return mass / density

def get_tank_pressure(volume_tank):
    p_tank = math.exp(-0.1281 * math.log(volume_tank) + 0.2498)
    return 2 * p_tank


def get_tank_mass(propellant_volume):
    volume_tank = propellant_volume * 1.01
    pressure_tank = get_tank_pressure(volume_tank)
    n = 0.2
    p_b = 2 * pressure_tank
    return (1 + n) * (3 * p_b * density_ti / (2 * allowable_tensile_ultimate_strength_titanium)) * volume_tank

def get_engine_mass(thrust):
    m_engine = 1.5
    # m_engine = 0.00144 * thrust + 49.6
    return m_engine


if __name__ == "__main__":
    sc_cross_sectional_area = 28 # m^2
    dry_mass = 909.68 # kg
    altitude = 572
    sma = altitude + earth_radius
    isp = 200 # s

    orbit_period = get_period(altitude + earth_radius)
    orbits_per_year = 365 * 24 * 60 * 60 / orbit_period # orbits / year

    # Decay
    degradation = -1 * get_sma_degradation(altitude, dry_mass)
    degradiation_yearly = degradation * orbits_per_year
    delta_v_need_maintenance = get_delta_v_maintenance(altitude, dry_mass)
    delta_v_need_maintenance_yearly = delta_v_need_maintenance * orbits_per_year

    # Deorbit
    delta_v_deorbit = get_delta_v_deorbit(altitude)

    # Propulsion system needs
    burns_per_year = round(degradiation_yearly)
    propellant_need_maintenance = get_propellant_need(delta_v_need_maintenance, dry_mass, isp)
    propellant_need_deorbit = get_propellant_need(delta_v_deorbit, dry_mass, isp)
    propellant_need_total = propellant_need_maintenance + propellant_need_deorbit
    time_to_burn = arctic_period(altitude)
    thrust_force = get_thrust_force(dry_mass + propellant_need_total, time_to_burn, delta_v_need_maintenance * 1000)

    propellant_volume = get_propellant_volume(propellant_need_total, hydrazine_density)
    tank_mass = get_tank_mass(propellant_volume)
    engine_mass = get_engine_mass(thrust_force)

    print("ORBIT SPECS")
    print("Orbits per year: ", orbits_per_year)
    print("Degradation per year: ", degradiation_yearly)

    print("\nPROPULSION SYSTEM NEEDS")
    print("Delta-V maintenance per year: ", delta_v_need_maintenance_yearly)
    print("Delta-V per burn: ", delta_v_need_maintenance_yearly / burns_per_year)
    print("Propellant need maintenance: ", propellant_need_maintenance)
    print("Propellant need deorbit: ", propellant_need_deorbit)
    print("Propellant need total: ", propellant_need_total)
    print("Time to burn: ", time_to_burn/60, "minutes")
    print("Thrust force: ", thrust_force)
    
    print("\nPROPULSION SYSTEM SPECS")
    print("Tank mass: ", tank_mass)
    print("Engine mass: ", engine_mass)
    print("Propulsion system mass: ", tank_mass + engine_mass)