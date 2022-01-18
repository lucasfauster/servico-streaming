import pickle
import threading
import cv2
import imutils
import socket
import base64

BUFF_SIZE = 65536
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
host_name = socket.gethostname()
host_ip = '127.0.1.1'
port = 5050
socket_address = (host_ip, port)
server_socket.bind(socket_address)
print('ESCUTANDO EM:', socket_address)

lista_videos = {'1': ['animacao.mp4', '240p'], '2': ['animacao.mp4', '480p'], '3': ['animacao.mp4', '720p'],
                '4': ['pacman.mp4', '240p'], '5': ['pacman.mp4', '480p'], '6': ['pacman.mp4', '720p']}


def find_video(video_name, resolution):
    # noinspection PyArgumentList
    video = cv2.VideoCapture(f'../videos/{resolution}/{video_name}')
    return video


def send_video(client_addr, video, resolution):
    vid = find_video(video, resolution)
    if vid.isOpened():
        print(f"ENVIANDO VÍDEO {video} COM RESOLUÇÃO {resolution} PARA {client_addr}")
        msg = f"REPRODUZINDO O VÍDEO {video}, COM RESOLUÇÃO {resolution}."
        server_socket.sendto(pickle.dumps(msg), client_addr)
        while vid.isOpened():
            img, frame = vid.read()
            if not img:
                print(f'ENVIO DO VÍDEO {video} COM RESOLUÇÃO {resolution} PARA {client_addr} TERMINADO!')
                break
            frame = imutils.resize(frame, width=600)
            encoded, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 50])
            message = base64.b64encode(buffer)
            server_socket.sendto(message, client_addr)
        vid.release()
    else:
        msg = f"VIDEO {video} NÃO ENCONTRADO PARA RESOLUÇÃO {resolution}."
        print(msg)
        msg = pickle.dumps(msg)
        server_socket.sendto(msg, client_addr)


def main():
    while True:
        msg, address = server_socket.recvfrom(BUFF_SIZE)
        msg = pickle.loads(msg)
        if type(msg) is list and msg[0] == 'REPRODUZIR_VIDEO':
            video = msg[1]
            resolution = msg[2]
            thread = threading.Thread(target=send_video, args=(address, video, resolution))
            thread.start()

        elif type(msg) is list and msg[0] == 'LISTAR_VIDEOS':
            msg = pickle.dumps(lista_videos)
            server_socket.sendto(msg, address)
            print("LISTA DE VIDEOS ENVIADA PARA", address)


if __name__ == "__main__":
    main()
