import argparse
import socket

from chess.protocol import JsonConnection

def run_client(host: str, port: int, name: str) -> None:
    '''
    connect to server with a name
    '''

    print(f"connecting to {host}:{port}!")

    with socket.create_connection((host, port), timeout=5) as client_socket:
        # using the helper class
        connection = JsonConnection(client_socket)

        # wait for server welcome message
        server_message = connection.receive()
        print(f"Server sent: {server_message}")

        # send expected name message
        name_message = {
            "type": "join",
            "name": name
        }
        connection.send(name_message)

        # wait for server reply
        server_message = connection.receive()
        print(f"Server sent: {server_message}")

def main() -> None:
    # example command:
    # python -m chess.client --host 127.0.0.1 --port 5000 --name John

    # reading options
    parser = argparse.ArgumentParser(description="console chess server")
    parser.add_arguement("--host", default="127.0.0.1")
    parser.add_arguement("--port", type=int, default=5000)
    parser.add_arguement("--name", required=True)

    # get the arguements
    args = parser.parse_args()

    # run client logic
    run_client(args.host, args.port, args.name)

if __name__ == "__main__":
    main()




