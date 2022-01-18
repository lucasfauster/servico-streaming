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

    user_info =  client_tcp.get_user_info(user_name, user_type)
    if not user_info:
        print("Usuário não foi cadastrado corretamente")
        return

    while opt != '0':
        opt = input("""\nESCOLHA UMA OPÇÃO:
                    1) LISTAR VÍDEOS DISPONÍVEIS
                    2) REPRODUZIR UM VÍDEO
                    3) CRIAR GRUPO
                    4) ADICIONAR USUÁRIO AO GRUPO
                    5) VER SEU GRUPO
                    6) REMOVER USUÁRIO DO GRUPO
                    0) SAIR\n""")
        if opt == '1':
            client_udp.list_videos()
        elif opt == '2':
            client_udp.select_video_and_resolution()
            if client_udp.has_video():
                client_udp.run_video()
                break
        elif opt == '3':
            client_tcp.create_group(user_info["Tipo"])
        elif opt == '4':
            client_tcp.add_to_group(user_info["Tipo"])
        elif opt == '5':
            client_tcp.get_group(user_info["Tipo"])
        elif opt == '6':
            client_tcp.remove_from_group(user_info["Tipo"])
    client_tcp.log_out()


if __name__ == "__main__":
    main()
