"""Sprachsteuerung für Jimmy: Mikrofon -> Text -> robotctl-Befehl.

Laufen auf dem Rechner, auf dem `robotctl` funktioniert (am Roboter oder per Netzwerk).
Installieren: pip install SpeechRecognition pyaudio
Skills müssen vorher mit `robotctl policy add <name> User1/microduck-<name>` installiert sein.
Unerprobt: Mikrofon/Erkennung und genaue robotctl-Syntax bitte am echten Roboter prüfen.
"""
import subprocess
import speech_recognition as sr

NAME = "jimmy"
# Stichwort (deutsch/englisch) -> Skill-Name in robotctl
COMMANDS = {
    "sitz": "sit", "sit": "sit",
    "steh": "stand", "stand": "stand", "aufstehen": "stand",
    "ball": "ball-kick", "schieß": "ball-kick", "kick": "ball-kick",
    "heb": "pick", "pick": "pick", "aufheben": "pick",
    "schlaf": "sleep", "sleep": "sleep",
    "roll": "roulade", "dreh": "spin", "spin": "spin",
}

def run(skill):
    print(f"-> robotctl robot do {skill}")
    subprocess.run(["robotctl", "robot", "do", skill], check=False)

def main():
    rec, mic = sr.Recognizer(), sr.Microphone()
    with mic:
        rec.adjust_for_ambient_noise(mic)
    print(f"Sag '{NAME} …' (Strg+C zum Beenden)")
    while True:
        with mic:
            audio = rec.listen(mic)
        try:
            text = rec.recognize_google(audio, language="de-DE").lower()
        except (sr.UnknownValueError, sr.RequestError):
            continue
        print("gehört:", text)
        if NAME not in text:
            continue
        for key, skill in COMMANDS.items():
            if key in text:
                run(skill)
                break

if __name__ == "__main__":
    main()
