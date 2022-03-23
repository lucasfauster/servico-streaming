import logging
import os
import pickle
import socket
import threading

from user_handler import UserHandler


class ServiceManager:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.log = logging.getLogger(" ServiceManager")
        port = 5000

        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
        self.log.info(' method = init, message = HOST IP:{}'.format(host_ip))
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_address = (host_ip, port)
        self.log.info(" method = init, message = Listening at {}".format(self.socket_address))
        self.server_socket.bind(self.socket_address)
        self.server_socket.listen()

        self.user_handler = UserHandler()

        self.streaming_socket = None
        self.streaming_address = None

    def listen_to_user(self):
        user_socket, address = self.server_socket.accept()
        thread = threading.Thread(target=self.user_handler.handle_user, args=(address, user_socket))
        thread.start()
        self.log.info(f" method = listen_to_user, message =  CLIENTS:{threading.activeCount() - 1}")

    def listen_to_streaming_server(self):
        self.streaming_socket, self.streaming_address = self.server_socket.accept()
        thread = threading.Thread(target=self.handle_streaming)
        thread.start()
        self.log.info(f"method=listen, message=connected with streaming service")

    def handle_streaming(self):
        message = ['', '']
        while True:
            self.log.info(
                " method = handle_streaming, message = waiting for message from streaming server")
            try:
                message = pickle.loads(self.streaming_socket.recv(1024))
            except (EOFError, ConnectionResetError, KeyboardInterrupt) as exception:
                self.log.error(
                    f" method = handle_streaming, error = Connection closed unexpectedly with "
                    f"address = {self.streaming_address}, exception={str(exception)}")
                os._exit(1)

            self.log.info(f"method=handle_streaming, message={message[0]}")

            if message[0] == "GET_USER_INFORMATION":
                if message[2] == "GROUP":
                    user = self.user_handler.user_manager.get_user_from_name(message[1])
                    users = self.user_handler.user_manager.get_users_from_group(user.group)
                    users_addresses = [user.address_UDP for user in users]
                    self.log.info(f"method = handle_streaming, message = sending users "
                                  f"addresses {users_addresses} from group {message[1]}")
                    self.streaming_socket.send(pickle.dumps(["ENDERECO_DOS_USUARIOS", users_addresses]))

                else:
                    user = self.user_handler.user_manager.get_user_from_name(message[1])
                    if user:
                        self.log.info(f" method = handle_streaming, message = sending user info: {user.user_type}")
                        self.streaming_socket.send(pickle.dumps(["STATUS_DO_USUARIO", user.user_type]))
                    else: 
                        self.log.error(
                        f" method = handle_streaming, error = User not found address={self.streaming_address}, exception = User not found")
                        self.streaming_socket.send(pickle.dumps(["ERROR"]))
