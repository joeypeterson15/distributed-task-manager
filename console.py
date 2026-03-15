import numpy as np
import json
import time

# rng = np.random.default_rng()
# grid = rng.random(size=(3, 3, 4, 4))
# region_boundaries = [[[] for _ in range(3)] for _ in range(3)]
# print(region_boundaries)

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
# boolean_matrix = [[False, True],[False, True]]
# print(np.any(boolean_matrix[index_matrix[0][1]]))
# print(boolean_matrix[index_matrix[0][0]][index_matrix[0][1]])
# print(np.where(boolean_matrix)[0][0])


n_grid_cols, n_grid_rows = 3,3
adjacent_regions=[[[] for _ in range(n_grid_cols)] for _ in range(n_grid_rows)]
dir = [(0,1), (0,-1), (1,0), (-1,0)]
for row in range(n_grid_rows):
    for col in range(n_grid_cols):
        for dr, dc in dir:
            adjacent_regions[row][col].append((dr,dc))
adjacent_regions = np.reshape(adjacent_regions, shape=(9, 4, -1))
print(adjacent_regions)