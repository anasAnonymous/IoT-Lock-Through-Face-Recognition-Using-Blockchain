# Face Recognition Program Using Blockchain and IoT

This project allows a client to capture an image using a webcam and send it to a server over a TCP socket connection.  

## 📌 How It Works  
1. The server listens for a connection.  
2. The client captures an image using a webcam and sends it to the server.  
3. The server receives and saves the image.  

## Prerequisites  
Make sure you have Python installed, then install the required libraries.

## 📂 Folder Structure
Before running the programs, ensure these directories exist:
- A folder for received images
- A folder for storing captured images

## 🛠 How to Run
### Start the Server
Run the following command to start the server:
```bash
python server.py
```
The server will wait for an image from the client.

### Run the Client
Once the server is running, start the client:
```bash
python client.py
```
The client will capture an image, save it, and send it to the server.

## 🎯 Features
- Uses OpenCV to capture images.
- Transfers images over a TCP connection.
- Saves received images to a predefined folder.

## 🔧 Troubleshooting
- If the image is not received, check if the directories exist.
- Ensure that both scripts are running on the same IP (127.0.0.1) and port (12345).
