import cv2
import pickle
import socket
import struct

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '127.0.1.1'
port = 5050
BUFFER_SIZE = 2430162


def main():
    client_socket.connect((host_ip, port))

    client_socket.send(pickle.dumps(["teste3.mkv", "480p"]))

    if has_video():
        show_video()


def show_video():
    while True:
        frame_data, data = get_frame_data()
        frame = pickle.loads(frame_data)
        cv2.imshow(f"FROM {host_ip}", frame)
        if cv2.waitKey(1) == ord('q'):
            break


def has_video():
    found_video_code, found_video_error_message = pickle.loads(client_socket.recv(1024))
    if found_video_code == 404:
        print(found_video_error_message)
        return False
    return True


def get_frame_data():
    data = b""
    payload_size = struct.calcsize("Q")

    data += client_socket.recv(4 * 1024)
    data = data[payload_size:]
    while len(data) < BUFFER_SIZE:
        data += client_socket.recv(4 * 1024)  # TODO descobrir como fazer client entender que video acabou
    frame_data = data[:BUFFER_SIZE]

    return frame_data, data[BUFFER_SIZE:]


if __name__ == "__main__":
    main()
