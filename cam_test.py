import cv2
import socket
import pickle
import struct
import time

# 소켓 설정
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = "172.30.1.33"  # 윈도우 PC의 IP 주소
port = 5000  # 사용하려는 포트
server_socket.bind((host_ip, port))
server_socket.listen(5)
print(f"Listening on {host_ip}:{port}")

# 클라이언트 연결 대기
client_socket, addr = server_socket.accept()
print(f"Connection from: {addr}")

# 카메라 설정
cap = cv2.VideoCapture(0)  # 내장 카메라 사용 (0번 카메라)

# FPS 설정
fps_limit = 1 / 30  # 30fps 제한
prev_time = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 현재 시간
    current_time = time.time()

    # 프레임 전송 제한
    if current_time - prev_time >= fps_limit:
        prev_time = current_time

        # 화질 저하 (해상도 줄이기)
        resized_frame = cv2.resize(frame, (640, 360))  # 640x360으로 축소

        # JPEG 압축으로 화질 저하
        _, encoded_frame = cv2.imencode(".jpg", resized_frame, [cv2.IMWRITE_JPEG_QUALITY, 50])  # 화질 50 설정

        # 프레임 직렬화 후 전송
        data = pickle.dumps(encoded_frame)
        message = struct.pack("Q", len(data)) + data
        client_socket.sendall(message)

cap.release()
client_socket.close()
server_socket.close()
