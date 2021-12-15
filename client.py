import cv2
import pickle
import socket
import struct

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host_ip = '127.0.1.1'
port = 5050
address = (host_ip, port)


def main():
    resAvaliable = ["240p", "480p", "720p"]
    print('Avaliable resolutions: 240p/ 480p/ 720p')
    resolution = input('Select one resolution: ')

    if resolution not in resAvaliable:
        print('Resolution not found')
        return

    msg = pickle.dumps(['REPRODUZIR_VIDEO'])
    client_socket.sendto(msg, ('127.0.1.1', 5050))

    resposta, address = client_socket.recvfrom(1024)
    if pickle.loads(resposta)[0] == 'ENVIAR RESOLUCAO':
        print('chegou')
        data = pickle.dumps(["VIDEO/RESOLUCAO", "video.mkv", resolution])
        client_socket.sendto(data, address)

    resposta, address = client_socket.recvfrom(1024)
    if pickle.loads(resposta)[0] == 404:
        print('Video não encontrado para a resolução escolhida')
    elif pickle.loads(resposta)[0] == 204:
        print('Iniciando reprodução do vídeo')
        show_video()


def show_video():
    data = b""
    print('chega no show_video')
    while True:
        frame_data, data = get_frame_data(data)
        if frame_data is None:
            print("VIDEO FINISHED!")
            client_socket.close()
            break

        frame = pickle.loads(frame_data)
        cv2.imshow(f"FROM {host_ip}", frame)
        if cv2.waitKey(1) == ord('q'):
            break


def get_frame_data(data):
    payload_size = struct.calcsize("Q")
    while len(data) < payload_size:
        packet, origin = client_socket.recvfrom(4 * 1024)
        if not packet:
            return None, data
        data += packet
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q", packed_msg_size)[0]
    while len(data) < msg_size:
        packet, origin = client_socket.recvfrom(4 * 1024)
        data += packet
    frame_data = data[:msg_size]
    data = data[msg_size:]
    return frame_data, data

''''

def has_video():
    found_video_code, found_video_error_message = pickle.loads(client_socket.recv(1024))
    if found_video_code == 404:
        print(found_video_error_message)
        return False
    return True
'''''

if __name__ == "__main__":
    main()
