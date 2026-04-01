import numpy as np

K = float(0.1) # scalar

def update_region(payload):
    boundaries = np.array(payload['boundaries'], dtype='float32')
    region_vals = np.array(payload['region_vals'], dtype='float32')

    n_cell_rows, n_cell_cols = len(region_vals), len(region_vals[0])

    region_plus_ghost = add_ghost_boundaries(boundaries, region_vals)

    assert region_plus_ghost.shape == (n_cell_rows + 2, n_cell_cols + 2)

    next_region = np.zeros(shape=(n_cell_rows, n_cell_cols), dtype='float32')
    for m in range(1, n_cell_rows + 1):
        for n in range(1, n_cell_cols + 1): # no need to worry about left or right (ghost) cells
            
            # Discretized version of the heat equation. 
            laplacian = (region_plus_ghost[m][n] + K * (region_plus_ghost[m - 1][n] + region_plus_ghost[m + 1][n] + region_plus_ghost[m][n - 1] + region_plus_ghost[m][n + 1] - (4 * region_plus_ghost[m][n])))

            next_region[m - 1][n - 1] = laplacian
    
    return next_region

def add_ghost_boundaries(boundaries, region_vals):

    rtop, rbot, cleft, cright = boundaries
    rtop = np.array(rtop).reshape((1,-1))
    rbot = np.array(rbot).reshape((1,-1))
    cleft = np.array(cleft).reshape((1,-1)).T
    cright = np.array(cright).reshape((1,-1)).T

    print('region vals: ', region_vals)
    print('boundaries: ', cleft)
    region_vals = np.hstack((cleft, region_vals))
    region_vals = np.hstack((region_vals, cright))
    rtop = np.pad(rtop, ((0,0), (1,1)))
    rbot = np.pad(rbot, ((0,0), (1,1)))
    region_vals = np.vstack((rtop, region_vals))
    region_vals = np.vstack((region_vals, rbot))

    return region_vals

