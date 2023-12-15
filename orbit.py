from constants import j2, earth_mu, earth_radius
import math

def get_inclination(sma, e):
    precesssion = 2 * math.pi / 365 / 24 / 60 / 60
    radians = math.acos(-2/3 * precesssion * 1/j2 * (sma * (1 - e**2) / earth_radius) * math.sqrt(sma ** 3 / earth_mu))
    return math.degrees(radians)

def get_period(sma):
    return 2 * math.pi * math.sqrt(sma ** 3 / earth_mu)

def orbital_velocity(sma):
    return math.sqrt(earth_mu / sma)

def orbits_per_day(sma):
    return 24 * 60 * 60 / get_period(sma)


if __name__ == '__main__':
    sma = 550 + earth_radius
    print("i", get_inclination(sma, 0.0))
    print("SMA: ", 550 + earth_radius)
    print("Period = ", get_period(sma), "s =", get_period(sma) / 60 / 60, "hours")
    print("Velocity = ", orbital_velocity(sma), "km/s")
    print("Orbits per day = ", orbits_per_day(sma))