# message.py
import json

class Message:
    def __init__(self, message_type: str = "", payload=None):
        self.message_type = message_type
        self.payload = payload if payload is not None else {}

    def to_json(self) -> str:
        return json.dumps({
            "message_type": self.message_type,
            "payload": self.payload,
        })

    @classmethod
    def from_json(cls, s: str) -> "Message":
        data = json.loads(s)
        return cls(
            message_type=data.get("message_type", ""),
            payload=data.get("payload", {})
        )
