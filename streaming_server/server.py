import pickle
import socket
import struct
import threading
import cv2
import imutils

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print('HOST IP:', host_ip)
port = 5050
socket_address = (host_ip, port)
server_socket.bind(socket_address)
server_socket.listen()
print("Listening at", socket_address)


def handle_client(address, client_socket):
    try:
        print('CLIENT {} CONNECTED!'.format(address))

        video_name, resolution = pickle.loads(client_socket.recv(1024))
        video = find_video(client_socket, resolution, video_name)
        send_video(video, client_socket)

        client_socket.close()

    except Exception as e:
        print(f"CLIENT {address} DISCONNECTED UNEXPECTEDLY, ERROR = {e}")
        pass


def send_video(video, client_socket):
    while video.isOpened():
        img, frame = video.read()
        if not img:
            print(f'VIDEO FINISHED!')
            break
        frame = imutils.resize(frame, width=1200)
        a = pickle.dumps(frame)
        message = struct.pack("Q", len(a)) + a
        client_socket.sendall(message)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
    client_socket.close()
    video.release()


def find_video(client_socket, resolution, video_name):

    # noinspection PyArgumentList
    video = cv2.VideoCapture(f'../videos/{resolution}/{video_name}')

    if not video.isOpened():
        error_message = f"Error: Video {video} not found for resolution {resolution}."
        print(error_message)
        client_socket.send(pickle.dumps([404, error_message]))
        client_socket.close()
    else:
        client_socket.send(pickle.dumps([204, ""]))

    return video


def main():
    while True:
        client_socket, address = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(address, client_socket))
        thread.start()
        print("TOTAL CLIENTS ", threading.activeCount() - 1)


if __name__ == "__main__":
    main()
