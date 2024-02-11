import socket
from concurrent import futures as f

hostname = socket.gethostname()
IP = str(socket.gethostbyname(hostname))  # here we get IP of a current PC
PORT = 5000


def run_server(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = ip, port
    sock.bind(server)
    try:
        while True:
            data, address = sock.recvfrom(1024)
            print(f"Recieved data: {data.decode()} from {address}")
            sock.sendto(data, address)
            print(f"Send data: {data.decode()} to: {address}")

    except KeyboardInterrupt:
        print("Destroy server")
    finally:
        sock.close()


if __name__ == "__main__":
    run_server(IP, PORT)
