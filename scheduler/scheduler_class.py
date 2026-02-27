import numpy as np

class Scheduler():    
    def __init__(self):
        self.client = ''
        self.workers = []
        self.task = ''
        self.status = 0
        self.configure()

    def configure(self):
        self.n_grid_cols = 3
        self.n_grid_rows = 3
        self.n_cells = 5
        self.n_regions = self.n_grid_cols * self.n_grid_rows
        self.region_coords = self.collect_regions(self.n_grid_cols, self.n_grid_rows)
        self.sim_duration = 10 #seconds
        self.time_interval = 1 #seconds
        self.epochs = self.sim_duration // self.time_interval
        self.epoch = 0
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
    
    def update_grid(self, region_coords, new_region, epoch):
        reg_row, reg_col = region_coords
        self.grid[epoch][reg_row][reg_col] = new_region
    
    def gen_grid(self):
        # grid = [[[[0 for _ in range(self.n_cells)] for _ in range(self.n_cells)] for _ in range(self.n_grid_cols)] for _ in range(self.n_grid_rows)]
        # return [grid] * self.epochs
        # grid = np.zeros(shape=(self.epochs, self.n_grid_rows, self.n_grid_cols, self.n_cells, self.n_cells), dtype=int)
        grid = np.random.randint(0, 101, size=(self.epochs, self.n_grid_rows, self.n_grid_cols, self.n_cells, self.n_cells), dtype=int)
        grid = grid / 100
        return grid
    
    def collect_regions(self, n_cols, n_rows):
        return [[m,n] for n in range(n_cols) for m in range(n_rows)]
    
    def gen_task_payload(self, region_coord, epoch):
        return {
                'grid': self.grid[epoch],
                'region_coords': region_coord,
                'n_regions': (self.n_grid_cols, self.n_grid_rows),
                'n_cells': self.n_cells
            }


