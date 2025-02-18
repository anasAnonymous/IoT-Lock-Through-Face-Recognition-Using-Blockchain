import socket
import multichain
import binascii
import numpy as np
import time
import io
import base64
import hashlib  # Import the hashlib module
from PIL import Image
import sys
import face_recognition

# MultiChain credentials
rpcuser = "multichainrpc"
rpcpassword = "BvGwbURySSahsZmF2oRyqS2evjM43WAzq5DAERa3iUg4"
rpchost = "127.0.0.1"
rpcport = "4770"
chainname = "newBlockChain"

# Create a MultiChain client
mc = multichain.MultiChainClient(rpchost, rpcport, rpcuser, rpcpassword)

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define host and port for the messaging server
host = '172.16.86.166'
port = 12345

# Bind the socket to a specific address and port
server_socket.bind((host, port))

# Listen for incoming connections (max 5 connections in the queue)
server_socket.listen(5)

print(f"Server listening on {host}:{port}")

# Accept connections from clients
client_socket, addr = server_socket.accept()
print(f"Connection from {addr}")

def receive_image():
    # Receive file
    time.sleep(5)
    with open(r'C:\Users\Anas\Desktop\fr/recieved_image.jpg', 'wb') as file:
        data = client_socket.recv(170000)
        while data:
            file.write(data)
            data = client_socket.recv(170000)



def publish_image():
    image_path = r'C:\Users\Anas\Desktop\fr/recieved_image.jpg'

    # Read the image
    image = Image.open(image_path)

    # Convert image to base64 format
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='JPEG')
    image_data_base64 = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')

    variable_size = sys.getsizeof(image_data_base64)
    print(variable_size)
    # Hash the base64-encoded image data using SHA-256
    sha256_hash = hashlib.sha256(image_data_base64.encode('utf-8')).hexdigest()

    # Create a JSON structure with the SHA-256 hash and base64-encoded image data
    image_json = {"sha256_hash": sha256_hash, "image_data_base64": image_data_base64}

    # Publish the JSON structure to the MultiChain stream
    mc.publish('bbfr', 'key1', {'json': image_json})

    print("Image hash and base64-encoded data published on the stream.")


def fetch_image():
    print("i am in fetch")
    stream_items = mc.liststreamitems("bbfr")
    if stream_items:
        fetched_data = stream_items[-1].get('data', {})

        # Access the 'json' field or an alternative field based on your data structure
        fetched_json = fetched_data.get('json', {})

        # Retrieve the SHA-256 hash and base64-encoded image data
        sha256_hash = fetched_json.get('sha256_hash', '')
        encoded_image = fetched_json.get('image_data_base64', '')

        # Verify the integrity of the image data using SHA-256
        if sha256_hash == hashlib.sha256(encoded_image.encode('utf-8')).hexdigest():
            # Decode the base64-encoded image data
            decoded_image = base64.b64decode(encoded_image)

            # Convert the decoded image data to a Pillow Image
            image = Image.open(io.BytesIO(decoded_image))

            # Save or send the image to the client (you can choose either option)
            image_path = r'C:/Users/Anas/Desktop/bnc\decoded_image.jpg'
            image.save(image_path, format='JPEG')

            # Send the image to the client
            with open(image_path, 'rb') as image_file:
                image_data = image_file.read()
                client_socket.send(image_data)

            print("Image sent to client.")
        else:
            print("Image integrity verification failed.")

    else:
        print("No data available.")

    comparison()


#compare the images 
def comparison(): 
    print("I am in face comparison")
    image1 = face_recognition.load_image_file(r'C:/Users/Anas/Desktop/bnc\decoded_image.jpg')
    image2 = face_recognition.load_image_file(r'C:/Users/Anas/Desktop/fr\recieved_image.jpg')

    face_locations1 = face_recognition.face_locations(image1)
    face_encodings1 = face_recognition.face_encodings(image1, face_locations1)

    face_locations2 = face_recognition.face_locations(image2)
    face_encodings2 = face_recognition.face_encodings(image2, face_locations2)

    # print("Face locations 1:", face_locations1)
    # print("Face locations 2:", face_locations2)

    # print("Image 1 dimensions:", image1.shape)  # Assuming face_recognition uses numpy arrays
    # print("Image 2 dimensions:", image2.shape)

    # print("1 : ", face_encodings1)
    # print("2 : ", face_encodings2)
    # Compare faces
    if face_encodings1 and face_encodings2:
     
        similarity = face_recognition.face_distance([face_encodings1[0]], face_encodings2[0])
        similarity_percentage = (1 - similarity[0]) * 100
        print("Similarity % : ", similarity_percentage)
        if similarity_percentage > 70:
            client_socket.send(b"Face Verified, ACCESS GRANTED :) ")
        else:
            client_socket.send(b"Who Are You, ACCESS DENIED :( ")
    else:
        print("Error in face encodings")
        client_socket.send(b"Error")
    

def main():
    option = int(client_socket.recv(1024).decode('utf-8'))
    
    if option == 1:
        print("Choice received:", option)
        receive_image()
        publish_image()
    elif option == 2:
        print("Choice received:", option)
        receive_image()
        fetch_image()
    else:
        print("Choice received:", option)
        print("Invalid option.")

# Call the main function
main()

# Close the connection
client_socket.close()
server_socket.close()

