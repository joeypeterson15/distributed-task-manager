import cmd
import requests
import os
from dotenv import load_dotenv

load_dotenv()
port = os.getenv("PORT")
# class ClientShell(cmd.Cmd):
    
class Client():
    def execute(self):
        self.call()
    def call():
        r = requests.get(f'http://localhost:{port}')
        print('response', r)

if __name__ == "__main__":
    Client.execute()