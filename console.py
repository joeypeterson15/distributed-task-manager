import numpy as np
import json


rng = np.random.default_rng()
grid = rng.random(size=(3, 3), dtype='float32')

s = json.dumps(grid.tolist())
uns = json.loads(s)
print(grid.tolist())
