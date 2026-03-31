import numpy as np
import time
import collections

N_NEIGHBORS = 4
DIRECTIONS = [(0,1), (0,-1), (1,0), (-1,0)]

class Scheduler():    
    def __init__(self):       
        self.configure()

    def configure(self):
        self.tasks_queue = collections.deque()
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
        self.ready_queue()

    def register_worker(self, websocket, id):
        self.workers[id].append(websocket)

    def register_client(self, websocket):
        self.client = websocket

    def generate_updated_regions_grid(self):
        updated_regions_grid = np.zeros(shape=(self.epochs, self.n_grid_rows, self.n_grid_cols))
        updated_regions_grid[0][:][:] = 1 #first grid is ready
        return updated_regions_grid

    def update_grid(self, region, new_region_values, epoch):
        row, col = region
        self.grid[self.epoch][row][col] = new_region_values
        self.updated_regions_bool[epoch][row][col] = 1
        self.increment_dependents(row, col)

    def increment_dependents(self, row, col, epoch):
        for r, c in self.dependents_graph[(row, col)]:
            self.ready_neighbor_count[epoch][r][c] += 1
            self.enqueue_tasks(r, c, epoch)

    def enqueue_tasks(self, r, c, epoch):
        if self.ready_neighbor_count[epoch][r][c] == self.required_ready_count[(r,c)] \
        and self.updated_regions_bool[epoch][r][c] == 1:
            self.tasks_queue.append(self.task_payload((r,c), epoch))

    def ready_queue(self):
        for r in range(self.n_grid_rows):
            for c in range(self.n_grid_cols):
                self.enqueue_tasks(r, c, 0)

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

        for row in range(self.n_grid_rows):
            for col in range(self.n_grid_cols):
                for dr, dc in DIRECTIONS:
                    r, c = row + dr, col + dc
                    if r < 0 or r > self.n_grid_rows - 1 or c < 0 or c > self.n_grid_cols - 1:
                        continue
                    dependency_graph[(row, col)].append((r,c))

        return dependency_graph

    def generate_required_ready_count(self):
        required_count = {}

        for row in range(self.n_grid_rows):
            for col in range(self.n_grid_cols):

                required_count[(row,col)] = 4 # assume all regions have 4 neighbors

                for dr, dc in DIRECTIONS:
                    r, c = row + dr, col + dc
                    if r < 0 or r > self.n_grid_rows - 1:
                        required_count[(row, col)] -= 1
                    if c < 0 or c > self.n_grid_cols - 1:
                        required_count[(row, col)] -= 1
        
        return required_count
    
    def collect_ghost_region_boundaries(self, region, epoch):
        zeros = np.zeros((self.n_cells))
        r, c = region
        rtop = zeros if r == 0 else self.grid[epoch][r - 1][c][self.n_cells - 1][:]
        rbot = zeros if r == (self.n_grid_rows - 1) else self.grid[epoch][r + 1][c][0][:]
        cleft = zeros if c == 0 else self.grid[epoch][r][c - 1][:][self.n_cells - 1]
        cright = zeros if c == (self.n_grid_cols - 1) else self.grid[epoch][r][c + 1][:][0]
        return [rtop.tolist(), rbot.tolist(), cleft.tolist(), cright.tolist()]
    
    def task_payload(self, region, epoch):
        boundaries = self.collect_ghost_region_boundaries(region, epoch)
        payload = {
                    'epoch': epoch + 1,
                    'boundaries': boundaries,
                    'region': region,
                    'region_vals': self.grid[epoch][region[0]][region[1]].tolist(),
                }
        # print('payload:', payload)
        
        return payload
