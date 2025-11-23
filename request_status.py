# request_status.py
from message import Message

class Request_Status(Message):
    def __init__(self):
        super().__init__("REQ_STATUS", payload={})
