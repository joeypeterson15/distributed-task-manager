import cmd
import requests
import os
from dotenv import load_dotenv
import websockets

load_dotenv()
port = os.getenv("PORT")
    
class Client():
    def call():
        r = requests.get(f'http://localhost:{port}')
        print('response', r)

if __name__ == "__main__":
    Client.call()