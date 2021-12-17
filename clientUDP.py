# This is client code to receive video frames over UDP
import pickle
import sys

import cv2, imutils, socket
import numpy as np
import time
import base64

BUFF_SIZE = 65536
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
host_name = socket.gethostname()
host_ip = '127.0.1.1'
port = 6000


def has_video():
    msg, _ = client_socket.recvfrom(BUFF_SIZE)
    msg = pickle.loads(msg)
    if "REPRODUZINDO" in msg:
        return True
    else:
        print(f"ERRO: {msg}")
        return False


def select_video_and_resolution():
    resAvaliable = ["240p", "480p", "720p"]
    print('Avaliable resolutions: 240p/ 480p/ 720p')
    resolution = input('Select one resolution: ')

    if resolution not in resAvaliable:
        print('Resolution not found')
        return

    msg = pickle.dumps(['REPRODUZIR_VIDEO', 'video.mkv', resolution])

    client_socket.sendto(msg, (host_ip, port))


def run_video():
    client_socket.settimeout(1)
    try:
        while True:
            packet, _ = client_socket.recvfrom(BUFF_SIZE)
            print("Received {0} bytes of data.".format(sys.getsizeof(packet)))
            data = base64.b64decode(packet, ' /')
            npdata = np.fromstring(data, dtype=np.uint8)
            frame = cv2.imdecode(npdata, 1)
            cv2.imshow("RECEIVING VIDEO", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                client_socket.close()
                break
    except socket.timeout:
        print("VIDEO TERMINOU!")



def main():
    select_video_and_resolution()
    if has_video():
        run_video()


if __name__ == "__main__":
    main()
