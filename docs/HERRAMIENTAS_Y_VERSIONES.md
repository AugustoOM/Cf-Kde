# Herramientas y versiones

Medidas en el equipo de referencia el 2026-10-03. Son versiones de referencia, no paquetes bloqueados para otras máquinas. CachyOS/Arch es rolling release; se usan las bibliotecas instaladas coherentemente en cada destino.

## Componentes y aplicaciones

| Paquete | Versión registrada |
| --- | --- |
| plasma-workspace | 6.7.5-1.1 |
| kwin | 6.7.5-1.1 |
| sddm | 0.21.0-8 |
| qt6-base | 6.11.2-3.1 |
| qt6-declarative | 6.11.2-2.1 |
| qt6-svg | 6.11.2-1.1 |
| qt6-5compat | 6.11.2-1.1 |
| dolphin | 26.08.1-1.1 |
| breeze | 6.7.5-1.1 |
| kdecoration | 6.7.5-1.1 |
| kiconthemes | 6.30.0-1.1 |
| kitty | 0.49.2-1.1 |
| chromium | 153.0.8010.52-1.1 |
| firefox | 157.0-1.1 |
| spotify-launcher | 0.6.6-2.1 |
| cmake | 4.4.4-1.1 |
| extra-cmake-modules | 6.30.0-1 |
| gcc | 16.2.1+r23+gd564253eb6c8-1 |
| make | 4.4.1-3.1 |
| git | 2.56.0-1.1 |
| curl | 8.22.0-1.1 |
| jq | 1.8.2-1.1 |
| python | 3.14.7-2 |
| python-dbus | 1.5.0-1 |
| python-gobject | 3.56.3-1 |
| kservice | 6.30.0-1.1 |
| libplasma | 6.7.5-1.1 |
| noto-fonts | 1:2026.10.01-1 |
| gtk3 | 1:3.24.52-1.1 |
| glib2 | 2.88.3-1.1 |
| systemd | 262-1 |
| tar | 1.35-5 |
| gzip | 1.15-1.1 |
| coreutils | 9.12-2.1 |
| bash | 5.3.20-2 |
| cachyos-lavender-kde-theme-git | r7.6279f76-1 |
| quickshell | 0.3.1.r10.g2d3b3e9-1 |
| kvantum | 1.1.8-1.1 |
| darkly | 0.5.39-2 |
| fuzzel | 1.15.0-1.1 |
| ripgrep | 15.2.0-1 |
| qt6-tools | 6.11.2-2.1 |
| gh | gh version 2.102.0 (2026-09-30) |
| Spotify | 1.2.96.518 (aplicación; spotify-launcher es el lanzador) |

## Herramientas de implementación e inspección

| Herramienta | Paquete y versión |
| --- | --- |
| qdbus6 | qt6-tools 6.11.2-2.1 |
| kwriteconfig6 | kconfig 6.30.0-1.1 |
| kreadconfig6 | kconfig 6.30.0-1.1 |
| plasma-apply-colorscheme | plasma-workspace 6.7.5-1.1 |
| plasma-apply-desktoptheme | plasma-workspace 6.7.5-1.1 |
| kbuildsycoca6 | kservice 6.30.0-1.1 |
| kscreen-doctor | libkscreen 6.7.5-1.1 |
| sddm-greeter-qt6 | sddm 0.21.0-8 |
| xdg-settings | xdg-utils 1.2.1-2 |
| xdg-mime | xdg-utils 1.2.1-2 |
| sed | sed 4.10-2.1 |
| awk | gawk 5.4.1-1.1 |
| timeout | coreutils 9.12-2.1 |
| sha256sum | coreutils 9.12-2.1 |
| systemctl | systemd 262-1 |
| pkg-config | pkgconf 3.0.7-1.1 |
| c++ | gcc 16.2.1+r23+gd564253eb6c8-1 |
| tar | tar 1.35-5 |
| gzip | gzip 1.15-1.1 |
| git | git 2.56.0-1.1 |
| curl | curl 8.22.0-1.1 |
| jq | jq 1.8.2-1.1 |
| python | python 3.14.7-2 |
| cmake | cmake 4.4.4-1.1 |
| make | make 4.4.1-3.1 |

GitHub CLI: `gh version 2.102.0 (2026-09-30)`. Codex CLI: `codex-cli 0.160.0`. Spotify aplicación: `1.2.96.518 (aplicación; spotify-launcher es el lanzador)`. GitHub CLI prepara la publicación; no se ha usado para publicar.

Los compiladores y CMake construyen Panel Colorizer y el conversor Qt de atajos. Python estándar gestiona instalación, snapshots, hashes y SVG; python-dbus registra atajos. qdbus6 llama a Plasma/KWin; las herramientas KDE escriben configuración y actualizan cachés. Bash orquesta la entrada y SDDM; curl obtiene el fondo opcional; Git descarga fuentes fijadas. rg, sed/awk, jq, tar/gzip, sha256sum, kscreen-doctor y systemctl se usaron para inspección, transformación o respaldo de la sesión original. GLib/GTK regeneran cachés de iconos. systemd aplica los overrides por proceso.

## Componentes de fuentes externas

| Componente | Versión / revisión | Fuente |
| --- | --- | --- |
| Panel Colorizer | 8.0.0; d0b1d4cab773f05cdcda2c1b2970093a5c367b54 | https://github.com/luisbocanegra/plasma-panel-colorizer |
| MacTahoe | sin release semántica; 839848b9a8a38a92a6936e30c4abe35cc6f2546d | https://github.com/vinceliuice/MacTahoe-icon-theme |
| Lavender (marco adaptado) | paquete r7.6279f76-1 | https://github.com/CachyOS/CachyOS-Lavender-KDE |
| Cf-Kde Aurorae / SDDM / SVG y scripts | 1.0.0 | este repositorio |

Darkly, Kvantum, Quickshell y Fuzzel pertenecían a la configuración anterior: se inspeccionaron, pero no son dependencias de Cf-Kde. Liquidglass widgets se inspeccionó y no se instaló; no se usa ni distribuye su contenido. ShellCheck no estaba disponible: se ejecutaron bash -n, compilación sintáctica Python y pruebas específicas.

## APIs y mantenimiento

[Scripting Plasma](https://develop.kde.org/docs/plasma/scripting/api/), [Aurorae](https://develop.kde.org/docs/plasma/aurorae/) y [temas SDDM](https://github.com/sddm/sddm/blob/develop/docs/THEMING.md). Se verificaron opciones con los binarios locales. Colorizer recomienda recompilar su plugin después de cambios incompatibles de Plasma; volver a ejecutar el instalador lo compila contra el destino.

Manifestación completa legible por máquina: [versions-reference.json](versions-reference.json). Fuentes que instala el script: [dependencies.lock.json](../dependencies.lock.json). Las librerías KDE/Qt usan la versión coherente del gestor de paquetes del destino, no las versiones del equipo original.
