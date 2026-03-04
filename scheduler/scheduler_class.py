import numpy as np

class Scheduler():    
    def __init__(self):
        self.client = ''
        self.workers = []
        self.task = ''
        self.status = 0
        self.configure()

    def configure(self):
        self.n_grid_cols = 8
        self.n_grid_rows = 8
        self.n_cells = 10
        self.n_regions = self.n_grid_cols * self.n_grid_rows
        self.region_coords = self.collect_regions(self.n_grid_cols, self.n_grid_rows)
        self.sim_duration = 25 #seconds
        self.time_interval = 1 #seconds
        self.epochs = self.sim_duration // self.time_interval
        self.epoch = 0
        self.n_worker_updates = 0
        self.grid = self.gen_grid()

    def register_worker(self, websocket):
        self.workers.append(websocket)

    def register_client(self, websocket):
        self.client = websocket

    def configure_tasks(self, task):
        self.task = task

    def update_status(self, status_num):
        self.status = status_num

    def assign_workers(self):
        return
    
    def update_grid(self, region_coords, new_region):
        reg_row, reg_col = region_coords
        self.grid[self.epoch + 1][reg_row][reg_col] = new_region
    
    def gen_grid(self):
        rng = np.random.default_rng()
        grid = rng.random(size=(self.epochs, self.n_grid_rows, self.n_grid_cols, self.n_cells, self.n_cells))
        # grid = np.zeros(shape=(self.epochs,2,2,2,2), dtype='float32')
        # grid[0][0][0][1][1] = 1
        # print('grid in gen_grid: ', grid)
        return grid
    
    def collect_regions(self, n_cols, n_rows):
        return [[r, c] for r in range(n_rows) for c in range(n_cols)]
    
    def gen_task_payload(self, region_coord):
        return {
                'grid': self.grid[self.epoch].tolist(),
                'region_coords': region_coord,
                'n_regions': (self.n_grid_cols, self.n_grid_rows),
                'n_cells': (self.n_cells, self.n_cells)
            }


