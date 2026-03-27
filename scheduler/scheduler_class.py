import numpy as np
import time
import collections

N_NEIGHBORS = 4

class Scheduler():    
    def __init__(self):       
        self.configure()

    def configure(self):
        self.tasks_queue = []
        self.workers = collections.defaultdict(list)
        self.n_grid_cols = 3
        self.n_grid_rows = 3
        self.n_cells = 4
        self.n_regions = self.n_grid_cols * self.n_grid_rows
        self.sim_duration = 25 #seconds
        self.time_interval = 1 #seconds
        self.epochs = self.sim_duration // self.time_interval
        self.epoch = 0
        self.n_worker_updates = 0

        self.grid = self.generate_grid()
        self.dependents_graph = self.generate_dependency_graph()
        self.required_ready_count = self.generate_required_ready_count()
        self.ready_neighbor_count = self.generate_ready_neighbor_count()
        self.updated_regions_bool = self.generate_updated_regions_grid()

    def register_worker(self, websocket, id):
        self.workers[id].append(websocket)

    def register_client(self, websocket):
        self.client = websocket

    def generate_updated_regions_grid(self):
        updated_regions_grid = np.zeros(shape=(self.epochs, self.n_grid_rows, self.n_grid_cols))
        for init_m in range(self.n_grid_rows):
            for init_n in range(self.n_grid_cols):
                updated_regions_grid[init_m][init_n] = 1
        return updated_regions_grid

    
    def update_grid(self, region, new_region_values, epoch):
        row, col = region
        self.grid[self.epoch + 1][row][col] = new_region_values
        self.updated_regions_bool[epoch][row][col] = 1
        self.update_dependents(row, col)

    def update_dependents(self, row, col, epoch):
        for r, c in self.dependents_graph[(row, col)]:
            self.ready_neighbor_count[epoch][r][c] += 1
            self.enqueue_tasks(r, c, epoch)

    def enqueue_tasks(self, r, c, epoch):
        if self.ready_neighbor_count[epoch][r][c] == self.required_ready_count[r][c] \
        and self.updated_regions_bool[r][c] == 1:
            self.tasks_queue.append(self.task_payload((r,c), epoch + 1))

    def generate_grid(self):
        rng = np.random.default_rng()
        grid = rng.random(size=(self.epochs,self.n_grid_rows, self.n_grid_cols, self.n_cells, self.n_cells))
        return grid
    
    def generate_ready_neighbor_count(self):
        ready_neighbor_count = np.zeros(shape=(self.epochs, self.n_grid_rows, self.n_grid_cols))

        for init_row, init_col in self.required_ready_count.keys():
            ready_neighbor_count[0][init_row][init_col] = self.required_ready_count[(init_row, init_col)]
        
        return ready_neighbor_count

    def generate_dependency_graph(self):
        dependency_graph = collections.defaultdict(list)
        dir = [(0,1), (0,-1), (1,0), (-1,0)]

        for row in range(self.n_grid_rows):
            for col in range(self.n_grid_cols):
                for dr, dc in dir:
                    r, c = row + dr, col + dc
                    if r < 0 or r > self.n_grid_rows - 1 or c < 0 or c > self.n_grid_cols - 1:
                        continue
                    dependency_graph[(row, col)].append((r,c))

        return dependency_graph
                    
    
    def generate_required_ready_count(self):
        required_count = {}
        dir = [(0,1), (0,-1), (1,0), (-1,0)]

        for row in range(self.n_grid_rows):
            for col in range(self.n_grid_cols):

                required_count[(row,col)] = 4 # assume all regions have 4 neighbors

                for dr, dc in dir:
                    r, c = row + dr, col + dc
                    if r < 0 or r > self.n_grid_rows - 1:
                        required_count[(row, col)] -= 1
                    if c < 0 or c > self.n_grid_cols - 1:
                        required_count[(row, col)] -= 1
        
        return required_count


    # def collect_regions(self, n_cols, n_rows):
    #     return [[r, c] for r in range(n_rows) for c in range(n_cols)]
    
    
    def collect_ghost_region_boundaries(self, region, epoch):
        zeros = np.zeros((self.n_cells)).tolist()
        r, c = region
        rtop = zeros if r == 0 else self.grid[epoch][r - 1][c][self.n_cells - 1][:]
        rbot = zeros if r == (self.n_grid_rows - 1) else self.grid[epoch][r + 1][c][0][:]
        cleft = zeros if c == 0 else self.grid[epoch][r][c - 1][:][self.n_cells - 1]
        cright = zeros if c == (self.n_grid_cols - 1) else self.grid[epoch][r][c + 1][:][0]
        return [rtop, rbot, cleft, cright]
    
    def task_payload(self, region, epoch):
        boundaries = self.collect_ghost_region_boundaries(region, epoch)
        payload = {
                    'epoch': epoch + 1,
                    'boundaries': boundaries,
                    'region': region,
                    'region_vals': self.grid[epoch][region[0]][region[1]],
                }
        
        return payload
