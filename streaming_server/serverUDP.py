import pickle
import threading

import cv2, imutils, socket
import numpy as np
import time
import base64

BUFF_SIZE = 65536
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
host_name = socket.gethostname()
host_ip = '127.0.1.1'
print(host_ip)
port = 5050
socket_address = (host_ip, port)
server_socket.bind(socket_address)
print('Listening at:', socket_address)

fps, st, frames_to_count, cnt = (0, 0, 20, 0)


def handle_client(data, address):
    print('CLIENT {} CONNECTED!'.format(address))


def find_video(address, resolution, video_name):
    print("chegou aqui")
    print(address)
    video = cv2.VideoCapture(f'../videos/{video_name}')
    print(video)
    if not video.isOpened():
        error_message = f"Error: Video {video_name} not found for resolution {resolution}."
        print(error_message)

        server_socket.sendto(pickle.dumps([404, error_message]), address)
    else:
        server_socket.sendto(pickle.dumps([204, ""]),address)

    return video


def main():
    print("WAITING FOR CLIENTS...")
    while True:
        data, address = server_socket.recvfrom(1024)
        msg = pickle.loads(data)
        if msg[0] == 'REPRODUZIR_VIDEO':
            thread = threading.Thread(target=handle_client, args=(data, address))
            thread.start()
            print("TOTAL CLIENTS ", threading.activeCount() - 1)
            resposta = ['ENVIAR RESOLUCAO']
            server_socket.sendto(pickle.dumps(resposta), address)
        elif msg[0] == "VIDEO/RESOLUCAO":
            print("Procurando video")
            video = msg[1]
            resolucao = msg[2]
            video = find_video(address, resolucao, video)
            while True:
                msg, client_addr = server_socket.recvfrom(BUFF_SIZE)
                print('GOT connection from ', client_addr)
                WIDTH = 400
                while video.isOpened():
                    _, frame = video.read()
                    frame = imutils.resize(frame, width=WIDTH)
                    encoded, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
                    message = base64.b64encode(buffer)
                    server_socket.sendto(message, client_addr)
                    frame = cv2.putText(frame, 'FPS: ' + str(fps), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    cv2.imshow('TRANSMITTING VIDEO', frame)
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('q'):
                        server_socket.close()
                        break
                    if cnt == frames_to_count:
                        try:
                            fps = round(frames_to_count / (time.time() - st))
                            st = time.time()
                            cnt = 0
                        except:
                            pass
                    cnt += 1

if __name__ == "__main__":
    main()