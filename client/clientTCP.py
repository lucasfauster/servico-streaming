import pickle
import socket
from time import sleep


class ClientTCP:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host_ip = '127.0.1.1'
        self.port = 6060

        self.client_socket.connect((self.host_ip, self.port))

    def send_message(self, message):
        self.client_socket.send(pickle.dumps(message))
        return  pickle.loads(self.client_socket.recv(1024))

    def log_in(self, name, type):
        resp = self.send_message(["ENTRAR_NA_APP", [name, type]])
        if resp[0] == "ENTRAR_NA_APP_ACK":
            print("Você entrou no app")
            return True

        print("Ocorreu um erro ao entrar no app")
        return False

    def log_out(self):
        self.send_message(["SAIR_DA_APP"])

    def get_user_info(self, name, type):
        resp = self.send_message(["ENTRAR_NA_APP", [name, type]])
        if resp[0] == "STATUS_DO_USUARIO":
            return resp[1]
        return None

    def create_group(self, type):
        if not type.lower() == 'premium':
            print("Exclusivo para premiuns")
            return
            
        resp = self.send_message(["CRIAR_GRUPO"])
        if resp[0] == "CRIAR_GRUPO_ACK":
            print("Grupo criado com sucesso!")
        else: 
            print("Erro ao criar grupo")

    def add_to_group(self, type):
        if not type.lower() == 'premium':
            print("Exclusivo para premiuns")
            return

        chosen_user = input("Digite o nome do usuário: ")
        resp = self.send_message(["ADD_USUARIO_GRUPO", chosen_user])
        if resp[0] == "ADD_USUARIO_GRUPO_ACK":
            print("Usuário adicionado ao grupo com sucesso!")
        else: 
            print("Erro ao adicionar usuário ao grupo")

    def get_group(self, type):
        if not type.lower() == 'premium':
            print("Exclusivo para premiuns")
            return

        resp = self.send_message(["VER_GRUPO"])
        if resp[0] == "GRUPO_DE_STREAMING":
            print("Usuários do grupo: {}".format(resp[1]))
        else: 
            print("Erro ao buscar grupo")

    def remove_from_group(self, type):
        if not type.lower() == 'premium':
            print("Exclusivo para premiuns")
            return

        chosen_user = input("Digite o nome do usuário: ")
        resp = self.send_message(["REMOVER_USUARIO_GRUPO", chosen_user])
        if resp[0] == "REMOVER_USUARIO_GRUPO_ACK":
            print("Usuário removido do grupo com sucesso!")
        else: 
            print("Erro ao remover usuário do grupo")
        
