# -*- coding: utf8 -*-

import numpy as np
from solve_and_post_proc import solve
from diff_generator import gen_diff
from objects_generator import generate_all_objects
import matplotlib.pyplot as plt

# variable sets: [Kiz, Eiz. Kexc, Eexc, Kela, Eela, h]

# create , no need to include it in any loop
# gen_diff('input_xenon.txt')
gen_diff('input_iodine.txt')

# nb_cases = 10
my_objects = generate_all_objects('input_iodine.txt')

power = 1E3 * np.arange(100, 500000, 25000)

results = []

for pow in power:

    thruster = my_objects[0]
    params = my_objects[1]
    params.Pabs = pow

    chem = my_objects[2]

    # print(thruster, params, chem)

    init = chem.init_vector

    results.append(solve(thruster, params, chem, init).values.y[-1])

print(results[0])

n_e = [res[0] for res in results]
n_Im = [res[1] for res in results]
n_I2 = [res[2] for res in results]
nI = [res[3] for res in results]
n_Ip = [res[4] for res in results]
n_I2p = [res[5] for res in results]
Te = [res[6] for res in results]
Tg = [res[7] for res in results]

fig, ax = plt.subplots()
ax.plot(power, n_e, 'o')
plt.show()
