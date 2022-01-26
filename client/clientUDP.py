import pickle
import struct

import cv2
import socket
import numpy as np
import base64

import pyaudio


class ClientUDP:
    def __init__(self):
        self.BUFF_SIZE = 65536
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.BUFF_SIZE)
        self.client_socket.bind(('127.0.1.1', 0))

        self.port = self.client_socket.getsockname()[1]

        self.audio_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.audio_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.BUFF_SIZE)
        self.audio_socket.bind(('127.0.1.1', self.port+1))

        self.host_ip = '127.0.1.1'
        self.port = 5050
        self.video_name = ""
        self.server_address = (self.host_ip, self.port)

        self.break_video = False

    def send_recv_message(self, message):
        self.client_socket.sendto(pickle.dumps(message), self.server_address)
        while True:
            try:
                resp, _ = self.client_socket.recvfrom(self.BUFF_SIZE)
                return pickle.loads(resp)
            except pickle.UnpicklingError:
                pass

    def has_video(self, option):
        if option == "SINGLE":
            self.client_socket.settimeout(10)
        else:
            self.client_socket.settimeout(None)
        try:
            msg, _ = self.client_socket.recvfrom(self.BUFF_SIZE)
            message = pickle.loads(msg)
            if message[0] == "REPRODUZINDO":
                return True
            else:
                print(f"ERRO: {message}")
                return False
        except socket.timeout:
            print("NÃO HÁ VIDEO A SER EXIBIDO")
            return False

    def select_video_and_resolution(self, video_name, resolution, user_name, option):

        self.video_name = video_name

        if option == "SINGLE":
            message = ['REPRODUZIR_VIDEO', self.video_name, resolution, "SINGLE"]
            self.client_socket.sendto(pickle.dumps(message), self.server_address)
        else:
            message = ['REPRODUZIR_VIDEO', self.video_name, resolution, "GROUP", user_name]
            self.client_socket.sendto(pickle.dumps(message), self.server_address)

        return True

    def check_permission(self, user_name):
        resp = self.send_recv_message(["GET_USER_INFORMATION", user_name, "SINGLE"])
        if resp[0] == "AUTORIZADO":
            return True
        else:
            print(resp[0])
            return False

    def run_video(self):
        self.client_socket.settimeout(1)
        self.break_video = False
        try:
            while True:
                packet, _ = self.client_socket.recvfrom(self.BUFF_SIZE)
                # print("Received {0} bytes of data.".format(sys.getsizeof(packet)))
                data = base64.b64decode(packet)
                npdata = np.fromstring(data, dtype=np.uint8)
                frame = cv2.imdecode(npdata, 1)
                cv2.imshow(self.video_name, frame)
                key = cv2.waitKey(1) & 0xFF  # não tá pegando o comando de parar a reprodução do vídeo
                if key == ord('q'):
                    print("VÍDEO FECHADO")
                    self.break_video = True
                    break

        except socket.timeout:
            print("VIDEO TERMINOU!")
        finally:
            cv2.destroyAllWindows()
            message = ['CLOSE_STREAMING']
            self.client_socket.sendto(pickle.dumps(message), self.server_address)

    def list_videos(self):
        resposta = self.send_recv_message(['LISTAR_VIDEOS'])
        return resposta

    def play_video(self, user_name, video_name, resolution, option="SINGLE"):
        has_permission = self.check_permission(user_name)
        if has_permission:
            video_selected = self.select_video_and_resolution(video_name, resolution, user_name, option)
            if video_selected and self.has_video("SINGLE"):
                from concurrent.futures import ThreadPoolExecutor
                with ThreadPoolExecutor(max_workers=2) as executor:
                    executor.submit(self.audio_stream)
                    executor.submit(self.run_video)

    def get_in_group_room(self):
        if self.has_video("GROUP"):
            from concurrent.futures import ThreadPoolExecutor
            with ThreadPoolExecutor(max_workers=2) as executor:
                executor.submit(self.audio_stream)
                executor.submit(self.run_video)

    def audio_stream(self):
        p = pyaudio.PyAudio()
        _CHUNK = 1024
        stream = p.open(format=p.get_format_from_width(2),
                        channels=2,
                        rate=44100,
                        output=True,
                        frames_per_buffer=_CHUNK)
        self.audio_socket.settimeout(1)
        while not self.break_video:
            try:
                frame, _ = self.audio_socket.recvfrom(self.BUFF_SIZE)
                stream.write(frame)
            except Exception as e:
                print(f"ERRO: {str(e)}")
                break
        self.break_video = False
