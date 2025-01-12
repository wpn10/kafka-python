import socket 

def create_message(correlation_id):
    id_bytes = correlation_id.to_bytes(4, byteorder='big')
    return len(id_bytes).to_bytes(4, byteorder='big') + id_bytes

def handle_client(client_socket, client_address):
    client_socket.recv(1024)
    client_socket.sendall(create_message(7))
    client_socket.close()

def main():
    print("Program Logs")
    server = socket.create_server(("localhost", 9092), reuse_port=True)  # Create a new socket server
    while True:
        client_socket, client_address = server.accept()  # Wait for client to connect
        handle_client(client_socket, client_address)

if __name__ == "__main__":
    main()
