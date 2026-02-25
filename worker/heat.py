def calculate(region, init_grid, n_grid_rows, n_grid_cols, cell_rows, cell_cols):
    # all cells in the region depend on all adjacent cells
    # so cells on the edge need to be aware of adjacent cells in other regions => ghost boundaries!
    add_ghost_boundaries_to_region()
    k = 3 #scalar constant
    grid_r, grid_c = region
    init_region = init_grid[grid_r][grid_c]
    next_grid = [[0 for _ in range(cell_cols)] for _ in range(cell_rows)]
    for m in range(cell_rows):
        for n in range(cell_cols):
            # This value will work if neighboring cells are in the region. 
            # If we're at the edge we need to go into other regions
                
            value = init_region[m][n] + \
            k(init_region[m - 1][n]
              + init_region[m + 1][n]
              + init_region[m][n - 1]
              + init_region[m][n + 1]
              - 4(init_region[m][n]))
            
            next_grid[m][n] = value


def add_ghost_boundaries_to_region(init_grid, region):
    return init_grid_region_plus_ghost_boundaries

        