import socket 

def create_message(correlation_id):
    id_bytes = correlation_id.to_bytes(4, byteorder='big')
    return len(id_bytes).to_bytes(4, byteorder='big') + id_bytes

def handle_client(client_socket, client_address):
    # First read the length (4 bytes)
    length_bytes = client_socket.recv(4)
    message_length = int.from_bytes(length_bytes, byteorder='big')
    
    # Read the entire message
    message = client_socket.recv(message_length)
    
    # Correlation ID is at bytes 4-8 of the message
    correlation_id = int.from_bytes(message[4:8], byteorder='big')
    
    client_socket.sendall(create_message(correlation_id))
    client_socket.close()

def main():
    print("Program Logs")
    server = socket.create_server(("localhost", 9092), reuse_port=True)  # Create a new socket server
    while True:
        print("Waiting for client to connect")
        client_socket, client_address = server.accept()  # Wait for client to connect
        print(f"Client connected: {client_address}")
        handle_client(client_socket, client_address)

if __name__ == "__main__":
    main()
