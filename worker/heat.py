import numpy as np


def update_region(grid, region_coords, n_regions, n_cells):

    region_plus_ghost = add_ghost_boundaries_to_region(grid, region_coords, n_regions, n_cells)
    n_cell_rows, n_cell_cols = n_cells

    K = 1 #scalar constant
    updated_region = np.zeros(shape=(n_cell_rows, n_cell_cols), dtype=int)
    print('updated region: ', updated_region.shape)
    for m in range(1, n_cell_rows):
        for n in range(1, n_cell_cols):
            # This value will work if neighboring cells are in the region. 
            # If we're at the edge we need to go into other regions
            
            # Discretized version of the heat equation. 
            value = region_plus_ghost[m][n] + \
            K * (region_plus_ghost[m - 1][n]
              + region_plus_ghost[m + 1][n]
              + region_plus_ghost[m][n - 1]
              + region_plus_ghost[m][n + 1]
              - 4 * (region_plus_ghost[m][n]))
            
            updated_region[m][n] = value
    print(region_plus_ghost)
    return updated_region

def add_ghost_boundaries_to_region(grid, region_coords, n_regions, n_cells):
    # n_grid_rows, n_grid_cols = n_regions
    n_cell_rows, n_cell_cols = n_cells
    region_r, region_c = region_coords

    grid = np.pad(grid, ((1,1), (1,1), (0,0), (0,0)))
    print(grid.shape)
    

    region = np.array(grid[region_r][region_c])

    dir = [-1, 1]

    for dc in dir:
        adj_c = region_c + dc

        adj_reg = np.array(grid[region_r][adj_c])
        if dc < 0:
            # place adj reg right col as left col of region
            col = adj_reg[:,n_cell_cols - 1:n_cell_cols] #(0:1 keeps the dimensions correct)
            region = np.hstack((col, region))
        if dc > 0:
            # place adj region left col as right col of region
            col = adj_reg[:, 0:1] #(0:1 keeps the dimensions correct)
            region = np.hstack((region, col))

        # REGION should now be padded on every side. So new region col length is n_cell_cols + 2. Same for rows
    for dr in dir:
        adj_r = region_r + dr
        
        adj_reg = grid[adj_r][region_c]
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
            # print('region:', region)

        # add zero rows/cols to grid boundary regions
        


        # REGION should now be padded on every side. So new region col length is n_cell_cols + 2. Same for rows
    print('region shape:', region.shape)
    return region
    

mock_grid = [[[np.arange(5) for _ in range(5)] for _ in range(3)] for _ in range(3)]
# print(add_ghost_boundaries_to_region(mock_grid, (2,2), (3, 3), (5, 5)))
print(update_region(mock_grid, (2,2), (3, 3), (5, 5)))

        