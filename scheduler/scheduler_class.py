import numpy as np
import time
import collections

BOUNDARY_IDX = {
    'rt': 0,
    'rb': 1,
    'cl': 2,
    'cb': 3
}

class Scheduler():    
    def __init__(self):
        self.client = ''
        self.workers = collections.defaultdict(list)
        self.task = ''
        # self.status = 0
        self.configure()

    def configure(self):
        self.n_grid_cols = 3
        self.n_grid_rows = 3
        self.n_cells = 4
        self.n_regions = self.n_grid_cols * self.n_grid_rows
        self.region_coords = self.collect_regions(self.n_grid_cols, self.n_grid_rows)
        self.collect_adj_regions()
        self.sim_duration = 25 #seconds
        self.time_interval = 1 #seconds
        self.epochs = self.sim_duration // self.time_interval
        self.epoch = 0
        self.n_worker_updates = 0
        self.grid = self.gen_initial_grid()
        self.gen_boundaries()
        # initialize to true for initial worker assignment(boundaries are already ready)
        self.updated_boundaries = [[True for _ in range(self.n_grid_cols)] for _ in range(self.n_grid_rows)]

    def register_worker(self, websocket, id):
        self.workers[id].append(websocket)

    def assign_regions_to_workers(self):
        for i, id in enumerate(self.workers.keys()):
            self.workers[id].append(self.region_coords[i])
            # assign adjacent regions also
            self.workers[id].append(self.adjacent_regions[i])

    def register_client(self, websocket):
        self.client = websocket

    def configure_tasks(self, task):
        self.task = task

    def update_status(self, status_num):
        self.status = status_num

    def assign_workers(self):
        return
    
    def update_grid(self, region, new_region_values):
        reg_row, reg_col = region
        self.grid[self.epoch + 1][reg_row][reg_col] = new_region_values
    
    def gen_initial_grid(self):
        rng = np.random.default_rng()
        grid = rng.random(size=(self.epochs,self.n_grid_rows, self.n_grid_cols, self.n_cells, self.n_cells))
        return grid
    
    def gen_boundaries(self):
        # each region contains its boundaries -> region =[[rowup], [rowbot], [cleft], [cright]]
        self.boundaries = [[[] for _ in range(self.n_grid_cols)] for _ in range(self.n_grid_rows)]
        for r in range(self.n_grid_rows):
            for c in range(self.n_grid_cols):
                rtop = self.grid[0][r][c][0][:]
                rbot = self.grid[0][r][c][self.n_cells - 1][:]
                cleft = self.grid[0][r][c][:][0]
                cright = self.grid[0][r][c][:][self.n_cells - 1]
                self.boundaries[r][c].append(list(zip(rtop,rbot,cleft,cright)))

    def collect_regions(self, n_cols, n_rows):
        return [[r, c] for r in range(n_rows) for c in range(n_cols)]
    
    def collect_adj_regions(self):
        self.adjacent_regions=[[] for _ in range(self.n_grid_cols) for _ in range(self.n_grid_rows)]
        dir = [(0,1), (0,-1), (1,0), (-1,0)]
        for row in range(self.n_grid_rows):
            for col in range(self.n_grid_cols):
                for dr, dc in dir:
                    self.adjacent_regions[row][col].append(dr,dc)
    
    def collect_region_boundaries(self, region):
        zeros = np.zeros((self.n_cells))
        row, col = region
        reg_boundaries = [[] for _ in range(4)]        

        if row == 0:
            reg_boundaries[BOUNDARY_IDX['rt']] = zeros
        else:
            reg_boundaries[BOUNDARY_IDX['rt']] = self.boundaries[row - 1][col][BOUNDARY_IDX['rb']]

        if row >= self.n_grid_rows - 1:
            reg_boundaries[BOUNDARY_IDX['rb']] = zeros
        else:
            reg_boundaries[BOUNDARY_IDX['rb']] = self.boundaries[row + 1][col][BOUNDARY_IDX['rt']]

        if col == 0:
            reg_boundaries[BOUNDARY_IDX['cl']] = zeros
        else:
            reg_boundaries[BOUNDARY_IDX['cl']] = self.boundaries[row][col - 1][BOUNDARY_IDX['cr']]
    
        if col >= self.n_grid_cols - 1:
            reg_boundaries[BOUNDARY_IDX['cr']] = zeros
        else:
            reg_boundaries[BOUNDARY_IDX['cr']] = self.boundaries[row][col + 1][BOUNDARY_IDX['cl']]
        
        return reg_boundaries
    
    def update_boundaries(self, region, region_vals):
        r, c = region
        rtop = region_vals[0][:]
        rbot = region_vals[self.n_cells - 1][:]
        cleft = region_vals[:][0]
        cright = region_vals[:][self.n_cells - 1]
        self.boundaries[r][c] = [list(zip(rtop,rbot,cleft,cright))]
        self.updated_boundaries[r][c] = True
        return
    
    def gen_task_payload(self, region):
        boundaries = self.collect_region_boundaries(region)
        initial_region_values = self.grid[self.epoch][region[0]][region[1]].tolist()
        payload = {
                    'boundaries': boundaries,
                    'region': region,
                    'n_regions': (self.n_grid_cols, self.n_grid_rows),
                    'n_cells': (self.n_cells, self.n_cells)
                }
        if self.epoch == 0:
            payload['initial_region_values'] = initial_region_values
        
        return payload
        


