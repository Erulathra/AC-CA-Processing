import pyaudio

import ac_ca_processing as ac

PORT = 2137
# chunk, input_format, chanel_number, rate
audio_setup = (1024, pyaudio.paInt16, 2, 44100)
ac.receive_audio(audio_setup, PORT)
