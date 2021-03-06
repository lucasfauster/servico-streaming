import pickle
import uuid

from user import User


class UserListManager:

    def __init__(self):
        self.user_list = []

    def add_user(self, name, address, address_UDP, user_socket, user_type):
        new_user = User(name=name, socket=user_socket, address=address, address_UDP=address_UDP, user_type=user_type)
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

    def get_user_from_name(self, name):
        for user in self.user_list:
            if user.name == name:
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
                return True
        return False

    def remove_group_to_user(self, premium_socket, name):
        for user in self.user_list:
            if user.name == name:
                user.group = None
                premium_socket.send(pickle.dumps(["REMOVER_USUARIO_GRUPO_ACK"]))
                return True
        return False

    def get_users_from_group(self, group):
        group_list = []
        for user in self.user_list:
            if group is not None and user.group == group:
                group_list.append(user)
        return group_list
