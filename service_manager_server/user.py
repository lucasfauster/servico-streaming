class User:
    def __init__(self, name, socket, address, address_UDP, user_type, group=None):
        self.name = name
        self.socket = socket
        self.address = address
        self.address_UDP = address_UDP
        self.user_type = user_type
        self.group = group

    def get_user_info(self):
        return {"Nome": self.name, "IP": self.address, "UDP": self.address_UDP, "Tipo": self.user_type, "Grupo": self.group}
