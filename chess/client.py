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
        message = connection.receive()
        print(f"Server sent: {message}")

        # send expected name message
        connection.send({
            "type": "join",
            "name": name
        })

        # wait for server reply
        message = connection.receive()
        print(f"Server sent: {message}")

        # get color 
        color = message.get("color")
        print(f"i will play {color}")

        # wait for game to start!!
        message = connection.receive()
        print(f"Server sent: {message}")

def main() -> None:
    # example command:
    # python -m chess.client --host 127.0.0.1 --port 5000 --name John

    # reading options
    parser = argparse.ArgumentParser(description="console chess server")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--name", required=True)

    # get the arguments
    args = parser.parse_args()

    # run client logic
    run_client(args.host, args.port, args.name)

if __name__ == "__main__":
    main()




