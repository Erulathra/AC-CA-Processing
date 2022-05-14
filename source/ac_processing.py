import socket

import pyaudio

PORT = 5000


def send_audio(audio_setup: tuple[int, int, int, int], ip_port: tuple[str, int]):
    p = pyaudio.PyAudio()
    chunk, input_format, chanel_number, rate = audio_setup

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        client_socket.connect(ip_port)

        with p.open(
                format=input_format,
                channels=chanel_number,
                rate=rate,
                frames_per_buffer=chunk,
                input=True) as stream:

            while True:
                data = stream.read(chunk)
                client_socket.send(data)


def receive_audio(audio_setup: tuple[int, int, int, int]):
    p = pyaudio.PyAudio()
    chunk, input_format, chanel_number, rate = audio_setup

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind(("", PORT))

        with p.open(
                format=input_format,
                channels=chanel_number,
                rate=rate,
                frames_per_buffer=chunk,
                output=True) as stream:
            while True:
                data, addr = server_socket.recv(chunk)
                stream.write(chunk)
