import numpy as np

def update_region(grid, region_coords, n_grid_rows, n_grid_cols, n_cell_rows, n_cell_cols):
    # all cells in the region depend on all adjacent cells
    # so cells on the edge need to be aware of adjacent cells in other regions => ghost boundaries!

    region_plus_ghost = add_ghost_boundaries_to_region(grid, region_coords, n_grid_rows, n_grid_cols, n_cell_rows, n_cell_cols)

    K = 3 #scalar constant
    updated_region = [[0 for _ in range(n_cell_cols)] for _ in range(n_cell_rows)]
    for m in range(1, n_cell_rows):
        for n in range(1, n_cell_cols):
            # This value will work if neighboring cells are in the region. 
            # If we're at the edge we need to go into other regions
            
            # Discretized version of the heat equation. 
            value = region_plus_ghost[m][n] + \
            K(region_plus_ghost[m - 1][n]
              + region_plus_ghost[m + 1][n]
              + region_plus_ghost[m][n - 1]
              + region_plus_ghost[m][n + 1]
              - 4(region_plus_ghost[m][n]))
            
            updated_region[m][n] = value
    return updated_region


def add_ghost_boundaries_to_region(grid, region_coords, n_grid_rows, n_grid_cols, n_cell_rows, n_cell_cols):
    region_r, region_c = region_coords
    region = np.array(grid[region_r][region_c])
    directions = [(0,1), (0,-1), (1,0), (-1,0)]
    for dr, dc in directions:
        adj_r = region_r + dr
        adj_c = region_c + dc

        # add zero rows/cols to grid boundary regions
        zero_ghost_row = np.array([[0] * n_grid_rows])
        zero_ghost_col = np.transpose([[0] * n_grid_cols])
        
        # add 0 row/col to boundary grid regions
        if adj_r < 0:
            # add ghost row to the bottom of region
            np.vstack((zero_ghost_row, region))
            continue
        elif adj_r >= n_grid_rows:
            # add ghost col to the end of region
            np.vstack((region, zero_ghost_row))
            continue
        if adj_c < 0:
            # add ghost row to the beginning of region
            np.hstack((zero_ghost_col, region))
            continue
        elif adj_c >= n_grid_cols:
            # add ghost row to end of region
            np.hstack((region, zero_ghost_col))
            continue

        adj_reg = np.array(grid[region_r + dr][region_c + dc])
        if dr < 0:
            # place adj reg bottom row as top row of region
            row = adj_reg[n_cell_rows-1:n_cell_rows, :] #(0:1 keeps the dimensions correct)
            np.vstack((row, region))
        if dr > 0:
            # place adj region top row as bottom row of region
            row = adj_reg[0:1, :] #(0:1 keeps the dimensions correct)
            np.vstack((region, row))
        if dc < 0:
            # place adj reg right col as left col of region
            col = adj_reg[:,n_cell_cols - 1:n_cell_cols] #(0:1 keeps the dimensions correct)
            np.hstack(col, region)
        if dc > 0:
            # place adj region left col as right col of region
            col = adj_reg[:, 0:1] #(0:1 keeps the dimensions correct)
            np.hstack(region, col)

        # REGION should now be padded on every side. So new region col length is n_cell_cols + 2. Same for rows
        return region

        