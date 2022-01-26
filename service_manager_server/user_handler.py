import logging
import pickle
import threading

from user_list_manager import UserListManager


class UserHandler:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.log = logging.getLogger("UserHandler")

        self.user_manager = UserListManager()

        self.operations = {
            "ENTRAR_NA_APP": self.handle_login,
            "SAIR_DA_APP": self.handle_logout,
            "CRIAR_GRUPO": self.handle_create_group,
            "ADD_USUARIO_GRUPO": self.handle_add_to_group,
            "REMOVER_USUARIO_GRUPO": self.handle_remove_from_group,
            "VER_GRUPO": self.handle_get_group
        }

    def is_premium_user(self, address, user_socket):
        user = self.user_manager.get_user_from_address(address)
        if not user.user_type.lower() == 'premium':
            self.log.info(
                "method=is_premium_user, message=this action is exclusive for premium users".format(address))
            user_socket.send(pickle.dumps(["PERMISSAO_NEGADA"]))
            return False
        return True

    # noinspection PyArgumentList
    def handle_user(self, address, user_socket):
        message = ['', '']
        while message[0] != "SAIR_DA_APP":
            self.log.info(
                "method=handle_client, waiting for message in thread={}".format(threading.current_thread().name))
            try:
                message = pickle.loads(user_socket.recv(1024))
            except (EOFError, ConnectionResetError, KeyboardInterrupt) as exception:
                self.log.error("method=handle_client, error=Connection closed "
                               "unexpectedly with address={}, exception={}".format(address, str(exception)))
                self.handle_logout(address=address, close_socket=False)
                return

            self.log.info("method=handle_client, message={}".format(message[0]))
            operation = self.operations.get(message[0], self.handle_default)
            operation(address=address, message=message, user_socket=user_socket)

    def handle_login(self, message, user_socket, address):
        user = self.user_manager.get_user_from_address(address)
        if user is None:
            name, user_type, address_UDP = message[1]
            self.log.info(
                "method=handle_login, message=adding user {} in user list with type {} and address_UDP {}".format(name, user_type, address_UDP))
            self.user_manager.add_user(name=name, address=address, address_UDP=address_UDP, user_socket=user_socket, user_type=user_type)

        else:
            user_info = user.get_user_info()
            self.log.info("method=handle_login, message=sending user info: {}".format(user_info))
            user_socket.send(pickle.dumps(["STATUS_DO_USUARIO", user_info]))

    def handle_logout(self, address, message=None, user_socket=None, close_socket=True):
        self.log.info(f"method=handle_logout, message=removing user with address {address} in user list")
        self.user_manager.remove_user(address, close_socket)

    def handle_create_group(self, address, user_socket, message=None):
        if self.is_premium_user(address, user_socket):
            self.log.info(f"method=handle_create_group, message=creating group for address={address}")
            group = self.user_manager.create_group(address)
            self.log.info(f"method=handle_create_group, message=group {group} created")

    def handle_add_to_group(self, message, user_socket, address):
        if self.is_premium_user(address, user_socket):
            user = self.user_manager.get_user_from_address(address)
            self.log.info(
                f"method=handle_add_to_group, message=adding user {message[1]} to group {user.group}")
            is_added = self.user_manager.add_group_to_user(premium_socket=user_socket, name=message[1],
                                                           group=user.group)
            if not is_added:
                self.log.error(f"method=handle_add_to_group, error=User not found "
                               f"unexpectedly with address={address}, exception=User not found")
                user_socket.send(pickle.dumps(["ADD_USUARIO_GRUPO_ERR"]))

    def handle_remove_from_group(self, message, user_socket, address):
        if self.is_premium_user(address, user_socket):
            self.log.info(f"method=handle_remove_from_group, message=removing user {message[1]} in group list")
            is_removed = self.user_manager.remove_group_to_user(premium_socket=user_socket, name=message[1])
            if not is_removed:
                self.log.error(f"method=handle_remove_from_group, error=User not found "
                               f"unexpectedly with address={address}, exception=User not found")
                user_socket.send(pickle.dumps(["REMOVER_USUARIO_GRUPO_ERR"]))

    def handle_get_group(self, user_socket, address, message=None):
        if self.is_premium_user(address, user_socket):
            user = self.user_manager.get_user_from_address(address)
            self.log.info(f"method=handle_get_group, message=getting group for user {user.get_user_info()}")
            users = self.user_manager.get_users_from_group(group=user.group)
            users_names = [user.name for user in users]
            self.log.info(f"method=handle_get_group, message=sending user list {users_names} to user")
            user_socket.send(pickle.dumps(["GRUPO_DE_STREAMING", users_names]))

    def handle_default(self, message, user_socket, address=None):
        user_socket.send(pickle.dumps(["OPÇÃO INVÁLIDA"]))
        self.log.error(f"method=handle_default, error=Opção {message[0]} inválida")
