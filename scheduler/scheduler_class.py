class Scheduler():    
    def __init__(self):
        self.workers = set()

    def register(self,id):
        self.workers.add(id)
        print('workers registered:', self.workers)
