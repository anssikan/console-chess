import argparse
import socket

from chess.protocol import JsonConnection

def handle_client(client_socket: socket.socket, address: tuple[str,int]) -> None:
    '''
    handles one client connection
    address is ("IP", port)
    '''

    # show that there is a new connection
    print(f"client connection: {address}")

    # using helper class 
    connection = JsonConnection(client_socket)

    # send welcome message to client
    welcome_message = {
        "type": "welcome",
        "message": "connected to chess"
    }
    connection.send(welcome_message)

    # recieve a message from client
    received_message = connection.receive()
    print(f"client sent: {message}")

    # we expect "join" type "{name}" message
    if (received_message.get("type") != "join"):
        return
    
    # get the name
    player_name = received_message.get("name")

    # confirm name was received
    received_message = {
        "type": "received",
        "message": f"server received name {player_name}"
    }
    connection.send(received_message)

def start_server(host: str, port: int) -> None:
    '''
    start the TCP server
    '''

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # using parameters for socket 
        server_socket.bind((host, port))

        # listen for TCP connections
        server_socket.listen()

        print(f"server listening on {host}:{port}")

        # wait until a client connects
        client_socket, address = server_socket.accept()

        # handle client until disconnect
        with client_socket:
            handle_client(client_socket, address)
        
        print("client disconnected, server off")

def main() -> None:
    '''
    '''

    # reading host and port from console, setting options
    parser = argparse.ArgumentParser(description="console chess server")
    parser.add_arguement("--host", default="127.0.0.1")
    parser.add_arguement("--port", type=int, default=5000)

    # actually read
    args = parser.parse_args()

    # start the server using given values
    start_server(args.host, args.port)

if __name__ == "__main__":
    main()
    



