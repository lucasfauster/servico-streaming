import pickle
import socket
import struct
import threading
import cv2
import imutils

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print('HOST IP:', host_ip)
port = 5050
socket_address = (host_ip, port)
server_socket.bind(socket_address)


def handle_client(data, address):
    print('CLIENT {} CONNECTED!'.format(address))
    # recebe o nome do video e a resolução que o cliente escolheu
    #(video_name, resolution), adress = pickle.loads(server_socket.recvfrom(1024))
    # carrega o video dos arquivos
    #video = find_video(resolution, video_name)
    # renderiza o video para o cliente
    #send_video(adress, video, resolution)


def send_video(address, video, resolution):
    while video.isOpened():
        img, frame = video.read()
        if not img:
            print(f'VIDEO FINISHED!')
            break

        # definindo a resolução
        resolSize = {"240p": 240, "480p": 480, "720p": 720}
        frame = imutils.resize(frame, width=int(resolSize.get(resolution)*0.7778), height=resolSize.get(resolution))
        # serializa o frame do vídeo
        a = pickle.dumps(frame)
        # empacota o frame serializado
        message = struct.pack("Q", len(a)) + a
        server_socket.sendto(message, address)
        # recebe um input do teclado do cliente
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
    video.release()


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
            send_video(address, video, resolucao)


if __name__ == "__main__":
    main()