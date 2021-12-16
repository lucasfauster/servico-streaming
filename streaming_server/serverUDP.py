import pickle
import cv2
import imutils
import socket
import time
import base64

clients = {}

BUFF_SIZE = 65536
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
host_name = socket.gethostname()
host_ip = '127.0.1.1'
port = 5050
socket_address = (host_ip, port)
server_socket.bind(socket_address)
print('Listening at:', socket_address)

vid = None


def find_video(video_name):
	global vid
	vid = cv2.VideoCapture(f'../videos/{video_name}')


while True:
	msg, client_addr = server_socket.recvfrom(BUFF_SIZE)
	msg = pickle.loads(msg)
	video, resolution = msg
	find_video(video)
	print('GOT connection from ', client_addr)
	if vid:
		while vid.isOpened():
			fps, st, frames_to_count, cnt = (0, 0, 20, 0)
			_, frame = vid.read()
			frame = imutils.resize(frame,width=int(resolution))
			encoded, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY,80])
			message = base64.b64encode(buffer)
			server_socket.sendto(message, client_addr)
			frame = cv2.putText(frame, 'FPS: '+str(fps), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
			cv2.imshow('TRANSMITTING VIDEO', frame)
			key = cv2.waitKey(1) & 0xFF
			if key == ord('q'):
				server_socket.close()
				break
			if cnt == frames_to_count:
				try:
					fps = round(frames_to_count/(time.time()-st))
					st=time.time()
					cnt = 0
				except:
					pass
			cnt += 1
