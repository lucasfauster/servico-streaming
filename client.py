import cv2
import pickle
import socket
import struct

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '127.0.1.1'
port = 5050


def main():
    client_socket.connect((host_ip, port))
    resAvaliable = ["240p", "480p", "720p"]
    print('Avaliable resolutions: 240p/ 480p/ 720p')
    resolution = input('Select one resolution: ')

    if resolution not in resAvaliable: 
        print('Resolution not found')
        return

    client_socket.send(pickle.dumps(["video.mkv", resolution]))

    if has_video():
        show_video()


def show_video():
    data = b""
    while True:
        frame_data, data = get_frame_data(data)

        if frame_data is None:
            print("VIDEO FINISHED!")
            client_socket.close()
            break

        frame = pickle.loads(frame_data)
        cv2.imshow(f"FROM {host_ip}", frame)
        if cv2.waitKey(1) == ord('q'):
            break


def get_frame_data(data):
    payload_size = struct.calcsize("Q")
    while len(data) < payload_size:
        packet = client_socket.recv(4 * 1024)
        if not packet:
            return None, data
        data += packet
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q", packed_msg_size)[0]
    while len(data) < msg_size:
        data += client_socket.recv(4 * 1024)
    frame_data = data[:msg_size]
    data = data[msg_size:]
    return frame_data, data


def has_video():
    found_video_code, found_video_error_message = pickle.loads(client_socket.recv(1024))
    if found_video_code == 404:
        print(found_video_error_message)
        return False
    return True


if __name__ == "__main__":
    main()
