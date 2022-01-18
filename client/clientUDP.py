import pickle
import cv2
import socket
import numpy as np
import base64

BUFF_SIZE = 65536
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
host_name = socket.gethostname()
host_ip = '127.0.1.1'
port = 6000
video_name=""


def has_video():
    msg, _ = client_socket.recvfrom(BUFF_SIZE)
    msg = pickle.loads(msg)
    if "REPRODUZINDO" in msg:
        return True
    else:
        print(f"ERRO: {msg}")
        return False


def select_video_and_resolution():
    global video_name
    video_name = input("DIGITE O NOME DO VÍDEO: ")
    res_avaliable = ["240p", "480p", "720p"]
    resolution = input('DIGITE A RESOLUÇÃO: ')

    if resolution not in res_avaliable:
        print('RESOLUÇÃO NÃO DISPONÍVEL')
        return

    msg = pickle.dumps(['REPRODUZIR_VIDEO', video_name, resolution])
    client_socket.sendto(msg, (host_ip, port))


def run_video():
    client_socket.settimeout(1)
    try:
        while True:
            packet, _ = client_socket.recvfrom(BUFF_SIZE)
            # print("Received {0} bytes of data.".format(sys.getsizeof(packet)))
            data = base64.b64decode(packet, ' /')
            npdata = np.fromstring(data, dtype=np.uint8)
            frame = cv2.imdecode(npdata, 1)
            cv2.imshow(video_name, frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                client_socket.close()
                print("VÍDEO FECHADO")
                break
    except socket.timeout:
        print("VIDEO TERMINOU!")


def list_videos():
    msg = pickle.dumps(['LISTAR_VIDEOS'])
    client_socket.sendto(msg, (host_ip, port))
    resposta, _ = client_socket.recvfrom(BUFF_SIZE)
    resposta = pickle.loads(resposta)
    if type(resposta) is dict:
        print("VÍDEOS DISPONÍVEIS: ")
        for video in resposta:
            print(f'{resposta[video][0]} - {resposta[video][1]}')


def main():
    opt = '0'
    while opt != '3':
        opt = input("\nESCOLHA UMA OPÇÃO:\n1) LISTAR VÍDEOS DISPONÍVEIS\n2) REPRODUZIR UM VÍDEO\n3) SAIR\n")
        if opt == '1':
            list_videos()
        elif opt == '2':
            select_video_and_resolution()
            if has_video():
                run_video()
                break


if __name__ == "__main__":
    main()
