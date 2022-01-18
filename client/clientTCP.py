import pickle
import socket
from time import sleep

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '127.0.1.1'
port = 5051


def main():
    client_socket.connect((host_ip, port))

    send_message(["ENTRAR_NA_APP", ["Igor2", "premium"]])
    send_message(["ENTRAR_NA_APP", ["Igor2", "premium"]])
    send_message(["CRIAR_GRUPO"])
    send_message(["VER_GRUPO"])
    send_message(["ADD_USUARIO_GRUPO", "Igor"])
    send_message(["VER_GRUPO"])
    send_message(["REMOVER_USUARIO_GRUPO", "Igor"])
    send_message(["TESTE"])
    send_message(["SAIR_DA_APP"])

    while True:
        print("oi")
        sleep(1000) # pra n morrer a conexão


def send_message(message):
    client_socket.send(pickle.dumps(message))
    teste = pickle.loads(client_socket.recv(1024))
    print(teste)


if __name__ == "__main__":
    main()
