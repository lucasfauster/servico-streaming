import logging
import pickle
import socket
import threading

from service_manager_server.user_manager import UserManager


class ServiceManager:

    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.log = logging.getLogger("ServiceManager")
        port = 5051

        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
        self.log.info('method=init, action=HOST IP:{}'.format(host_ip))
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_address = (host_ip, port)
        self.log.info("method=init, action=Listening at {}".format(self.socket_address))
        self.server_socket.bind(self.socket_address)
        self.server_socket.listen()

        self.user_manager = UserManager()

        self.operations = {
            "ENTRAR_NA_APP": self.handle_login,
            "SAIR_DA_APP": self.handle_logout,
            "CRIAR_GRUPO": self.handle_create_group,
            "ADD_USUARIO_GRUPO": self.handle_add_to_group,
            "REMOVER_USUARIO_GRUPO": self.handle_remove_from_group,
            "VER_GRUPO": self.handle_get_group
        }

    def listen(self):
        user_socket, address = self.server_socket.accept()
        thread = threading.Thread(target=self.handle_client, args=(address, user_socket))
        thread.start()
        self.log.info("method=listen, action=TOTAL CLIENTS:{}".format(threading.activeCount() - 1))

    # noinspection PyArgumentList
    def handle_client(self, address, user_socket):
        message = ['', []]
        while message[0] != "SAIR_DA_APP":
            self.log.info("method=handle_client, waiting for message in thread={}".format(threading.current_thread().name))
            try:
                message = pickle.loads(user_socket.recv(1024))
            except (EOFError, ConnectionResetError, KeyboardInterrupt) as exception:
                self.log.error("method=handle_client, error=Connection closed "
                               "unexpectedly with address={}, exception={}".format(address, str(exception)))
                self.handle_logout(address=address, close_socket=False)
                return

            self.log.info("method=handle_client, action={}".format(message[0]))
            operation = self.operations.get(message[0], self.handle_default)
            operation(address=address, message=message, user_socket=user_socket)

    def handle_login(self, message, user_socket, address):
        user = self.user_manager.get_user_from_address(address)
        if user is None:
            name, user_type = message[1]
            self.log.info("method=handle_login, action=adding user {} in user list with type {}".format(name, user_type))
            self.user_manager.add_user(name=name, address=address, user_socket=user_socket, user_type=user_type)

        else:
            user_info = user.get_user_info()
            self.log.info("method=handle_login, action=sending user info: {}".format(user_info))
            user_socket.send(pickle.dumps(["STATUS_DO_USUARIO", user_info]))

    def handle_logout(self, address, message=None, user_socket=None, close_socket=True):
        self.log.info("method=handle_logout, action=removing user with address {} in user list".format(address))
        self.user_manager.remove_user(address, close_socket)

    def handle_create_group(self, address, message=None, user_socket=None):
        self.log.info("method=handle_create_group, action=creating group for address={}".format(address))
        group = self.user_manager.create_group(address)
        self.log.info("method=handle_create_group, action=group {} created".format(group))

    def handle_add_to_group(self, message, user_socket, address):
        user = self.user_manager.get_user_from_address(address)
        self.log.info("method=handle_add_to_group, action=adding user {} to group {}".format(message[1], user.group))
        self.user_manager.add_group_to_user(premium_socket=user_socket, name=message[1], group=user.group)

    def handle_remove_from_group(self, message, user_socket, address=None):
        self.log.info("method=handle_remove_from_group, action=removing user {} in group list".format(message[1]))
        self.user_manager.remove_group_to_user(premium_socket=user_socket, name=message[1])

    def handle_get_group(self, user_socket, address, message=None):
        user = self.user_manager.get_user_from_address(address)
        self.log.info("method=handle_get_group, action=getting group for user {}".format(user.get_user_info()))
        users = self.user_manager.get_users_from_group(group=user.group)
        self.log.info("method=handle_get_group, action=sending user list {} to user".format(users))
        user_socket.send(pickle.dumps(["GRUPO_DE_STREAMING", users]))

    def handle_default(self, message, user_socket, address=None):
        user_socket.send(pickle.dumps(["OPÇÃO INVÁLIDA"]))
        self.log.error("method=handle_default, error=Opção {} inválida".format(message[0]))


def main():
    service_manager = ServiceManager()
    while True:
        service_manager.listen()


if __name__ == "__main__":
    main()
