class User:
    def __init__(self, name, socket, address, user_type, group=None):
        self.name = name
        self.socket = socket
        self.address = address
        self.user_type = user_type
        self.group = group

    def get_user_info(self):
        return {"Nome": self.name, "IP": self.address, "Tipo": self.user_type, "Grupo": self.group}