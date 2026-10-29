"""Jimmy mit KI-Gehirn: normal reden, Claude versteht es und wählt den passenden Skill.

pip install anthropic SpeechRecognition pyaudio
export ANTHROPIC_API_KEY=...   (eigener Key, nie ins Repo schreiben)
Unerprobt: Mikrofon, Claude-Aufruf und robotctl-Syntax bitte am echten Roboter prüfen.
"""
import json
import subprocess
import anthropic
import speech_recognition as sr

MODEL = "claude-haiku-5-5"
# Skills, die auf Jimmy installiert sind (robotctl policy add <name> ...). Beschreibung hilft der KI.
SKILLS = {
    "sit": "hinsetzen",
    "stand": "aufstehen / hinstellen",
    "ball-kick": "gegen einen Ball treten",
    "pick": "etwas vom Boden aufheben",
    "sleep": "sich hinlegen und schlafen",
    "roulade": "Rolle machen",
    "spin": "sich drehen",
}
SYSTEM = (
    "Du bist das Gehirn von Jimmy, einem kleinen Laufroboter, Besitzer Lennard. "
    "Lennard redet normal mit dir. Wähle den Skill, der passt, oder null, wenn nichts passt "
    "(Smalltalk, unklar). Antworte NUR mit JSON: "
    '{"skill": <name oder null>, "say": <kurze freundliche Antwort auf Deutsch>}. Skills: '
    + json.dumps(SKILLS, ensure_ascii=False)
)

client = anthropic.Anthropic()

def decide(text):
    msg = client.messages.create(model=MODEL, max_tokens=200, system=SYSTEM,
                                 messages=[{"role": "user", "content": text}])
    try:
        return json.loads(msg.content[0].text)
    except json.JSONDecodeError:
        return {"skill": None, "say": ""}

def main():
    rec, mic = sr.Recognizer(), sr.Microphone()
    with mic:
        rec.adjust_for_ambient_noise(mic)
    print("Rede mit Jimmy (Strg+C beendet)")
    while True:
        with mic:
            audio = rec.listen(mic)
        try:
            text = rec.recognize_google(audio, language="de-DE")
        except (sr.UnknownValueError, sr.RequestError):
            continue
        print("Lennard:", text)
        out = decide(text)
        print("Jimmy:", out.get("say", ""))
        skill = out.get("skill")
        if skill in SKILLS:
            subprocess.run(["robotctl", "robot", "do", skill], check=False)

if __name__ == "__main__":
    main()
