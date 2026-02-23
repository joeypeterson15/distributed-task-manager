class Scheduler():    
    def __init__(self):
        self.client = None
        self.workers = []
        self.tasks = []

    def register_worker(self, id):
        self.workers.append(id)
        print('workers registered:', self.workers)

    def register_client(self, id):
        self.client = id
    def register_tasks(self, tasks):
        self.tasks = tasks

    def assign_workers(self):
        # configure tasks:
        #   figure out which tasks can be parallelized or not by dependency graph
        #   create new graph based on current tasks
        # 
        # assign workers:
        #   keep track of what items depend on others(can't be parallelized)
        #   get worker status, assign new tasks to workers when work complete
        # update client:
        #   tell client status of workers and when tasks are completed/show result
        return
