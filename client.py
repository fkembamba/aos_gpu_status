# client.py
import argparse
import zmq
from message import Message
from request_status import Request_Status

def client(server_addr: str):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect(server_addr)

    req = Request_Status()
    print(f"[CLIENT] Sending request: {req.message_type}")
    socket.send_string(req.to_json())

    raw_reply = socket.recv_string()
    reply = Message.from_json(raw_reply)

    print(f"[CLIENT] Received reply type={reply.message_type}")
    print(f"[CLIENT] Payload: {reply.payload}")

    if reply.message_type == "STATUS_REPORT":
        total = reply.payload.get("memory_total_mb")
        used = reply.payload.get("memory_used_mb")
        print(f"[CLIENT] GPU memory: {used} / {total} MB used")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--server-ip",
        required=True,
        help="IP or hostname of the GPU server (e.g., 10.31.12.12)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=5555,
        help="Port the server is listening on (default: 5555)"
    )
    args = parser.parse_args()

    addr = f"tcp://{args.server_ip}:{args.port}"
    client(addr)
