import pyaudio

import ac_processing as ac

# chunk, input_format, chanel_number, rate
audio_setup = (1024, pyaudio.paInt16, 2, 44100)
ac.send_audio(audio_setup, ("192.168.0.18", 5000))
