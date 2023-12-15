from constants import arctic_circle_latitude, earth_radius
from orbit import get_period

def arctic_period(altitude):
    period = get_period(altitude + earth_radius)
    return 2 * (90 - arctic_circle_latitude) / 360 * period

if __name__ == "__main__":
    period_over_arctic = arctic_period(550)
    print("Period over arctic: ", period_over_arctic, "s =", period_over_arctic / 60 / 60, "hours")
