import socket
from config import FORWARD_IP, FORWARD_PORT

def forward_data(data):
    """Forward data to predefined IP and port, and return the response."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((FORWARD_IP, FORWARD_PORT))
        sock.sendall(data)
        return sock.recv(1024)
