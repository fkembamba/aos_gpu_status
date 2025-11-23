# server.py
import zmq
from message import Message
from status_report import Status_Report

def server(bind_addr="tcp://*:5555"):
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(bind_addr)

    print(f"[SERVER] Listening on {bind_addr}")

    while True:
        raw = socket.recv_string()
        req = Message.from_json(raw)
        print(f"[SERVER] Received: type={req.message_type}, payload={req.payload}")

        if req.message_type == "REQ_STATUS":
            reply_msg = Status_Report()
        else:
            reply_msg = Message(
                "ERROR",
                {"reason": f"Unknown message_type: {req.message_type}"}
            )

        socket.send_string(reply_msg.to_json())
        print(f"[SERVER] Sent reply of type={reply_msg.message_type}")

if __name__ == "__main__":
    server()
