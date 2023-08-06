import socket
import json
from hyperlite.event import Event

DATABASE = "test.db"


class Connection(socket.socket):
    def __init__(self, host, port):
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        Event.on('request', self.sendRequest)

    def connect(self, **kwargs) -> bool:
        try:
            super().connect((self.host, self.port))
            print("[#] Connected to Hyperlite Database ..")
            return True
        except Exception as ex:
            return False

    def sendRequest(self, data):
        super().send(str(data).encode("UTF-8"))
        response = super().recv(1024).decode('UTF-8')
        Event.emmit("response", response)


def generateInsertRequestSchema():
    return json.loads('''
    {
        "Insert": {
            "meta": {
                "Database": "db-1",
                "Collection": "col-1"
            }
        },
        "type": "Request"
    }
    ''')


def generateReadRequestSchema():
    return json.loads('''
    {
        "Read": {
            "meta": {
                "Database": "db-1",
                "Collection": "col-1"
            }
        },
        "type": "Request"
    }
    ''')


def generateReadOneRequestSchema():
    return json.loads('''
    {
        "ReadOne": {
            "meta": {
                "Database": "db-1",
                "Collection": "col-1"
            }
        },
        "type": "Request"
    }
    ''')


def generateUpdateRequestSchema():
    return json.load('''
    {
        "Update": {
            "meta": {
                "Database": "db-1",
                "Collection": "col-1",
            }
        },
        "type": "Request"
    }
    ''')


def generateReadByIdRequestSchema():
    return json.loads('''
        {
            "ReadById": {
                "meta": {
                    "Database": "db-1",
                    "Collection": "col-1"
                }
            },
            "type": "Request"
        }
        ''')


def generateDeleteRequestSchema():
    return json.loads('''
    {
        "Delete": {
            "meta": {
                "Database": "db-1",
                "Collection": "col-1",
                "Object_Id": "db-1.col-1.1"
            }
        },
        "type": "Request"
    }
    ''')
