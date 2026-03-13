import numpy as np
import json
import time

# rng = np.random.default_rng()
# grid = rng.random(size=(3, 3, 4, 4))
region_boundaries = [[[] for _ in range(3)] for _ in range(3)]
print(region_boundaries)

# for r in range(3):
#     for c in range(3):
#         rtop = grid[r][c][0][:]
#         rbot = grid[r][c][4 - 1][:]
#         cleft = grid[r][c][:][0]
#         cright = grid[r][c][:][4 - 1]
#         region_boundaries[r][c].append(list(zip(rtop,rbot,cleft,cright)))
#         if r == 0 and c == 0:
#             print(list(zip(rtop,rbot,cleft,cright)))

# # print(region_boundaries[0][0])
# index_matrix = [[0,1], [1,1]]
boolean_matrix = [[False, True],[False, True]]
# print(np.any(boolean_matrix[index_matrix[0][1]]))
# print(boolean_matrix[index_matrix[0][0]][index_matrix[0][1]])
print(np.where(boolean_matrix)[0][0])