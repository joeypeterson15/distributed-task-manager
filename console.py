import numpy as np
import json


rng = np.random.default_rng()
grid = rng.random(size=(3, 3), dtype='float32')
print(grid.shape)
print(np.arange(0, 10, 1))