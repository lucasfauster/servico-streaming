from clientUDP import ClientUDP
from clientTCP import ClientTCP


def main():
    opt = ''
    client_udp = ClientUDP()
    client_tcp = ClientTCP()

    user_name = input("Digite seu nome: ")
    user_type = input("Digite o tipo de usuário ( Premium/Convidado ): ")
    if not client_tcp.log_in(user_name, user_type):
        return

    while opt != '0':
        opt = input("""\nESCOLHA UMA OPÇÃO:
                    1) LISTAR VÍDEOS DISPONÍVEIS
                    2) REPRODUZIR UM VÍDEO
                    3) CRIAR GRUPO
                    4) ADICIONAR USUÁRIO AO GRUPO
                    5) VER SEU GRUPO
                    6) REMOVER USUÁRIO DO GRUPO
                    7) REPRODUZIR VIDEO EM GRUPO
                    8) ENTRAR NA SALA DO GRUPO
                    0) SAIR\n""")
        if opt == '1':
            client_udp.list_videos()
        elif opt == '2':
            client_udp.play_video(user_name = user_name)
        elif opt == '3':
            client_tcp.create_group()
        elif opt == '4':
            client_tcp.add_to_group()
        elif opt == '5':
            client_tcp.get_group()
        elif opt == '6':
            client_tcp.remove_from_group()
        elif opt == '7':
            client_udp.play_video(user_name = user_name, option = "GROUP")
        elif opt == '8':
            client_udp.get_in_room()
        elif opt == '0':
            client_tcp.log_out()
        else:
            print("OPÇÃO INVÁLIDA")


if __name__ == "__main__":
    main()
