class Scheduler():    
    def __init__(self):
        self.client = ''
        self.workers = []
        self.task = ''
        self.status = 0
        self.n_grid_cols = 3
        self.n_grid_rows = 3
        self.n_regions = self.n_grid_cols * self.n_grid_rows
        self.n_region_precision = 5
        self.regions = self.collect_regions(self.n_grid_cols, self.n_grid_rows)
        self.sim_duration = 10 #seconds
        self.time_interval = 1 #seconds
        self.epochs = self.sim_duration / self.time_interval
        self.boundary_conditions = self.assign_boundary_conditions()
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
    
    def assign_boundary_conditions(self):
        return [[[[False for _ in range(self.n_region_precision)] for _ in range(self.n_region_precision)] for _ in range(self.n_grid_cols)] for _ in range(self.n_grid_rows)]
    
    def collect_regions(self, n_cols, n_rows):
        return [[m,n] for n in range(n_cols) for m in range(n_rows)]
        # for m in range(n_rows):
        #     for n in range(n_cols):
        #         res.append
        # def permute(curr):
        #     if len(curr) == 2:
        #         res.append(curr.copy())
        #         return
            
        #     for i in range(n_rows):
        #         curr.append(i)
        #         permute(curr)
        #         curr.pop()
        # permute([])
        # return res

