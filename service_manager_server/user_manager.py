import pickle
import uuid

from service_manager_server.user import User


class UserManager:

    def __init__(self):
        self.user_list = []

    def add_user(self, name, address, user_socket, user_type):
        new_user = User(name=name, socket=user_socket, address=address, user_type=user_type)
        self.user_list.append(new_user)
        user_socket.send(pickle.dumps(["ENTRAR_NA_APP_ACK"]))

    def remove_user(self, address, close_socket):
        for user in self.user_list:
            if user.address == address:
                if close_socket:
                    user.socket.send(pickle.dumps(["SAIR_DA_APP_ACK"]))
                    user.socket.close()
                self.user_list.remove(user)

    def get_user_from_address(self, address):
        for user in self.user_list:
            if user.address == address:
                return user
        return None

    def create_group(self, address):
        user = self.get_user_from_address(address)
        user.group = uuid.uuid4()
        user.socket.send(pickle.dumps(["CRIAR_GRUPO_ACK"]))
        return user.group

    def add_group_to_user(self, premium_socket, name, group):
        for user in self.user_list:
            if user.name == name:
                user.group = group
                premium_socket.send(pickle.dumps(["ADD_USUARIO_GRUPO_ACK"]))

    def remove_group_to_user(self, premium_socket, name):
        for user in self.user_list:
            if user.name == name:
                user.group = None
                premium_socket.send(pickle.dumps(["REMOVER_USUARIO_GRUPO_ACK"]))

    def get_users_from_group(self, group):
        group_list = []
        for user in self.user_list:
            if user.group == group:
                group_list.append(user.name)
        return group_list
