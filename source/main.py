from email.policy import default
import record_audio as r
from rich.console import Console
from rich.prompt import Prompt

prompt = Prompt()
console = Console()
waiter_txt = "\nWciśnij dowolny klawisz, aby kontynuować... "


def main():
	output_path = "plik"
	user_input = ''
	debug_enabled = False
	while user_input != 'q':
		print()
		if debug_enabled: console.print("[ Debug enabled ]\n")
		#todo: poprawić to niżej
		if output_path != "": console.print(f"Nagrany plik:\n {output_path} \n")
		console.print("Podaj, czy chcesz:",
		"\t(1) Nagrać dźwięk",
		"\t(2) Odtworzyć dźwięk",
		"\t[dim]\[d - debug][/]",
		"\t[dim]\[q - wyjdź][/]", sep="\n")
		user_input = console.input("> ")
		print()
		match user_input:
			case '1': 
				record_audio(output_path)
			case '2': 
				if output_path != "": play_audio(output_path)
				else: console.input(f"Trzeba najpierw nagrać plik audio. {waiter_txt}")
			case 'l': debug_enabled = not debug_enabled
			case 'q': break
			case _: continue


def record_audio(file_name):
	file_name = prompt.ask("Podaj nazwę pliku: ", default=file_name)
	audio_setup = r.AudioSetup
	audio_setup.chunk = int(console.input("Podaj rozdzielczość: "))
	# todo: jakiś switch na inne formaty
	# audio_setup.input_format
	audio_setup.channel_number = int(prompt.ask(
		"Wprowadź liczbę kanałów", 
		choices=["1", "2"], 
		default="1"))
	audio_setup.rate = int(prompt.ask("Podaj częstotliwość próbkowania: ", default="4410"))
	console.print("Rozpoczęto nagrywanie")
	r.record_audio(audio_setup, file_name)	


def play_audio():
	pass


if __name__ == '__main__':
	main()