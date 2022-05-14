import socket

import pyaudio

PORT = 5000


def send_audio(audio_setup: tuple[int, int, int, int], ip_port: tuple[str, int]):
    p = pyaudio.PyAudio()
    chunk, input_format, chanel_number, rate = audio_setup

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
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
                client_socket.send(data)
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()


def receive_audio(audio_setup: tuple[int, int, int, int]):
    p = pyaudio.PyAudio()
    chunk, input_format, chanel_number, rate = audio_setup

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind(("", PORT))

        try:
            stream = p.open(
                format=input_format,
                channels=chanel_number,
                rate=rate,
                frames_per_buffer=chunk,
                output=True)
            while True:
                data, addr = server_socket.recv(chunk)
                stream.write(data)
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()
