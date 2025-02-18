import socket
import cv2
import time

def register_user(client_socket):
    # client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # host = '127.0.0.1'
    # port = 12345
    # client_socket.connect((host, port))
    
    camera = cv2.VideoCapture(0)

# Allow the camera to warm up

# Capture an image
    ret, frame = camera.read()
    print("Frame capture successful:", ret)
    x=76

    for i in range(x):  # Capture x frames
        ret, frame = camera.read()
    # cv2.imwrite(f'C:/Users/Anas/Desktop/img/2/image_{i}.jpg', frame)
    # print("Frame capture successful:", ret)

# Save the image
    cv2.imwrite(r'D:/FAST_NU/5th Sem/Blockchain/Project\reg.jpg', frame)

# Release resources
    camera.release()

    time.sleep(1)

    file_name = r'D:/FAST_NU/5th Sem/Blockchain/Project\reg.jpg'

    with open(file_name, 'rb') as file:
        data = file.read(4096)
        while data:
            client_socket.sendall(data)
            data = file.read(4096)

    print("Image sent successfully.")
    # client_socket.close()

    #send a msg from server that {RECEIVED}


def verify_user(client_socket):
    camera = cv2.VideoCapture(0)

# Allow the camera to warm up

# Capture an image
    ret, frame = camera.read()
    print("Frame capture successful:", ret)
    x=76

    for i in range(x):  # Capture x frames
        ret, frame = camera.read()
        # print("loop")
    # cv2.imwrite(f'C:/Users/Anas/Desktop/img/2/image_{i}.jpg', frame)
    # print("Frame capture successful:", ret)

# Save the image
    cv2.imwrite(r'D:/FAST_NU/5th Sem/Blockchain/Project\ver.jpg', frame)

# Release resources
    camera.release()

    time.sleep(1)

    file_name = r'D:/FAST_NU/5th Sem/Blockchain/Project\ver.jpg'
    print("started to write")

    with open(file_name, 'rb') as file:
        data = file.read(4096)
        while data:
            client_socket.sendall(data)
            data = file.read(4096)

    print("Image sent successfully.")    


def main():
    host = '172.16.86.166'
    port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    print("1) Registration\n2) Verification")
    choice = int(input("Enter your choice (1 or 2): "))

    # Send the client's choice to the server
    client_socket.send(str(choice).encode('utf-8'))

    if choice == 1:
        register_user(client_socket)
    elif choice == 2:
        verify_user(client_socket)
        # print("Verify")
    else:
        print("Invalid choice.")

    client_socket.close()



if __name__ == "__main__":
    main()
