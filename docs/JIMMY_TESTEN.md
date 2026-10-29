# Jimmy am PC testen (alle Skills, per Tastatur steuern)

`scripts/infer_policy.py` ist der Test-Simulator: 3D-Fenster, Steuerung per Tastatur, mehrere Policies gleichzeitig.
Es braucht keine GPU. ACHTUNG: es nutzt `termios` (Linux/Mac). Unter Windows deshalb **WSL2 (Ubuntu)** verwenden.

## Windows: WSL2 einrichten (einmalig)
PowerShell als Administrator: `wsl --install -d Ubuntu`, PC neu starten, Ubuntu-Benutzer anlegen.
In Ubuntu: `curl -LsSf https://astral.sh/uv/install.sh | sh`, dann Terminal neu öffnen.
Fenster: Windows 11 zeigt Linux-Fenster direkt an (WSLg).

## Policies besorgen
- Dein eigenes Gehen: `output.onnx` (aus Colab, Schritt 3 der Anleitung) nach WSL kopieren.
- Offizielle fertige Skills (Stehen, Sit/Stand, Kicks, Roulade, Aufheben):
  `uv run hf download pollen-robotics/microduck-policies --local-dir policies` und dann `ls policies`
  (Dateinamen z.B. `velstand.onnx`, `alpha_sitstand.onnx`; die genauen Namen stehen nach dem Download im Ordner).

## Alles gleichzeitig starten
```bash
uv run scripts/infer_policy.py --new-cmd-obs \
  --walking output.onnx \
  --sitstand policies/<sitstand>.onnx \
  --kick-left policies/<kick-left>.onnx --kick-right policies/<kick-right>.onnx \
  --roulade policies/<roulade>.onnx
```
Nur die Optionen angeben, für die du eine Datei hast. Tasten (im Terminal tippen, nicht im Fenster):
Pfeile = laufen/drehen, Leertaste = anhalten, **Y = hinsetzen/aufstehen**, **K / L = Kick links/rechts**,
**R = Rolle**, G = Aufheben, B = Körperpose-Modus, H = Kopf-Modus (Z/S/Pfeile/A/E), T = Policy an/aus, Q = Ende.
Eine Taste funktioniert nur, wenn die passende Policy per `--…` geladen wurde.
