from db.video_transactions import *
import pickle
import threading
import cv2
import imutils
import socket
import base64
import logging


class ServerUDP:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.log = logging.getLogger(" ServerUDP")
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

        self.active_clients = []

        self.lista_videos = read_videos_transaction_to_client()
        self.log.info(' method = init, message = UDP server ready!')

    def get_user_type(self, user_name):
        self.service_socket.send(pickle.dumps(["GET_USER_INFORMATION", user_name, "SINGLE"]))
        resp = pickle.loads(self.service_socket.recv(1024))
        if resp[0] == "STATUS_DO_USUARIO":
            return resp[1]
        self.log.error(' method = get_user_type, error = An error occurred while getting user type')

    def get_user_group(self, user_name):
        self.service_socket.send(pickle.dumps(["GET_USER_INFORMATION", user_name, "GROUP"]))
        resp = pickle.loads(self.service_socket.recv(1024))
        if resp[0] == "ENDERECO_DOS_USUARIOS":
            return resp[1]
        self.log.error(' method = get_user_group, error = An error occurred while getting user group')

    @staticmethod
    def find_video(video_name, resolution):
        # noinspection PyArgumentList
        video = cv2.VideoCapture(f'../videos/{resolution}/{video_name}')
        return video

    def is_client_active(self, addresses):
        new_addresses = []
        for address in addresses:
            if address in self.active_clients:
                new_addresses.append(address)
        return new_addresses

    def send_video(self, client_addr, video, resolution):
        vid = self.find_video(video, resolution)
        if vid.isOpened():
            self.log.info(f' method = send_video, message = Sending video "{video}" with resolution {resolution} to {client_addr}')
            message = pickle.dumps(["REPRODUZINDO"])
            for addr in client_addr:
                self.server_socket.sendto(message, addr)
            while vid.isOpened():
                client_addr = self.is_client_active(client_addr)
                img, frame = vid.read()
                if not img or len(client_addr) == 0:
                    self.log.info(f' method = send_video, message = Video "{video}" with resolution {resolution} '
                                  f'finished being sent to {client_addr}')
                    break
                frame = imutils.resize(frame, width=600)
                encoded, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 60])
                message = base64.b64encode(buffer)
                for addr in client_addr:
                    self.server_socket.sendto(message, addr)
            vid.release()
        else:
            msg = f"VIDEO {video} NÃO ENCONTRADO PARA RESOLUÇÃO {resolution}."
            self.log.error(f' method = send_video, error = Video "{video} not found for resolution {resolution}.')
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
                    if address not in self.active_clients:
                        self.active_clients.append(address)
                    thread = threading.Thread(target=self.send_video, args=([address], video, resolution))
                    thread.start()
                else:
                    user_name = msg[4]
                    addresses = self.get_user_group(user_name)
                    video = msg[1]
                    resolution = msg[2]
                    for address in addresses:
                        if address not in self.active_clients:
                            self.active_clients.append(address)
                    thread = threading.Thread(target=self.send_video, args=(addresses, video, resolution))
                    thread.start()

            elif type(msg) is list and msg[0] == 'LISTAR_VIDEOS':
                msg = pickle.dumps(self.lista_videos)
                self.server_socket.sendto(msg, address)
                self.log.info(f' method = main, message = List of Videos sent to {address}')

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
            elif type(msg) is list and msg[0] == "CLOSE_STREAMING":
                self.active_clients.remove(address)


if __name__ == "__main__":
    ServerUDP().main()
