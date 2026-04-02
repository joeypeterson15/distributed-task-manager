import numpy as np
from worker import heat

rng = np.random.default_rng()
matrix = rng.random(size=(20,20,20))
np.save('matrix.npy', matrix)
# data = np.load('worker/matrix.npy')
epochs = 20
zeros = np.zeros((20))

rtop = zeros
rbot = zeros
cleft = zeros
cright = zeros
print('MATRIX first row first col val: ', matrix[0][0][0])
boundaries = [rtop.tolist(), rbot.tolist(), cleft.tolist(), cright.tolist()]

for epoch in range(1, epochs):
    payload = {
        'boundaries': boundaries,
        'region_vals': matrix[epoch - 1]
    }
    next_vals = heat.update_region(payload)
    matrix[epoch] = next_vals

np.save('epochs.npy', matrix)

