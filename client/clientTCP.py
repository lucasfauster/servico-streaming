import pickle
import socket


class ClientTCP:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host_ip = '127.0.1.1'
        self.port = 5000

        self.client_socket.connect((self.host_ip, self.port))
        self.address_UDP = ()

    @staticmethod
    def has_permission(message):
        if message == "PERMISSAO_NEGADA":
            print("Apenas usuários Premium podem fazer essa ação!")
            return False
        return True

    def send_recv_message(self, message):
        self.client_socket.send(pickle.dumps(message))
        return pickle.loads(self.client_socket.recv(1024))

    def log_in(self, name, user_type):
        message = ["ENTRAR_NA_APP", [name, user_type, self.address_UDP]]
        resp = self.send_recv_message(message)
        if resp[0] == "ENTRAR_NA_APP_ACK":
            print("Você entrou no app")
            return True
        print("Ocorreu um erro ao entrar no app")
        return False

    def log_out(self):
        print("TCHAU!")
        self.send_recv_message(["SAIR_DA_APP"])

    def get_user_info(self):
        resp = self.send_recv_message(["ENTRAR_NA_APP"])
        if resp[0] == "STATUS_DO_USUARIO":
            return resp[1]
        return None

    def create_group(self):
        resp = self.send_recv_message(["CRIAR_GRUPO"])
        if self.has_permission(resp[0]):
            if resp[0] == "CRIAR_GRUPO_ACK":
                print("Grupo criado com sucesso!")
            else:
                print("Erro ao criar grupo")

    def add_to_group(self, chosen_user):
        resp = self.send_recv_message(["ADD_USUARIO_GRUPO", chosen_user])
        if self.has_permission(resp[0]):
            if resp[0] == "ADD_USUARIO_GRUPO_ACK":
                print("Usuário adicionado ao grupo com sucesso!")
                return True
            else:
                print("Erro ao adicionar usuário ao grupo")
                return False

    def get_group(self):
        resp = self.send_recv_message(["VER_GRUPO"])
        if resp[0] == "GRUPO_DE_STREAMING":
            print("Usuários do grupo: {}".format(resp[1]))
            return resp[1]
        else:
            print("Erro ao buscar grupo {}".format(resp[1]))
            return None

    def remove_from_group(self, chosen_user):
        resp = self.send_recv_message(["REMOVER_USUARIO_GRUPO", chosen_user])
        if self.has_permission(resp[0]):
            if resp[0] == "REMOVER_USUARIO_GRUPO_ACK":
                print("Usuário removido do grupo com sucesso!")
                return True
            else:
                print("Erro ao remover usuário do grupo")
                return False
