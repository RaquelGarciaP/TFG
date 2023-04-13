import numpy as np
import matplotlib.pyplot as plt
from KeplerianOrbit import KeplerianOrbit


# parameters
period1, period2 = 1301.25, 1301.25
K1, K2 = 147980.06, 147980.06
ecc1, ecc2 = 0.5, 0.5
omega1 = 90.0
omega2 = omega1 + 180.0
t_peri1, t_peri2 = 3.54, 18.31

# time array creation
# the time array goes from t=0 to t=period -> we have a full orbital cycle
# (both stars have the same orbital period)
num_t = 500
t = np.linspace(0.0, 5*period1, num_t)

# initialize keplerian orbit for both stars to obtain their radial velocity
orbit1 = KeplerianOrbit(t, period1, K1, ecc1, omega1, t_peri1)
orbit2 = KeplerianOrbit(t, period2, K2, ecc2, omega2, t_peri2)

# radial velocity array of both stars
rv1 = orbit1.rv.copy()
rv2 = orbit2.rv.copy()

fig, ax = plt.subplots()
l1, = ax.plot(t, rv1)
l2, = ax.plot(t, rv2)

ax.legend((l1, l2), ('rv1', 'rv2'), loc='upper right', shadow=False)
ax.grid()
ax.set_xlabel('time')
ax.set_ylabel('velocity')
ax.set_title('Radial velocity check')
plt.show()



