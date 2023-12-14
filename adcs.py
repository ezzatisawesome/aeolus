import math

def calculate_control_torque(margin_factor, largest_disturbance_t):
    Tc = largest_disturbance_t * margin_factor
    return Tc

# @param theta: angle of slew (degrees)
# @param inertia: moment of inertia
# @param time: time of slew
def calculate_slew_torque(theta, inertia, time):
    T = 4 * math.radians(theta) * inertia / time ** 2
    return T

# @param largest_disturbance_t: largest disturbance torque
# @param period: orbit period
def momentum_storage(largest_disturbance_t, period):
    momentum = largest_disturbance_t * period * (0.707) / 4
    return momentum

def magnetic_torquer_dipole(momentum_storage, t, earth_field):
    dipole = momentum_storage / (t * earth_field)
    return dipole


if __name__ == "__main__":
    margin_factor = 2.1
    largest_disturbance_t = 0.00504
    Tc = calculate_control_torque(margin_factor, largest_disturbance_t)
    print("Tc = ", Tc)

    theta = 360
    inertia = 5275.2973694
    time = 6648.12
    Ts = calculate_slew_torque(theta, inertia, time)
    print("Ts = ", Ts)

    h = momentum_storage(largest_disturbance_t, time)
    print("h = ", h)

    earth_field = 1.78371747e-5
    t = 6648.12
    dipole = magnetic_torquer_dipole(h, t, earth_field)
    print("dipole = ", dipole)
