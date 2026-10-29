# Jimmy (Microduck) – alle Skills trainieren und auf den Roboter bringen

## Ehrlicher Stand
- Fertig vortrainierte Policies (Laufen, Aufstehen, Sit/Stand, Ball kicken, Aufheben …) liegen schon
  offiziell auf Hugging Face: `pollen-robotics/microduck-policies`. Das ist der **schnellste Weg**:
  Du trainierst nichts selbst, der Roboter lädt sie.
- Eigene/zusätzliche Skills trainierst du mit diesem Repo. Dafür braucht man eine GPU. Ohne eigene GPU
  läuft es über Hugging Face Jobs (`--hf-jobs`, siehe `scripts/hf/README.md`).
- "Schlafen legen" gibt es hier noch **nicht** als Task (am nächsten dran: `SitStand` / `StandUp`).
  Das müsste als neue Env gebaut werden (Workflow in `AGENTS.md`).
- Es gibt keinen "alles in einer Policy"-Knopf: jeder Skill ist eine eigene Policy, der Roboter
  wechselt zwischen ihnen.

## Schritt 1 – Einrichten (einmalig)
```bash
git clone https://github.com/LennardOwnTest123006/microduck_rl_learn-Jimmy
cd microduck_rl_learn-Jimmy
huggingface-cli login      # eigenes HF-Konto
wandb login
```

## Schritt 2 – Alles trainieren
```bash
scripts/train_all_jimmy.sh smoke   # zuerst! 5 Iterationen pro Task, kostet fast nichts
scripts/train_all_jimmy.sh full    # dann echtes Training aller Skills auf HF Jobs
```
Skills: Laufen, Fall-Recovery, Aufstehen, Sitzen/Stehen, Ball kicken, Aufheben,
Rollschuh fahren (+ Swizzle, Crouch, Slope, StandUp), Rolle (Roulade), Drehung.

## Schritt 3 – Exportieren und veröffentlichen
Pro Skill (Run-Pfad steht in wandb):
```bash
uv run publish --task Mjlab-BallKick-Flat-MicroDuck \
  --wandb-run-path <entity/project/run_id> --checkpoint <N> \
  --repo <dein-user>/microduck-ball-kick --kind episodic --duration-s 4.0
```
Ein Gang (Laufen) bekommt stattdessen `--kind perpetual --slot walk`.
Nie ein `.pt` selbst in ONNX umwandeln – immer `publish`/`scripts/export.py` benutzen.

## Schritt 4 – Auf Jimmy installieren (auf dem Roboter)
```bash
sudo robotctl policy add ball-kick <dein-user>/microduck-ball-kick
sudo robotctl policy load walk <dein-user>/microduck-my-walk
robotctl robot do ball-kick
```
Die offiziellen, schon fertigen Skills nimmst du aus `pollen-robotics/microduck-policies`
(Anleitung im Repo `pollen-robotics/microduck`).

## Eigene Tricks
Neue Env nach dem Workflow in `AGENTS.md` bauen (nächstes Template wählen, Smoke-Test, trainieren),
dann wie oben veröffentlichen. Testen am PC vor dem Roboter: `uv run scripts/infer_policy.py --walking out.onnx`.
