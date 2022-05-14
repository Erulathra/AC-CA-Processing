import pyaudio

import ac_ca_processing as ac
import threading

PORT = 2137

audio_setup = (128, pyaudio.paInt16, 2, 44100)

sender_thread = threading.Thread(target=ac.send_audio, args=(audio_setup, ("192.168.0.19", PORT)))
receiver_thread = threading.Thread(target=ac.receive_audio, args=(audio_setup, PORT))

receiver_thread.start()
input("Naciśnij enter aby rozpocząć połączenie")
print("Rozpoczynam połączenie")
sender_thread.start()