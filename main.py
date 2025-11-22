import os
import sys
import difflib
import sounddevice as sd
import vosk
import queue
import json

if getattr(sys, 'frozen', False):
    # when executable
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(__file__)

model_path = os.path.join(base_path, "vosk-model-de-0.21")

# signals to interact with gpu-screen-recorder (https://git.dec05eba.com/gpu-screen-recorder/about/)
save_command = "pkill -SIGUSR1 -f gpu-screen-recorder"
stop_command = "pkill -SIGINT -f gpu-screen-recorder"

voice_commands = {
    "okay garmin video speichern": save_command,
    "okay garmin aufnahme stoppen": stop_command,
}

model = vosk.Model(model_path)
rec = vosk.KaldiRecognizer(model, 16000)
q = queue.Queue()

def callback(indata, frames, time, status):
    q.put(bytes(indata))

def find_best_match(spoken, commands, threshold=0.8):

    # if spoken contains a voice command
    contained = [cmd for cmd in commands if cmd in spoken]
    if contained:
        # return longest command
        return max(contained, key=len)

    # fuzzy matching
    matches = difflib.get_close_matches(spoken, commands, n=1, cutoff=threshold)
    return matches[0] if matches else None

def execute_command(command):
    os.system(command)

def listen_for_voice_command():
    try:
        with sd.RawInputStream(samplerate=16000, blocksize=500, dtype='int16', channels=1, callback=callback):
            print("Listening!")
            
            while True:
                data = q.get()
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    text = result.get('text', '')
                    print("Recognized: ", text)
                    match = find_best_match(text, voice_commands.keys())
                    if match:
                        print(f"Executed: {match}")
                        execute_command(voice_commands[match])
                    else:
                        print("No command executed.")
    except Exception as e:
        print(f"Error during speech recognition: {e}")
    except KeyboardInterrupt:
        print('\nExited.')

if __name__ == "__main__":
    listen_for_voice_command()