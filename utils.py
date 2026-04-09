import json

SERVER_MESSAGE = {
    'task_assign' : {
        'type': 'task_assign',
        'payload': {} 
    }
}

WORKER_MESSAGE = {
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
    },

    'task_complete' : {
        'type': 'task_complete',
        'payload': {
            'new_region': ''
        }
    },

    'task_request' : {
        'type': 'task_request',
        'payload': {

        }
    }
}
