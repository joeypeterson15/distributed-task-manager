import numpy as np

K = float(0.2) # scalar

def update_region(payload, worker):
    boundaries = np.array(payload['boundaries'], dtype='float32')
    # region = payload['region']
    n_cells = worker.cells
    region_vals = worker.region_vals

    region_plus_ghost = add_ghost_boundaries(boundaries, region_vals, n_cells)
    n_cell_rows, n_cell_cols = n_cells

    next_region = np.zeros(shape=(n_cell_rows, n_cell_cols), dtype='float32')
    for m in range(1, n_cell_rows + 1):
        for n in range(1, n_cell_cols + 1): # no need to worry about left or right (ghost) cells
            
            # Discretized version of the heat equation. 
            laplacian = (region_plus_ghost[m][n] + K * (region_plus_ghost[m - 1][n] + region_plus_ghost[m + 1][n] + region_plus_ghost[m][n - 1] + region_plus_ghost[m][n + 1] - (4 * region_plus_ghost[m][n])))

            next_region[m - 1][n - 1] = laplacian
    
    return next_region

def add_ghost_boundaries(boundaries, region_vals, n_cells):
    # n_cell_rows, n_cell_cols = n_cells
    rtop, rbot, cleft, cright = boundaries
    # region_r, region_c = region_coords

    # grid = np.pad(grid, ((1,1), (1,1), (0,0), (0,0)))
    # region = grid[region_r + 1][region_c + 1]
    region_vals = np.hstack((cleft, region_vals))
    region_vals = np.hstack((region_vals, cright))
    rtop = np.pad(rtop, ((0,0), (1,1)))
    rbot = np.pad(rbot, ((0,0), (1,1)))
    region_vals = np.vstack((rtop, region_vals))
    region_vals = np.vstack((region_vals, rbot))

    return region_vals

