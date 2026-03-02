import json

MESSAGES = {
    'scheduler' : {
        'task_assign' : {
            'type': 'task_assign',
        }
    },

    'worker': { 
        'register' : {
            'type': 'register'
        }
    },

    'client': {
        'register': {
            'type': 'register'
        }
    }
}


async def send(sender, websocket, type, payload={}):
    message = MESSAGES[sender][type]
    message['payload'] = payload
    await websocket.send(json.dumps(message))