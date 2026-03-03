import numpy as np

def update_region(grid, region_coords, n_cells):

    region_plus_ghost = add_ghost_boundaries(grid, region_coords, n_cells)
    n_cell_rows, n_cell_cols = n_cells

    K = 0.1 # scalar
    next_region = np.zeros(shape=(n_cell_rows, n_cell_cols), dtype='float32')
    for m in range(1, n_cell_rows + 1):
        for n in range(1, n_cell_cols + 1): # no need to worry about left or right (ghost) cells
            
            # Discretized version of the heat equation. 
            value = (region_plus_ghost[m][n] +
            K * (region_plus_ghost[m - 1][n]
              + region_plus_ghost[m + 1][n]
              + region_plus_ghost[m][n - 1]
              + region_plus_ghost[m][n + 1]
              - (4 * region_plus_ghost[m][n])))

            next_region[m - 1][n - 1] = value
    # print(region_plus_ghost)
    return next_region

def add_ghost_boundaries(grid, region_coords, n_cells):
    n_cell_rows, n_cell_cols = n_cells
    region_r, region_c = region_coords

    grid = np.pad(grid, ((1,1), (1,1), (0,0), (0,0)))
    # print('pad grid', grid)
    region = np.array(grid[region_r + 1][region_c + 1])
    # print('region extracted from padded grid', region)

    dir = [-1, 1]    
    for dc in dir:
        adj_c = region_c + 1 + dc

        adj_reg = np.array(grid[region_r + 1][adj_c])
        if dc < 0:
            # place adj reg right col as left col of region
            col = adj_reg[:,n_cell_cols - 1:n_cell_cols] #(0:1 keeps the dimensions correct)
            region = np.hstack((col, region))
        if dc > 0:
            # place adj region left col as right col of region
            col = adj_reg[:, 0:1] #(0:1 keeps the dimensions correct)
            region = np.hstack((region, col))



    for dr in dir:
        adj_r = region_r + dr + 1
        
        adj_reg = grid[adj_r][region_c + 1]
        if dr < 0:
            # place adj reg bottom row as top row of region
            row = adj_reg[n_cell_rows-1:n_cell_rows, :] #(0:1 keeps the dimensions correct)
            row = np.pad(row, ((0,0),(1,1))) # new region col length is n_cell_cols + 2
            region = np.vstack((row, region))
        if dr > 0:
            # place adj region top row as bottom row of region
            row = adj_reg[0:1, :] #(0:1 keeps the dimensions correct)
            row = np.pad(row, ((0,0),(1,1)))
            region = np.vstack((region, row))

    # print('region with ghost boundaries', region)

    return region


mock_grid = np.ones(shape=(2,2,2,2), dtype='float32')
u = update_region(mock_grid, (1,0), (2,2))
print('mock grid', mock_grid)
print(u)