import pickle
import socket
import logging


class ClientTCP:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.log = logging.getLogger(" clientTCP")
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host_ip = '127.0.1.1'
        self.port = 5000

        self.client_socket.connect((self.host_ip, self.port))
        self.address_UDP = ()

    def has_permission(self, message):
        if message == "PERMISSAO_NEGADA":
            self.log.error(" method = has_permission, error = Only premium users can do this action!")
            return False
        return True

    def send_recv_message(self, message):
        self.client_socket.send(pickle.dumps(message))
        return pickle.loads(self.client_socket.recv(1024))

    def log_in(self, name, user_type):
        message = ["ENTRAR_NA_APP", [name, user_type, self.address_UDP]]
        resp = self.send_recv_message(message)
        if resp[0] == "ENTRAR_NA_APP_ACK":
            self.log.info(" method = log_in, message = User entered the app!")
            return True
        self.log.error(" method = log_in, error = An error occurred while entering the app!")
        return False

    def log_out(self):
        self.log.info("method = log_out, message = User left the app! TCHAU!")
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
                self.log.info(" method = create_group, message = Group created successfully!")
            else:
                self.log.error(" method = create_group, error = An error occurred while creating group!")

    def add_to_group(self, chosen_user):
        resp = self.send_recv_message(["ADD_USUARIO_GRUPO", chosen_user])
        if self.has_permission(resp[0]):
            if resp[0] == "ADD_USUARIO_GRUPO_ACK":
                self.log.info(" method = add_to_group, message = User added to group successfully!")
                return True
            else:
                self.log.error(" method = add_to_group, error = An error occurred while adding user to group!")
                return False

    def get_group(self):
        resp = self.send_recv_message(["VER_GRUPO"])
        if resp[0] == "GRUPO_DE_STREAMING":
            self.log.info(" method = get_group, message = Group users: {}".format(resp[1]))
            return resp[1]
        else:
            self.log.error(" method = get_group, error = An error occurred while fetching group: {}".format(resp[1]))
            return None

    def remove_from_group(self, chosen_user):
        resp = self.send_recv_message(["REMOVER_USUARIO_GRUPO", chosen_user])
        if self.has_permission(resp[0]):
            if resp[0] == "REMOVER_USUARIO_GRUPO_ACK":
                self.log.info(" method = remove_from_group, message = User removed from group successfully!")
                return True
            else:
                self.log.error(" method = add_to_group, error = An error occurred while removing user from group!")
                return False
