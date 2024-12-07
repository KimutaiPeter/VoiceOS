import logging
import threading
import time
from pynput import keyboard
from pynput.mouse import Button, Controller
import pyaudio
import wave
import sys
import whisper
import pythoncom
import Lama


pythoncom.CoInitialize()

program_ended=False
mouse =Controller()
hold=False
audio= pyaudio.PyAudio()
mic=False
model = whisper.load_model("small.en")
user_prompt=""
user_prompt_present=False
user_prompt_inprogress=False
sound_perception_inprogress=False

def thread_function():
    global mic,audio,user_prompt,user_prompt_present,sound_perception_inprogress,user_prompt_inprogress
    try:
        print("Starting hearing...")
        audio= pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16,channels=1,rate=44100,input=True,frames_per_buffer=1024,input_device_index=2)
        frames=[]
        while mic:
            data=stream.read(1024)
            frames.append(data)
        stream.stop_stream()
        stream.close()
        audio.terminate()
        sound_file=wave.open('myrecording.wav','wb')
        sound_file.setnchannels(1)
        sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        sound_file.setframerate(44100)
        sound_file.writeframes(b''.join(frames))
        sound_file.close()
    except KeyboardInterrupt:
        print("Interupted")
    except Exception as e:
        print("Some error",e)
    finally:
        print("Starting sound perception...")
        sound_perception_inprogress=True
        out = model.transcribe("myrecording.wav", language="english")
        print("You:",out['text'])
        sound_perception_inprogress=False
        user_prompt=out['text']
        user_prompt_inprogress=True
        if len(user_prompt)>5:
            print("Executing:",user_prompt)
            responce=Lama.run_conversation(user_prompt)
            print("AI:",responce)
            user_prompt_present=False
            user_prompt_inprogress=False
            user_prompt=""
        else:
            user_prompt_present=False
            user_prompt_inprogress=False
            user_prompt=""
        
    sys.exit()
    print('Exiting...')


def on_press(key):
    global hold,mic,program_ended,sound_perception_inprogress,user_prompt_inprogress

    try:
        if key == keyboard.Key.alt_l:
            if user_prompt_inprogress:
                print("Please wait for the task at hand to be complete")
            else:
                if hold==False:
                    hold=True
                    mic=True
                    listening_thread = threading.Thread(target=thread_function, args=())
                    if(listening_thread.is_alive()):
                        listening_thread.exit()
                    else:
                        listening_thread.start()
        if key== keyboard.Key.alt_gr:
            print(Lama.run_conversation("increase the volume by 90%"))
        if key== keyboard.Key.esc:
            program_ended=True
            return False

    except AttributeError:
        if key == keyboard.Key.alt_l:
            if hold==False:
                hold=True
                mic=True
                listening_thread = threading.Thread(target=thread_function, args=())
                if(listening_thread.is_alive()):
                    listening_thread.exit()
                else:
                    
                    logging.info("Main: Starting listening")
                    listening_thread.start()

    

def on_release(key):
    global hold,mic
    if key == keyboard.Key.esc:
        # Stop listener
        listener.stop()
        return False
    if key == keyboard.Key.alt_l:
        if not sound_perception_inprogress:
            print("Stoping sound recording...")
            hold=False
            mic=False



    

if __name__ == "__main__":

    # Collect events until released
    with keyboard.Listener(on_press=on_press,on_release=on_release) as listener:
        listener.join()

    

    