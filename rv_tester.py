import numpy as np
import matplotlib.pyplot as plt
from KeplerianOrbit import KeplerianOrbit


# parameters
period = 1728000.0  # seconds
K1, K2 = 147980.06, 147980.06  # 156760.43
ecc = 0.5
omega1 = 90.0
omega2 = omega1 + 180.0
t_peri = 3.54

# time array creation
# the time array goes from t=0 to t=period -> we have a full orbital cycle
# (both stars have the same orbital period)
num_t = 500
t = np.linspace(0.0, 5*period, num_t)

# initialize keplerian orbit for both stars to obtain their radial velocity
orbit = KeplerianOrbit(t, period, ecc, t_peri)
# orbit2 = KeplerianOrbit(t, period, K2, ecc2, omega2, t_peri2)

# radial velocity array of both stars
rv1 = orbit.keplerian_orbit(K1, omega1)
rv2 = orbit.keplerian_orbit(K2, omega2)

fig, ax = plt.subplots()
l1, = ax.plot(t, rv1)
l2, = ax.plot(t, rv2)

ax.legend((l1, l2), ('rv1', 'rv2'), loc='upper right', shadow=False)
ax.grid()
ax.set_xlabel('time')
ax.set_ylabel('velocity')
ax.set_title('Radial velocity check')
plt.show()



