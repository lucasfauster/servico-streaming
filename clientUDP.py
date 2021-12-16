import pickle

import cv2, imutils, socket
import numpy as np
import time
import base64

BUFF_SIZE = 65536
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
host_name = socket.gethostname()
host_ip = '127.0.1.1'
print(host_ip)
port = 5050

def main ():
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
        fps, st, frames_to_count, cnt = (0, 0, 20, 0)
        while True:
            packet, _ = client_socket.recvfrom(BUFF_SIZE)
            data = base64.b64decode(packet, ' /')
            npdata = np.fromstring(data, dtype=np.uint8)
            frame = cv2.imdecode(npdata, 1)
            frame = cv2.putText(frame, 'FPS: ' + str(fps), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.imshow("RECEIVING VIDEO", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                client_socket.close()
                break
            if cnt == frames_to_count:
                try:
                    fps = round(frames_to_count / (time.time() - st))
                    st = time.time()
                    cnt = 0
                except:
                    pass
            cnt += 1

if __name__ == "__main__":
    main()