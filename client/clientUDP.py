import pickle
import cv2
import socket
import numpy as np
import base64


class ClientUDP:
    def __init__(self):
        self.BUFF_SIZE = 65536
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.BUFF_SIZE)
        self.host_ip = '127.0.1.1'
        self.port = 5050
        self.video_name = ""
        self.server_address = (self.host_ip, self.port)
        self.address = self.get_address()

    def send_recv_message(self, message):
        self.client_socket.sendto(pickle.dumps(message), self.server_address)
        resp, _ = self.client_socket.recvfrom(self.BUFF_SIZE)
        return pickle.loads(resp)

    def has_video(self, option):
        if option == "SINGLE":
            self.client_socket.settimeout(10)
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
    
    def select_video_and_resolution(self, option, user_name):
        self.video_name = input("DIGITE O NOME DO VÍDEO: ")
        res_avaliable = ["240p", "480p", "720p"]
        resolution = input('DIGITE A RESOLUÇÃO: ')

        if resolution not in res_avaliable:
            print('RESOLUÇÃO NÃO DISPONÍVEL')
            return False
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
                    self.client_socket.close()
                    print("VÍDEO FECHADO")
                    break
        except socket.timeout:
            print("VIDEO TERMINOU!")

    def list_videos(self):
        resposta = self.send_recv_message(['LISTAR_VIDEOS'])
        if type(resposta) is dict:
            print("VÍDEOS DISPONÍVEIS: ")
            for video in resposta:
                print(f'{resposta[video][0]} - {resposta[video][1]}')

    def play_video(self, user_name, option="SINGLE"):
        has_permission = self.check_permission(user_name)
        if has_permission:
            video_selected = self.select_video_and_resolution(option, user_name)
            if video_selected and self.has_video("SINGLE"):
                self.run_video()
        
    def get_in_room(self):
        if self.has_video("GROUP"):
            self.run_video()

    def get_address(self):
        return self.send_recv_message(['GET_ADDRESS'])[0]