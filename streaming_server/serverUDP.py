import pickle
import threading
import cv2
import imutils
import socket
import base64

class serverUDP:
    def __init__(self):
        self.BUFF_SIZE = 65536
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.BUFF_SIZE)
        self.host_name = socket.gethostname()
        self.host_ip = '127.0.1.1'
        self.port = 5050
        self.socket_address = (self.host_ip, self.port)
        self.server_socket.bind(self.socket_address)

        self.service_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.service_port = 5000
        self.service_host_ip = '127.0.1.1'
        self.service_socket.connect((self.host_ip, self.service_port))

        self.lista_videos = {'1': ['animacao.mp4', '240p'], '2': ['animacao.mp4', '480p'], '3': ['animacao.mp4', '720p'],
                    '4': ['pacman.mp4', '240p'], '5': ['pacman.mp4', '480p'], '6': ['pacman.mp4', '720p']}


    def get_user_type(self, user_name):
        self.service_socket.send(pickle.dumps(["GET_USER_INFORMATION", user_name, "SINGLE"]))
        resp = pickle.loads(self.service_socket.recv(1024))
        if resp[0] == "STATUS_DO_USUARIO":
            return resp[1]
        print("ERRO AO BUSCAR INFORMAÇÕESDO USUÁRIO")

    def get_user_group(self, user_name):
        self.service_socket.send(pickle.dumps(["GET_USER_INFORMATION", user_name, "GROUP"]))
        resp = pickle.loads(self.service_socket.recv(1024))
        if resp[0] == "ENDERECO_DOS_USUARIOS":
            return resp[1]
        print("ERRO AO BUSCAR INFORMAÇÕES DO GRUPO  DO USUÁRIO")

    def find_video(self, video_name, resolution):
        # noinspection PyArgumentList
        video = cv2.VideoCapture(f'../videos/{resolution}/{video_name}')
        return video


    def send_video(self, client_addr, video, resolution):
        vid = self.find_video(video, resolution)
        if vid.isOpened():
            print(f"ENVIANDO VÍDEO {video} COM RESOLUÇÃO {resolution} PARA {client_addr}")
            message = pickle.dumps(["REPRODUZINDO"])
            for addr in client_addr:
                self.server_socket.sendto(message, addr)
            while vid.isOpened():
                img, frame = vid.read()
                if not img:
                    print(f'ENVIO DO VÍDEO {video} COM RESOLUÇÃO {resolution} PARA {client_addr} TERMINADO!')
                    break
                frame = imutils.resize(frame, width=600)
                encoded, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 50])
                message = base64.b64encode(buffer)
                for addr in client_addr:
                    self.server_socket.sendto(message, addr)
            vid.release()
        else:
            msg = f"VIDEO {video} NÃO ENCONTRADO PARA RESOLUÇÃO {resolution}."
            print(msg)
            for addr in client_addr:
                self.server_socket.sendto(pickle.dumps(msg), addr)


    def main(self):
        while True:
            msg, address = self.server_socket.recvfrom(self.BUFF_SIZE)
            msg = pickle.loads(msg)
            if type(msg) is list and msg[0] == 'REPRODUZIR_VIDEO':
                if msg[3] == "SINGLE":
                    video = msg[1]
                    resolution = msg[2]
                    thread = threading.Thread(target=self.send_video, args=([address], video, resolution))
                    thread.start()
                else:
                    user_name = msg[4]
                    addresses = self.get_user_group(user_name)
                    video = msg[1]
                    resolution = msg[2]
                    thread = threading.Thread(target=self.send_video, args=(addresses, video, resolution))
                    thread.start()

            elif type(msg) is list and msg[0] == 'LISTAR_VIDEOS':
                msg = pickle.dumps(self.lista_videos)
                self.server_socket.sendto(msg, address)
                print("LISTA DE VIDEOS ENVIADA PARA", address)

            elif type(msg) is list and msg[0] == "GET_USER_INFORMATION":
                user_name = msg[1]
                resp = self.get_user_type(user_name)
                if resp == "premium":
                    msg = pickle.dumps(["AUTORIZADO"])
                else:
                    msg = pickle.dumps(["NÃO TEM PERMISSÃO PARA REPRODUZIR VÍDEOS, POR FAVOR MUDE SUA CLASSIFICAÇÃO"])
                self.server_socket.sendto(msg, address)
            elif type(msg) is list and msg[0] == 'GET_ADDRESS':
                msg = pickle.dumps([address])
                self.server_socket.sendto(msg, address)


if __name__ == "__main__":
    serverUDP().main()
