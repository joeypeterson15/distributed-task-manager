class Scheduler():    
    def __init__(self):
        self.workers = []

    def register(self, worker):
        self.workers.append(worker)