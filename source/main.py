import os

from rich.console import Console
from rich.prompt import Prompt

import ac_ca_processing as r

#TODO: to trzeba uaktualnić
def get_device_index(p):
    device_index = None
    for i in range(p.get_device_count()):
        devinfo = p.get_device_info_by_index(i)
        for keyword in ["mic", "input"]:
            if keyword in devinfo["name"].lower():
                print("Found an input: device %d - %s" % (i, devinfo["name"]))
                device_index = i
                return device_index
    if device_index is None:
        print("No preferred input found; using default input device.")

    return device_index


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


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
        # todo: poprawić to niżej
        if output_path != "": console.print(f"Nazwa pliku:\n {output_path} \n")
        console.print("Podaj, czy chcesz:",
                      "\t(1) Nagrać dźwięk",
                      "\t(2) Odtworzyć dźwięk",
                      "\t[dim]\[d - debug][/]",
                      "\t[dim]\[q - wyjdź][/]", sep="\n")
        user_input = console.input("> ")
        print()
        if user_input == '1':
            output_path = record_audio(output_path)
        elif user_input == '2':
            play_audio()
        elif user_input == 'l':
            debug_enabled = not debug_enabled
        elif user_input == 'q':
            break
        else:
            continue


def record_audio(file_name):
    if file_name == "":
        file_name = "plik"
    file_name = prompt.ask("Podaj nazwę pliku: ", default=file_name)
    audio_setup.chunk = int(prompt.ask("Podaj rozdzielczość: ", default=str(audio_setup.chunk)))
    console.print(f"Podaj format wejściowy:",
                  "(1) Int8",
                  "(2) Int16",
                  "(3) Int24", sep="\n")
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
    file_name = prompt.ask("Podaj nazwę pliku: ", default="plik.wav")
    audio_setup.chunk = int(console.input(f"Podaj rozdzielczość [{audio_setup.chunk}]: "))
    console.print("Odtwarzanie...")
    r.play_audio(audio_setup, file_name)


if __name__ == '__main__':
    main()
