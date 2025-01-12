import socket 


def main():
    print("Program Logs")
    server = socket.create_server(("localhost", 9092), reuse_port=True)  # Create a new socket server
    server.accept()  # Wait for client to connect

if __name__ == "__main__":
    main()
