import json
import socket
from typing import Any

# string key and any value messages
Message = dict[str, Any]

class JsonConnection:
    '''
    sending and receiving JSON messages in TCP socket
    handles: dict -> JSON -> bytes -> socket 
        and: socket -> JSON -> dict
    messages end with "\n"
    '''

    def __init__(self, sock: socket.socket):
        # storing the socket object
        self.sock = sock
        # readable text from socket, bytes decoded into strings
        self.reader = sock.makefile("r", encoding="utf-8")

    def send(self, message : Message) -> None:
        '''
        sends given JSON message
        '''

        # dictionary to JSON string, with end indicator "\n"
        text = json.dumps(message) + "\n"

        # encode to bytes
        data = text.encode("utf-8")

        # send the message
        self.sock.sendall(data)
    
    def receive(self) -> Message:
        '''
        receives one JSON message, returns as dictionary
        '''

        # read until "\n"
        line = self.reader.readline()

        # empty string means other side closed connection
        if (line == ""):
            raise ConnectionError("Connection closed")

        # convert JSON string to dictionary
        try:
            message = json.loads(line)
        except json.JSONDecodeError as error:
            raise ValueError("invalid JSON received") from error
        
        # check received was a dictionary
        if not isinstance(message, dict):
            raise ValueError("received not a dictionary")
        
        return message


