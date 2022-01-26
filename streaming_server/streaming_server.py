import base64
import os
import pickle
import queue
import socket
import threading
import wave

import cv2
import imutils

from db.video_transactions import *


class StreamingService:
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

        self.active_clients = []

        self.lista_videos = read_videos_transaction_to_client()

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

    @staticmethod
    def find_video(video_name, resolution):
        video_path = f'../videos/{resolution}/{video_name}'
        # noinspection PyArgumentList
        video = cv2.VideoCapture(video_path)
        return video

    def are_clients_active(self, addresses):
        new_addresses = []
        for address in addresses:
            if address in self.active_clients:
                new_addresses.append(address)
        return new_addresses

    def send_video_and_audio(self, client_addr, video, resolution):

        video_queue = queue.Queue(maxsize=10)

        vid = self.find_video(video, resolution)
        FPS = vid.get(cv2.CAP_PROP_FPS)
        TS = (0.5 / FPS)
        totalNoFrames = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
        durationInSeconds = float(totalNoFrames) / float(FPS)
        d = vid.get(cv2.CAP_PROP_POS_MSEC)

        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=3) as executor:
            executor.submit(self.audio_stream, client_addr, video, resolution)
            executor.submit(self.gen_video_stream, vid, video_queue)
            executor.submit(self.send_video, client_addr, video_queue)

    def audio_stream(self, client_addr, video_name, resolution):
        CHUNK = 1024
        try:
            try:
                wf = wave.open(f'../audios/{resolution}-{video_name.split(".")[0]}.wav', 'rb')
            except FileNotFoundError as e:
                command = "ffmpeg -i {} -ab 160k -ac 2 -ar 44100 -vn {}".format(f'../videos/{resolution}/{video_name}',
                                                                                f'../audios/{resolution}-{video_name.split(".")[0]}.wav')
                os.system(command)
                wf = wave.open(f'../audios/{resolution}-{video_name.split(".")[0]}.wav', 'rb')
            while len(client_addr) != 0:
                data = wf.readframes(CHUNK)
                for addr in client_addr:
                    host, port = addr
                    self.server_socket.sendto(data, (host, port + 1))
                client_addr = self.are_clients_active(client_addr)
        except Exception as e:
            print("Error in audio_stream: " + str(e))
            for addr in client_addr:
                host, port = addr
                self.server_socket.sendto(pickle.dumps(["ERRO_PARSING_AUDIO"]), (host, port + 1))
                return

    def gen_video_stream(self, vid, video_queue):
        WIDTH = 400
        while vid.isOpened():
            try:
                _, frame = vid.read()
                frame = imutils.resize(frame, width=WIDTH)
                video_queue.put(frame)
            except Exception as e:
                print(f"Error: {str(e)}")
                return
        print('Player closed')
        vid.release()

    def send_video(self, client_addr, video_queue):
        message = pickle.dumps(["REPRODUZINDO"])
        for addr in client_addr:
            self.server_socket.sendto(message, addr)
        while True:
            frame = video_queue.get()
            encoded, buffer = cv2.imencode('.jpeg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
            message = base64.b64encode(buffer)
            client_addr = self.are_clients_active(client_addr)
            if frame is None or len(client_addr) == 0:
                print(f'ENVIO DO VÍDEO TERMINADO!')
                break
            for addr in client_addr:
                self.server_socket.sendto(message, addr)

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
                    thread = threading.Thread(target=self.send_video_and_audio, args=([address], video, resolution))
                    thread.start()
                else:
                    user_name = msg[4]
                    addresses = self.get_user_group(user_name)
                    video = msg[1]
                    resolution = msg[2]
                    for address in addresses:
                        if address not in self.active_clients:
                            self.active_clients.append(address)
                    thread = threading.Thread(target=self.send_video_and_audio, args=(addresses, video, resolution))
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
            elif type(msg) is list and msg[0] == "CLOSE_STREAMING":
                self.active_clients.remove(address)


if __name__ == "__main__":
    StreamingService().main()
