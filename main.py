import sys
import os
import pyautogui
import threading
from modules import notify, engine
from modules.notify import timeinfo
import time
import datetime
import webbrowser
import random
from modules.engine import speak, listen
from modules.nova_face import NovaFace
from modules.functions import search_wikipedia, interactive_youtube, advanced_media_control
from modules.engine_nova import NOVA_BRAIN
#from modules.auth import NovaAuthenticator
import customtkinter
import pyttsx3

brain_instance = NOVA_BRAIN() 

def PowerOn():
    face = NovaFace()
    face.start()
    time.sleep(2) 
    global brain_instance
    face.write_log("💱 Booting Nova...")
    time.sleep(2)

    try:
        notify.startnote()
    except Exception as e:
        face.write_log(f"Notification Error: {e}")

    face.write_log("🟢 NOVA IS ONLINE")
    speak(">>>NOVA is Online")
    

    while True:
        face.change_emotion("listening")
        
        command = listen(face) 

        if not command or len(command.strip().split()) < 1: 
            continue 
        
        command = command.lower()
        face.write_log(f"Heard: {command}")

        # --- 2. SPECIAL SKILLS (INTERCEPTORS) ---
        media_msg = advanced_media_control(command, face)
        if media_msg:
            speak(media_msg)
            continue
    
        wiki_result = search_wikipedia(command, face)
        if wiki_result:
            speak(wiki_result)
            continue

        # --- 3. COMMAND LOGIC ---
        if "hello" in command or "hi" in command:
            face.change_emotion("happy")
            speak("Hi there! How can I help you today?")
        
        elif "time" in command:
            face.change_emotion("neutral")
            current_time = datetime.datetime.now().strftime('%I:%M %p')
            timeinfo(current_time)
            face.write_log(current_time)
            speak(f"The current time is {current_time}")

        elif "party mode" in command or "open youtube" in command:
            response = interactive_youtube(face, speak, listen)
            speak(response)

        elif "open website" in command:
            domain = command.replace("open website", "").strip()
            webbrowser.open(f"https://www.google.com/{domain}")
            speak(f"Opening {domain}")

        elif "search for" in command or "google" in command:
            search_query = command.replace("search for", "").replace("google", "").strip()
            speak(f"Searching for {search_query} on Google.")
            webbrowser.open(f"https://google.com{search_query}")

        elif "lag" in command or "game mode" in command:
            face.change_emotion("happy")
            speak("Activating low latency mode for Gaming.")
            import os
            os.system("powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c")
            os.system("ipconfig /flushdns")
            speak("Optimization complete.")

        elif "turbo" in command or "fan booster" in command:
            face.change_emotion("happy")
            face.write_log("Engaging Turbo Mode...")
            speak("Engaging turbo fans and ultimate performance.")
            os.system("powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c")

        elif "clean slate" in command or "mop" in command:
            face.write_log("Purging background apps...")
            speak("Closing background apps. Keeping the game open.")
            
            apps_to_kill = ["chrome.exe", "msedge.exe", "spotify.exe", "steam.exe", "vlc.exe", "sublime_text.exe", "RobloxPlayerBeta.exe"]
            
            for app in apps_to_kill:
                os.system(f"taskkill /f /im {app}")
            
            face.write_log("System Cleaned.")
            speak("Memory cleared. You're ready to game.")

        elif "close" in command or "sweep" in command:
            import pyautogui
            face.write_log("CLOSING WINDOW...")
            face.change_emotion("neutral")
            pyautogui.hotkey('alt','f4')

        elif "goodnight" in command or "shut down" in command:
            face.change_emotion("sad")
            speak("Goodnight, boss. Turning off the system now.")
            face.write_log("SHUTTING DOWN...")
            time.sleep(2)
            os.system("shutdown /s /t 5")

        elif "stealth on" in command or "hide it" in command:
            import pyautogui
            face.change_emotion("neutral")
            face.write_log("INITIATING STEALTH MODE...")
          
            pyautogui.press('volumemute')
            
            pyautogui.hotkey('win', 'd')
            
            webbrowser.open("https://www.youtube.com/watch?v=ucRsatGCeKg&list=PLFhDY9NOas7Woo-S5YHpITmwQpPjZffji") 
            
            face.write_log("SYSTEM MUTED & HIDDEN.")
            print("Nova: Stealth Mode Active (System Muted)")

        elif "stealth off" in command or "show it" in command:
            import pyautogui
            pyautogui.press('volumemute')
            face.write_log("Stealth Mode Deactivated.")
            speak("Welcome back. Audio restored.")

        elif "stop" in command or "exit" in command:
            face.change_emotion("sad")
            speak("Powering OFF.")
            break

        else:
            face.change_emotion("happy")
            resp = brain_instance.get_response(command, face)
            if resp:
                speak(resp)
            else:
                speak("I'm sorry, I couldn't process that.")

if __name__ == "__main__":
    PowerOn()
    #auth = NovaAuthenticator()
    #user = auth.run() 

    #if user:
    #    print(f"System Unlocked for {user}")
    #   PowerOn(user) 
    #else:
    #    print("Unauthorized Access. System Shutdown.")
    #    sys.exit()