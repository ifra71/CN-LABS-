import socket
import cv2 # type: ignore
import numpy as np # type: ignore

def run_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = "10.5.116.247"
    port = 8000
    server.bind((server_ip, port))
    server.listen(0)
    print(f"Listening on {server_ip}:{port}")
    
    client_socket, client_address = server.accept()
    print(f"Accepted connection from {client_address[0]}:{client_address[1]}")

    # Receive data from the client
    while True:
        request = client_socket.recv(1024)
        request = request.decode("utf-8")  # Convert bytes to string

        # Check for close connection request
        if request.lower() == "close":
            client_socket.send("closed".encode("utf-8"))
            break

        # Check for image transmission request
        if request.lower() == "send image":
            client_socket.send("ready".encode("utf-8"))

            # Receive image size
            img_size = int(client_socket.recv(1024).decode("utf-8"))
            client_socket.send("size received".encode("utf-8"))

            # Receive the image data
            img_data = b""
            while len(img_data) < img_size:
                img_data += client_socket.recv(1024)

            # Convert bytes to image
            np_img = np.frombuffer(img_data, np.uint8)
            img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

            # Display the image
            cv2.imshow('Received Image', img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            client_socket.send("image received".encode("utf-8"))

        print(f"Received: {request}")
        response = "accepted".encode("utf-8")  # Convert string to bytes
        client_socket.send(response)  # Send accept response to the client

    client_socket.close()  # Close connection socket with the client
    print("Connection to client closed")
    server.close()  # Close server socket

run_server()
