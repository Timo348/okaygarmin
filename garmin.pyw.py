import speech_recognition as sr
import keyboard
from rapidfuzz import fuzz
import time
import subprocess  
import simpleaudio as sa  # playsound entfernt, simpleaudio hinzugefügt

wake_words = {
    "okay garmin video speichern": lambda: keyboard.press_and_release('alt+f10'),
    "okay garmin genug gespielt für heute": lambda: keyboard.press_and_release('alt+f4'),
    "okay garmin gomme mode": lambda: (
        keyboard.press_and_release('t'),
        time.sleep(0.5),
        keyboard.write('/gamemode creative'),
        keyboard.press_and_release('enter')
    ),
    "okay garmin ab zu Leon": lambda: (
        keyboard.press_and_release('t'),
        time.sleep(0.5),
        keyboard.write('/tp Knuusper Einfachunbekannt'),
        keyboard.press_and_release('enter')
    ),
    "okay garmin hol Leon zu mir": lambda: (
        keyboard.press_and_release('t'),
        time.sleep(0.5),
        keyboard.write('/tp Einfachunbekannt Knuusper'),
        keyboard.press_and_release('enter')
    ),
    "okay garmin ab in die Kluft": lambda: subprocess.Popen(
        ['explorer', r'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Riot Games\League of Legends.lnk']
    ),
    "okay garmin starte Valorant": lambda: subprocess.Popen(
        ['explorer', r'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Riot Games\Valorant.lnk']
    ),
    "okay garmin stream starten": lambda: keyboard.press_and_release('ctrl+shift+0'),
    "okay garmin raus hier": lambda: keyboard.press_and_release('ctrl+shift+9'),
    "okay garmin pc ausschalten": lambda: subprocess.Popen(
        ["shutdown", "/s", "/t", "0"], shell=True
    ),
    "okay garmin schließ dich": lambda: (
        sa.WaveObject.from_wave_file(r"C:\Users\Timoh\Desktop\garmin\okaygarmin.wav")
        .play()
        
    )
}

threshold = 80

recognizer = sr.Recognizer()
mic = sr.Microphone()

print("...")
with mic as source:
    recognizer.adjust_for_ambient_noise(source)

while True:
    with mic as source:
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language="de-DE")
        print(f"Erkannt: {text}")

        for wake_word, action in wake_words.items():
            similarity = fuzz.ratio(text.lower(), wake_word)
            if similarity >= threshold:
                print(f"Wake Word erkannt! Aktion für '{wake_word}' wird ausgeführt.")
                try:
                    action()
                except Exception as e:
                    print(f"Fehler beim Ausführen der Aktion: {e}")
                break

    except sr.UnknownValueError:
        pass
    except sr.RequestError as e:
        print(f"Fehler bei der Spracherkennung: {e}")
