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
        self.n_grid_cols = 4
        self.n_grid_rows = 4
        self.n_cells = 4
        self.n_regions = self.n_grid_cols * self.n_grid_rows
        self.sim_duration = 30 #seconds
        self.time_interval = 1 #seconds
        self.epochs = self.sim_duration // self.time_interval
        self.epoch = 0
        self.n_worker_updates = 0

        self.grid = self.generate_grid()
        self.dependents_graph = self.generate_dependency_graph()
        self.required_ready_count = self.generate_required_ready_count()
        self.ready_neighbor_count = self.generate_ready_neighbor_count()
        self.prev_region_present = self.generate_prev_region_present()
        self.region_enqueued = self.generate_region_enqueued()
        self.ready_initial_queue()

    def register_worker(self, websocket, id):
        self.workers[id].append(websocket)

    def register_client(self, websocket):
        self.client = websocket

    def generate_prev_region_present(self):
        prev_region_present = np.zeros(shape=(self.epochs, self.n_grid_rows, self.n_grid_cols), dtype=bool)
        prev_region_present[0][:][:] = True #first grid is ready
        return prev_region_present

    def generate_region_enqueued(self):
        return np.zeros(shape=(self.epochs, self.n_grid_rows, self.n_grid_cols), dtype=bool)

    def update_grid(self, region, new_region_values, epoch):
        row, col = region
        self.grid[epoch][row][col] = new_region_values
        self.prev_region_present[epoch][row][col] = True

    def increment_dependents_and_enqueue(self, region, epoch):
        row, col = region
        for r, c in self.dependents_graph[(row, col)]:
            self.ready_neighbor_count[epoch + 1][r][c] += 1
            self.enqueue_tasks(r, c, epoch)
        self.enqueue_tasks(row, col, epoch)

    def enqueue_tasks(self, r, c, epoch):
        if self.ready_neighbor_count[epoch + 1][r][c] == self.required_ready_count[(r,c)] \
         and not self.region_enqueued[epoch + 1][r][c] and self.prev_region_present[epoch][r][c] == True:
            self.tasks_queue.append(self.task_payload((r,c), epoch))
            self.region_enqueued[epoch + 1][r][c] = True

    def ready_initial_queue(self):
        for r in range(self.n_grid_rows):
            for c in range(self.n_grid_cols):
                self.enqueue_tasks(r, c, 0)
        # print(self.enqueue_tasks)

    def generate_grid(self):
        rng = np.random.default_rng()
        grid = rng.random(size=(self.epochs,self.n_grid_rows, self.n_grid_cols, self.n_cells, self.n_cells))
        # grid = np.zeros(shape=(self.epochs,self.n_grid_rows, self.n_grid_cols, self.n_cells, self.n_cells))
        # grid[0][0][0][0][0] = 1
        # grid[0][1][1][0][0] = 1
        # grid[0][1][0][1][0] = 1
        # grid[0][0][1][0][1] = 1
        # grid[0][1][1][1][0] = 1
        # grid[0][0][1][1][1] = 1
        return grid
    
    def generate_ready_neighbor_count(self):
        ready_neighbor_count = np.zeros(shape=(self.epochs, self.n_grid_rows, self.n_grid_cols))

        for init_row, init_col in self.required_ready_count.keys():
            ready_neighbor_count[1][init_row][init_col] = self.required_ready_count[(init_row, init_col)]
        # print('ready neighbor count:', ready_neighbor_count)
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
        # print('dependency graph', dependency_graph)
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
        # print('required ready count: ', required_count)
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
        return payload
