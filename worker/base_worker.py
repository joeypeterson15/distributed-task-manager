import sys
import os
from dotenv import load_dotenv
import json
import websockets
import asyncio


MESSAGE = {
    'register' : {
        'type': 'register',
        'payload': {
            'name': 'worker',
            'id': ''
        }
    },

    'stdout' : {
        'type': 'stdout',
        'payload': {
            'message': ''
        } 
    }
}

class BaseWorker():
    def __init__(self):
        self.workers = []
        self.task_meta = ''

    async def send(self, websocket, type, **kwargs):
        message = MESSAGE[type]
        for key in kwargs.keys():
            message['payload'][key] = kwargs[key]
        await websocket.send(json.dumps(message))
