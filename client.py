import socket
import cv2
import time

def send_image():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 12345
    client_socket.connect((host, port))
    
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
    cv2.imwrite(r'C:\Users\Anas\Desktop\imageSharing/image3.jpg', frame)

# Release resources
    camera.release()

    time.sleep(1)

    file_name = r'C:\Users\Anas\Desktop\imageSharing/image3.jpg'

    with open(file_name, 'rb') as file:
        data = file.read(4096)
        while data:
            client_socket.sendall(data)
            data = file.read(4096)

    print("Image sent successfully.")
    client_socket.close()

if __name__ == "__main__":
    send_image()
