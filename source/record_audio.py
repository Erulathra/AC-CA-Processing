import pyaudio
import wave

class AudioSetup:
	chunk = 1024
	input_format = pyaudio.paInt16
	channel_number = 1
	rate = 44100

def record_audio(audio_setup : AudioSetup, file_name):
	p = pyaudio.PyAudio()

	stream = p.open(
		format=audio_setup.input_format,	
		channels=audio_setup.channel_number,
		rate=audio_setup.rate,
		frames_per_buffer=audio_setup.chunk,
		input=True)
	
	audio_input = []
	try:
		print("Wciśnij Ctrl+C, aby zakończyć nagrywanie")
		while True:
			data = stream.read(audio_setup.chunk)
			audio_input.append(data)
	except KeyboardInterrupt:
		print('Zakończono nagrywanie')
	stream.stop_stream()
	stream.close()
	p.terminate()
	save_wav_file(audio_input, audio_setup, file_name, p)


def save_wav_file(audio_input, audio_setup : AudioSetup, file_name : str, p : pyaudio.PyAudio):
	wf = wave.open(file_name+".wav", 'wb')
	wf.setnchannels(audio_setup.channel_number)
	wf.setsampwidth(p.get_sample_size(audio_setup.input_format))
	wf.setframerate(audio_setup.rate)
	wf.writeframes(b''.join(audio_input))
	wf.close()