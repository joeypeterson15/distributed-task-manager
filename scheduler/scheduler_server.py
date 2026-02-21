import os
from dotenv import load_dotenv
from scheduler_class import Scheduler
from http.server import HTTPServer, BaseHTTPRequestHandler

load_dotenv()
port = int(os.getenv("PORT"))

class SchedulerHTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200, 'received')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        return
        
    def do_REGISTER(self, worker):
        self.scheduler.register(worker)
        self.send_response(200, 'worker registered')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

# class Server():
def run(server_class=HTTPServer, handler_class=SchedulerHTTPHandler):
    handler_class.scheduler = Scheduler()
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == "__main__":
    print('Server listening on PORT 8000')
    run()