import argparse
import socket

from chess.protocol import JsonConnection

def accept_player(client_socket: socket.socket, color: str) -> tuple[socket.socket, JsonConnection, str, tuple[str, int]]:
    '''
    wait for a player to connect
    return the socket, JSON helper, player name and address
    '''

    # show what the server is waiting for
    print(f"waiting for {color} player...")

    # wait until the connection here, accept is blocking
    client_socket, address = server_socket.accept()

    # show the connection
    print(f"{color} player connected from {address}")

    # using helper class to send/receive dictionaries instead of JSON
    connection = JsonConnection(client_socket)

    # send welcome message to client to show connection
    connection.send({
        "type": "welcome",
        "message": "connected to chess"
    })

    # wait for join message from the client
    message = connection.receive()
    print(f"{color} player sent: {message}")

    # we expect "join" type "{name}" message
    if (message.get("type") != "join"):
        # not a join message, inform and error
        connection.send({
            "type": "error",
            "message": "expected a join message"
        })

        # close the socket and raise error
        client_socket.close()
        raise ValueError("client didn't send a join message")
    
    # get the player name
    player_name = received_message.get("name")

    # confirm name was received, tell player the color
    connection.send({
        "type": "color_and_name",
        "color": color,
        "message": f"server received name {player_name}, you are playing {color}"
    })

    return client_socket, connection, player_name, address


def start_server(host: str, port: int) -> None:
    '''
    start the TCP server
    '''

    # IPv4, TCP and close when done automatically
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # using parameters for socket 
        server_socket.bind((host, port))

        # listen for TCP connections
        server_socket.listen(2)

        print(f"server listening on {host}:{port}")

        # first connection
        white_socket, white_connection, white_name, white_address = accept_player(server_socket, "white")
        print(f"{white_name} connected from {white_address}, and will play white")

        # second connection
        black_socket, black_connection, black_name, black_address = accept_player(server_socket, "black")
        print(f"{black_name} connected from {black_address}, and will play black")
        print("both players connected")

        # handle client until disconnect
        with white_socket, black_socket:

            white_connection.send({
                "type": "game_start",
                "color": "white",
                "opponent": black_name
            })

            black_connection.send({
                "type": "game_start",
                "color": "black",
                "opponent": white_name
            })

            #
            #
            # CHESS WILL START HERE
            #
            #

def main() -> None:
    '''
    '''

    # reading host and port from console, setting options
    parser = argparse.ArgumentParser(description="console chess server")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5000)

    # actually read
    args = parser.parse_args()

    # start the server using given values
    start_server(args.host, args.port)

if __name__ == "__main__":
    main()
    



