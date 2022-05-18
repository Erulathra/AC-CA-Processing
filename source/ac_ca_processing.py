import socket

import pyaudio


def send_audio(audio_setup: tuple[int, int, int, int], ip_port: tuple[str, int]):
    p = pyaudio.PyAudio()
    chunk, input_format, chanel_number, rate = audio_setup

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(ip_port)

        try:
            stream = p.open(
                format=input_format,
                channels=chanel_number,
                rate=rate,
                frames_per_buffer=chunk,
                input=True)

            while True:
                data = stream.read(chunk)
                client_socket.sendall(data)
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()


def receive_audio(audio_setup: tuple[int, int, int, int], port):
    p = pyaudio.PyAudio()
    chunk, input_format, chanel_number, rate = audio_setup

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(("", port))
        server_socket.listen()

        conn, addr = server_socket.accept()
        print(f"Connected with: {addr}")

        try:
            stream = p.open(
                format=input_format,
                channels=chanel_number,
                rate=rate,
                frames_per_buffer=chunk,
                output=True)
            while True:
                data = conn.recv(chunk)
                stream.write(data)
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()
