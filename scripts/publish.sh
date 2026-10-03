#!/usr/bin/env bash
# Run explicitly when ready to publish this project to GitHub.
set -euo pipefail
project_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
cd -- "$project_dir"
command -v gh >/dev/null || { echo 'Instalar GitHub CLI: sudo pacman -S github-cli'; exit 1; }
gh auth status >/dev/null 2>&1 || { echo 'Primero: gh auth login'; exit 1; }
git config user.name >/dev/null && git config user.email >/dev/null || {
 echo 'Configurar git config user.name y git config user.email (puede ser el correo noreply de GitHub).'; exit 1;
}
python -m unittest discover -s tests -v
python scripts/verify.py
if [[ -n $(git remote) ]]; then echo 'Ya existe un remoto. Revisar git remote -v y publicar manualmente.'; exit 1; fi
git add -- .
if ! git diff --cached --quiet; then git commit -m 'Cf-Kde 1.0.0: tema KDE reproducible para CachyOS'; fi
gh repo create Cf-Kde --public --description 'Tema oscuro para CachyOS KDE Plasma: docks, reloj centrado, KRunner y decoración Windows' --source . --remote origin --push
