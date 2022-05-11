import source.process_audio as r
from rich.console import Console
from rich.prompt import Prompt
import os

def cls():
    os.system('cls' if os.name=='nt' else 'clear')


prompt = Prompt()
console = Console()
waiter_txt = "\nWciśnij dowolny klawisz, aby kontynuować... "

audio_setup = r.AudioSetup()


def main():
	output_path = ""
	user_input = ''
	debug_enabled = False
	while user_input != 'q':
		cls()
		print()
		if debug_enabled: console.print("[ Debug enabled ]\n")
		#todo: poprawić to niżej
		if output_path != "": console.print(f"Nazwa pliku:\n {output_path} \n")
		console.print("Podaj, czy chcesz:",
		"\t(1) Nagrać dźwięk",
		"\t(2) Odtworzyć dźwięk",
		"\t[dim]\[d - debug][/]",
		"\t[dim]\[q - wyjdź][/]", sep="\n")
		user_input = console.input("> ")
		print()
		match user_input:
			case '1': 
				output_path = record_audio(output_path)
			case '2': 
				if output_path != "": play_audio(output_path)
				else: console.input(f"Trzeba najpierw nagrać plik audio. {waiter_txt}")
			case 'l': debug_enabled = not debug_enabled
			case 'q': break
			case _: continue


def record_audio(file_name):
	if file_name == "": file_name = "plik"
	file_name = prompt.ask("Podaj nazwę pliku: ", default=file_name)
	audio_setup.chunk = int(prompt.ask("Podaj rozdzielczość: ", default=str(audio_setup.chunk)))
	console.print(f"Podaj format wejściowy:",
		"(1) Int8",
		"(2) Int16",
		"(3) Int24",
		"(4) Int32", sep="\n")
	input_format_chosen = int(prompt.ask("", default=str(audio_setup.input_format)))
	audio_setup.channel_number = int(prompt.ask(
		"Wprowadź liczbę kanałów", 
		choices=["1", "2"], 
		default="1"))
	audio_setup.rate = int(prompt.ask("Podaj częstotliwość próbkowania: ", default=str(audio_setup.rate)))
	console.print("Rozpoczęto nagrywanie")
	r.record_audio(audio_setup, file_name)
	return file_name


def play_audio():
	file_name = prompt.ask("Podaj nazwę pliku: ", default=file_name)
	audio_setup.chunk = int(console.input(f"Podaj rozdzielczość [{audio_setup.chunk}]: "))
	console.print("Odtwarzanie...")
	r.play_audio(audio_setup, file_name)


if __name__ == '__main__':
	main()