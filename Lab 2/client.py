import socket
import cv2 # type: ignore

def run_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = "10.5.116.247"
    server_port = 8000
    client.connect((server_ip, server_port))

    while True:
        msg = input("Enter message: ")
        client.send(msg.encode("utf-8"))

        # Send image if requested
        if msg.lower() == "send image":
            response = client.recv(1024).decode("utf-8")
            
            if response.lower() == "ready":
                # Read image file
                img_path = 'robot.jpg'  # Specify the path to your image
                img = cv2.imread(img_path)

                # Convert image to bytes
                _, img_encoded = cv2.imencode('.jpg', img)
                img_data = img_encoded.tobytes()

                # Send image size
                client.send(str(len(img_data)).encode("utf-8"))
                client.recv(1024)  # Wait for size received acknowledgment

                # Send the image data
                client.sendall(img_data)
                response = client.recv(1024).decode("utf-8")
                print(response)

        # If server sent "closed" in the payload, break out of the loop and close the socket
        response = client.recv(1024).decode("utf-8")
        if response.lower() == "closed":
            break

        print(f"Received: {response}")

    client.close()  # Close client socket (connection to the server)
    print("Connection to server closed")

run_client()
