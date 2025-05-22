import sounddevice as sd
import soundfile as sf
from pynput import keyboard
import numpy as np
import threading
import os
import random
from colorama import Fore, Style, init
import win32api
import win32con

# Run this line to find your audio devices
# print(sd.query_devices())

HEADPHONE_DEVICE = 4          # Replace with ur device index
VIRTUAL_MIC_DEVICE = 10        # Replace with ur device index
SOUND_BITES_FOLDER = os.getcwd() + "\sounds"
TARGET_PEAK_VOLUME = 0.2225  # Adjust as u like

all_ansi_colors = [Fore.RED,Fore.BLUE,Fore.CYAN,Fore.GREEN,Fore.MAGENTA,Fore.LIGHTBLUE_EX,Fore.LIGHTGREEN_EX,Fore.LIGHTMAGENTA_EX,Fore.LIGHTCYAN_EX,Fore.YELLOW,Fore.LIGHTRED_EX,Fore.WHITE]

num_pad_layout = {
    # DONT INCLUDE THE .mp3 AT THE END

    # Num Pad 1 
    97: "Random Sound",
    # Num Pad 2
    98: "donotinvestigate",
    # Num Pad 3
    99: "iregreteverythingivedone",
    # Num Pad 4
    100: "nuke",
    # Num Pad 5
    101: "ceoofisis",
    # Num Pad 6
    102: "darkevilpoison",
    # Num Pad 7
    103: "tookyoursoul",
    # Num Pad 8
    104: "holyfuckingshit",
    # Num Pad 9
    105: "evilpoisonmoneygang"
}
def is_numlock_enabled():
    return win32api.GetKeyState(win32con.VK_NUMLOCK)

def get_all_paths(folder_path):
    all_paths = []
    for root, dirs, files in os.walk(folder_path):
        for name in dirs + files:
            full_path = os.path.join(root, name)
            all_paths.append(full_path)
    return all_paths

def play_on_device(data, samplerate, device_index):
    try:
        with sd.OutputStream(
            samplerate=samplerate,
            channels=data.shape[1],
            dtype='float32',
            device=device_index
        ) as stream:
            stream.write(data)
    except Exception as e:
        print(f"Error playing on device {device_index}: {e}")

def center_text(text, ignored_chars=0, end_flag=None):
    terminal_width = os.get_terminal_size().columns
    padding = abs((terminal_width - (len(text) - ignored_chars)) // 2)
    print(" " * padding, end="")
    if end_flag is None:
        print(text)
    else:
        print(text, end=end_flag)

def normalize_audio(data, target_peak):
    peak = np.max(np.abs(data))
    if peak > 0:
        data = data * (target_peak / peak)
    return data

def play_sound_to_both_devices(file_path):
    try:
        data, samplerate = sf.read(file_path, always_2d=True)
        data = data.astype(np.float32)

        data = normalize_audio(data, TARGET_PEAK_VOLUME)

        threading.Thread(target=play_on_device, args=(data, samplerate, HEADPHONE_DEVICE)).start()
        threading.Thread(target=play_on_device, args=(data, samplerate, VIRTUAL_MIC_DEVICE)).start()
    except Exception as e:
        print(f"Error playing sound: {e}")

def on_press(key):
    global recent_sound_bites
    try:
        if num_pad_layout[key.vk] is not None:
            if num_pad_layout[key.vk] == "Random Sound":
                
                while True:
                    random_sound_bite = sound_bite_list[random.randint(0, len(sound_bite_list) - 1)]
                    if random_sound_bite not in recent_sound_bites: 
                        recent_sound_bites.append(random_sound_bite)
                        if len(recent_sound_bites) > 10:
                            recent_sound_bites.pop(0)
                        break
                    
                temp_str = random_sound_bite.split("\\")
                
                center_text("Playing Random Sound: ")
                center_text(f"{Style.BRIGHT}{all_ansi_colors[random.randint(0, len(all_ansi_colors) - 1)]}" + temp_str.pop()[:-4] + f"{Style.RESET_ALL}", 12)
                threading.Thread(target=play_sound_to_both_devices, args=(random_sound_bite,)).start()
            else:
                threading.Thread(target=play_sound_to_both_devices, args=(SOUND_BITES_FOLDER + "\\" + num_pad_layout[key.vk] + ".mp3",)).start()
    except:
        pass

sound_bite_list = get_all_paths(SOUND_BITES_FOLDER)
recent_sound_bites = []
print("\n")
center_text(f"{Style.BRIGHT}{Fore.RED}N {Fore.CYAN}U{Fore.YELLOW} K {Fore.BLUE}E {Fore.GREEN}A{Fore.LIGHTBLUE_EX} H{Fore.MAGENTA} O{Fore.LIGHTRED_EX} L{Fore.LIGHTBLACK_EX} I{Fore.LIGHTGREEN_EX} C {Fore.LIGHTWHITE_EX}S {Fore.LIGHTYELLOW_EX} S {Fore.YELLOW}O {Fore.LIGHTMAGENTA_EX}U {Fore.RED}N{Fore.CYAN} D{Fore.LIGHTBLACK_EX} B{Fore.LIGHTGREEN_EX} O {Fore.MAGENTA}A {Fore.YELLOW}R {Fore.CYAN}D{Style.RESET_ALL}\n\n\n", 116)
center_text(f"{Style.BRIGHT}{Fore.CYAN}Soundboard Layout:{Style.RESET_ALL}\n\n", 15)

if num_pad_layout[97] is not None:
    text = "Num Pad " + str(97 - 96) + ": " + num_pad_layout[97]
else:
    text = "Num Pad " + str(97 - 96) + ": " + f"{Style.BRIGHT}{Fore.RED}Not Set{Style.RESET_ALL}"

terminal_width = os.get_terminal_size().columns
padding = abs((terminal_width - (len(text))) // 2)
menu_padding = " " * padding

for i in range(97,106):
    if num_pad_layout[i] is not None:
        print(f"{Style.BRIGHT}{all_ansi_colors[random.randint(0, len(all_ansi_colors) - 1)]}" + menu_padding + "Num Pad " + str(i - 96) + ": " + num_pad_layout[i] + f"{Style.RESET_ALL}")
    else:
        print(menu_padding + "Num Pad " + str(i - 96) + ": " + f"{Style.BRIGHT}{Fore.RED}Not Set{Style.RESET_ALL}")
print("\n")

if not is_numlock_enabled():
    center_text(f"{Style.BRIGHT}{Fore.RED}T U R N  O N  Y O U R  N U M  L O C K  R E T A R D{Style.RESET_ALL}", 15)

random_sound_bite = sound_bite_list[random.randint(0, len(sound_bite_list) - 1)]
temp_str = random_sound_bite.split("\\")
center_text("Playing Random Sound: ")
center_text(f"{Style.BRIGHT}{all_ansi_colors[random.randint(0, len(all_ansi_colors) - 1)]}" + temp_str.pop()[:-4] + f"{Style.RESET_ALL}", 12)
threading.Thread(target=play_sound_to_both_devices, args=(random_sound_bite,)).start()

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()

    
