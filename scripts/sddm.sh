#!/usr/bin/env bash
# SPDX-License-Identifier: GPL-3.0-only
set -euo pipefail
project_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
command -v sddm-greeter-qt6 >/dev/null || { echo 'Falta sddm-greeter-qt6 (SDDM Qt6).'; exit 1; }
work_dir=$(mktemp -d)
trap 'rm -rf -- "$work_dir"' EXIT
cp -a "$project_dir/assets/sddm" "$work_dir/theme"
if [[ $# -gt 0 ]]; then
 cp -- "$1" "$work_dir/background.png"
else
 curl --fail --location --proto '=https' --tlsv1.2 --max-time 120 \
  'https://misc-assets.raycast.com/wallpapers/red_distortion_1_preview.png' -o "$work_dir/background.png"
fi
python - "$work_dir/background.png" <<'PY'
import struct,sys
from pathlib import Path
b=Path(sys.argv[1]).read_bytes()
if b[:8]!=b'\x89PNG\r\n\x1a\n' or b[12:16]!=b'IHDR': raise SystemExit('El fondo debe ser un PNG válido.')
w,h=struct.unpack('>II',b[16:24])
if w<640 or h<360 or w*h>100_000_000: raise SystemExit('Dimensiones no admitidas.')
print('Fondo PNG:',w,'×',h)
PY
printf '[General]\nbackground=%s\n' "$work_dir/background.png" > "$work_dir/theme/theme.conf"
# Actual options are detected on destination, not assumed from another SDDM release.
greeter_help=$(sddm-greeter-qt6 --help 2>&1)
if [[ "$greeter_help" == *--test-mode* ]]; then test_flag=--test-mode
elif [[ "$greeter_help" == *--test* ]]; then test_flag=--test
else echo 'SDDM no ofrece un modo de prueba compatible.'; exit 1; fi
set +e
QT_QPA_PLATFORM=offscreen timeout 5s sddm-greeter-qt6 "$test_flag" --theme "$work_dir/theme" > "$work_dir/preview.log" 2>&1
preview_result=$?
set -e
cat "$work_dir/preview.log"
if [[ $preview_result != 0 && $preview_result != 124 ]]; then echo 'Falló la prueba del greeter.'; exit 1; fi
if rg -i 'is not installed|is not a type|failed to load|Error loading|Error decoding|libpng error|SyntaxError|ReferenceError|TypeError|file:.*:[0-9]+:[0-9]+:' "$work_dir/preview.log"; then
 echo 'Errores QML: se conserva el login anterior.'; exit 1
fi
printf '[General]\nbackground=/usr/share/backgrounds/custom/cf-kde-raycast.png\n' > "$work_dir/theme/theme.conf"
# Privileges are limited to these system assets and Theme/Current; PAM/autologin untouched.
sudo bash -s -- "$work_dir" <<'ROOT'
set -euo pipefail
work_dir=$1
stamp=$(date +%Y%m%d-%H%M%S)-$$
backup_dir=/var/lib/cf-kde/backups/$stamp
mkdir -p -- "$backup_dir"
chmod 700 "$backup_dir"
# Reject linked targets before backing up or editing privileged files.
for target in /usr/share/sddm/themes/cf-kde /usr/share/backgrounds/custom/cf-kde-raycast.png /etc/sddm.conf.d/zz-cf-kde.conf /etc/sddm.conf; do
 parent=$target
 while [[ $parent != / ]]; do
  [[ ! -L $parent ]] || { echo "Ruta del login enlazada: $parent; resolver antes de instalar."; exit 1; }
  parent=$(dirname -- "$parent")
 done
done
paths=(usr/share/sddm/themes/cf-kde usr/share/backgrounds/custom/cf-kde-raycast.png etc/sddm.conf.d/zz-cf-kde.conf etc/sddm.conf)
for path in "${paths[@]}"; do
 if [[ -e /$path || -L /$path ]]; then
  mkdir -p -- "$backup_dir/files/$(dirname -- "$path")"
  cp -a -- "/$path" "$backup_dir/files/$path"
  printf '%s\n' "$path" >> "$backup_dir/present"
 fi
 printf '%s\n' "$path" >> "$backup_dir/paths"
done
cat > "$backup_dir/restore.sh" <<'RESTORE'
#!/usr/bin/env bash
set -euo pipefail
[[ $(id -u) == 0 ]] || { echo 'Ejecutar con sudo.'; exit 1; }
backup_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
# Exact allowed paths; preserve current files before recovering the old ones.
recovery_dir="$backup_dir/before-restore-$(date +%Y%m%d-%H%M%S)"
for path in usr/share/sddm/themes/cf-kde usr/share/backgrounds/custom/cf-kde-raycast.png etc/sddm.conf.d/zz-cf-kde.conf etc/sddm.conf; do
 if [[ -e /$path || -L /$path ]]; then
  mkdir -p -- "$recovery_dir/$(dirname -- "$path")"
  mv -- "/$path" "$recovery_dir/$path"
 fi
 if [[ -e "$backup_dir/files/$path" || -L "$backup_dir/files/$path" ]]; then
  mkdir -p -- "/$(dirname -- "$path")"
  cp -a -- "$backup_dir/files/$path" "/$path"
 fi
done
echo 'SDDM restaurado; no se reinició display-manager.'
RESTORE
chmod 700 "$backup_dir/restore.sh"
mkdir -p /usr/share/sddm/themes /usr/share/backgrounds/custom /etc/sddm.conf.d
rm -rf -- /usr/share/sddm/themes/cf-kde
cp -a -- "$work_dir/theme" /usr/share/sddm/themes/cf-kde
chmod -R a+rX /usr/share/sddm/themes/cf-kde
install -m 644 "$work_dir/background.png" /usr/share/backgrounds/custom/cf-kde-raycast.png
printf '[Theme]\nCurrent=cf-kde\n' > /etc/sddm.conf.d/zz-cf-kde.conf
# Main sddm.conf has priority: change only Theme/Current when that key already exists.
if [[ -f /etc/sddm.conf ]] && python - <<'PY'
import configparser
p=configparser.ConfigParser(strict=False); p.read('/etc/sddm.conf')
raise SystemExit(0 if p.has_option('Theme','Current') else 1)
PY
then kwriteconfig6 --file /etc/sddm.conf --group Theme --key Current cf-kde; fi
python - <<'PY'
import configparser,glob
p=configparser.ConfigParser(strict=False)
p.read(sorted(glob.glob('/usr/lib/sddm/sddm.conf.d/*.conf'))+sorted(glob.glob('/etc/sddm.conf.d/*.conf'))+['/etc/sddm.conf'])
if p.get('Theme','Current',fallback='')!='cf-kde': raise SystemExit('Otra configuración tiene prioridad. Usar el respaldo para revertir SDDM.')
PY
printf 'Login instalado sin cerrar sesión. Restauración: sudo bash %s/restore.sh\n' "$backup_dir"
ROOT
