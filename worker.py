# workers should be able to:
    # register with the scheduler
    # complete tasks
    # update scheduler on status
    # 
import sys
import requests
import os
from dotenv import load_dotenv

load_dotenv()
port = os.getenv("PORT")

class Worker():
    def __init__(self, id):
        self.id = id

    def registerWithScheduler(self):
        r = requests.post("http://localhost:8000/register", json=self)


def gen_workers(n):
    for id in range(n):
        w = Worker(id)
        w.registerWithScheduler()


if __name__ == "__main__"():
    if len(sys.argv) >= 1:
        n_workers = sys.argv[0]
