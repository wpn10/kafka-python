import socket 

def create_message(correlation_id, error_code):
    id_bytes = correlation_id.to_bytes(4, byteorder='big')
    error_code_bytes = error_code.to_bytes(2, byteorder='big', signed=True)
    
    # Create the response body for APIVersions
    api_key = 18
    min_version = 0
    max_version = 4
    api_key_bytes = api_key.to_bytes(2, byteorder='big')
    min_version_bytes = min_version.to_bytes(2, byteorder='big')
    max_version_bytes = max_version.to_bytes(2, byteorder='big')
    
    # Construct the response body
    response_body = api_key_bytes + min_version_bytes + max_version_bytes
    
    # Calculate the total message length
    total_length = len(id_bytes + error_code_bytes + response_body)
    
    # Construct the full message
    return total_length.to_bytes(4, byteorder='big') + id_bytes + error_code_bytes + response_body

def handle_client(client_socket, client_address):
    # First read the length (4 bytes)
    length_bytes = client_socket.recv(4)
    message_length = int.from_bytes(length_bytes, byteorder='big')
    
    # Read the entire message
    message = client_socket.recv(message_length)
    
    # Correlation ID is at bytes 4-8 of the message
    correlation_id = int.from_bytes(message[4:8], byteorder='big')
    
    # Request API version is at bytes 6-8 of the message
    request_api_version = int.from_bytes(message[6:8], byteorder='big')
    
    # Check if the request API version is supported
    if request_api_version > 4:
        error_code = 35  # UNSUPPORTED_VERSION
    else:
        error_code = 0  # No error
    
    client_socket.sendall(create_message(correlation_id, error_code))
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
