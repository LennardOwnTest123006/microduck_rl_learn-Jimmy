#!/usr/bin/env bash
# Trains every skill for Jimmy on Hugging Face Jobs (no local GPU needed).
# Usage: scripts/train_all_jimmy.sh smoke   # 5-iteration check of every task (cheap, run first!)
#        scripts/train_all_jimmy.sh full    # real training runs
set -euo pipefail
MODE="${1:-smoke}"

# task id | iterations (budgets from AGENTS.md: gaits 4000-6000, tricks ~1000-3000)
TASKS=(
  "Mjlab-Velocity-Flat-MicroDuck|5000"          # walking
  "Mjlab-VelStand-Flat-MicroDuck|6000"          # walking + fall recovery
  "Mjlab-StandUp-Flat-MicroDuck|3000"           # stand up
  "Mjlab-SitStand-Flat-MicroDuck|3000"          # sit <-> stand
  "Mjlab-BallKick-Flat-MicroDuck|3000"          # kick a ball
  "Mjlab-GroundPick-Flat-MicroDuck|3000"        # pick something up
  "Mjlab-Velocity-Flat-MicroDuck-Rollers|5000"  # roller skating
  "Mjlab-Velocity-Swizzle-MicroDuck|3000"       # skating swizzle
  "Mjlab-RollerCrouch-Flat-MicroDuck|2000"
  "Mjlab-RollerSlope-Flat-MicroDuck|3000"
  "Mjlab-RollerStandUp-Flat-MicroDuck|3000"
  "Mjlab-Roulade-Flat-MicroDuck|2000"           # roll trick
  "Mjlab-Spin-Flat-MicroDuck|2000"              # spin trick
)

for entry in "${TASKS[@]}"; do
  task="${entry%%|*}"; rest="${entry#*|}"; iters="${rest%% *}"
  if [ "$MODE" = "smoke" ]; then
    echo ">>> SMOKE $task"
    uv run train "$task" --env.scene.num-envs 64 --agent.max_iterations 5 --hf-jobs
  else
    echo ">>> TRAIN $task ($iters iters)"
    uv run train "$task" --env.scene.num-envs 4096 --agent.max_iterations "$iters" --hf-jobs
  fi
done
