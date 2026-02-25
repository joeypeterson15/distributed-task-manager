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
        self.n_regions = self.n_grid_cols * self.n_grid_rows
        self.n_region_precision = 5
        self.regions = self.collect_regions(self.n_grid_cols, self.n_grid_rows)
        self.sim_duration = 10 #seconds
        self.time_interval = 1 #seconds
        self.epochs = self.sim_duration // self.time_interval
        self.curr_epoch = 0
        self.epochs_grid = self.gen_grid()
        # print('grid epochs: ', len(self.epochs_grid))
        # print('ind grid rows: ', len(self.epochs_grid[0]))
        # print('ind grid cols: ', len(self.epochs_grid[0][0]))
        # print('ind grid cols: ', len(self.epochs_grid[0][0]))
        # print('ind precision rows: ', len(self.epochs_grid[0][0][0]))
        # print('ind precision cols: ', len(self.epochs_grid[0][0][0][0]))

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
    
    def gen_grid(self):
        grid = [[[[False for _ in range(self.n_region_precision)] for _ in range(self.n_region_precision)] for _ in range(self.n_grid_cols)] for _ in range(self.n_grid_rows)]
        return [grid] * self.epochs
    
    def collect_regions(self, n_cols, n_rows):
        return [[m,n] for n in range(n_cols) for m in range(n_rows)]
    
    def gen_task_payload(self, region):
        return {
                'task' : region,
                'meta' : {
                    'n_grid_cols': self.n_grid_cols,
                    'n_grid_rows': self.n_grid_rows,
                    'region_precision': self.n_region_precision,
                    'initial_grid': self.epochs_grid[self.curr_epoch]
                },
            }


