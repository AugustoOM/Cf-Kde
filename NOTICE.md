# Atribuciones y recursos externos

Cf-Kde 1.0.0 (2026). Código y vectores propios GPL-3.0-only, salvo `assets/sddm/` bajo MIT; textos de licencia en LICENSE y licenses/MIT.txt. Los recursos de terceros conservan sus licencias originales.

- **Panel Colorizer**, Luis Bocanegra y colaboradores: [fuente](https://github.com/luisbocanegra/plasma-panel-colorizer), GPL-3.0, versión 8.0.0 y commit fijado en dependencies.lock.json. Se descarga y compila en destino; el parche GPL de Cf-Kde está en patches/colorizer-binding.patch.
- **MacTahoe icon theme**, vinceliuice y colaboradores: [fuente](https://github.com/vinceliuice/MacTahoe-icon-theme), GPL-3.0, commit fijado. Cf-Kde instala solamente rojo/oscuro y sustituye el alias de Dolphin por el icono oficial instalado. No contiene una copia del árbol de iconos.
- **Lavender-Dark-transparent**, Dharam Dhurandhar: [fuente CachyOS](https://github.com/CachyOS/CachyOS-Lavender-KDE), GPL-3.0. El marco decoration.svg y la configuración de Aurorae se adaptaron del paquete `cachyos-lavender-kde-theme-git r7.6279f76-1`. Fondos neutralizados y botones propios. La fuente modificada completa del tema está en assets/aurorae/.
- **Breeze Dark / KDE Visual Design Group**: [fuente Plasma Framework](https://invent.kde.org/plasma/libplasma), recursos obtenidos exclusivamente de los paquetes KDE instalados en el destino. El instalador copia metadata, colores y configuración localmente y transforma tasks.svg conservando sus elementos originales y añadiendo las esquinas propias de assets/task-states.svg. No se redistribuye el SVG original en este repositorio.
- **Dolphin / KDE**: icono oficial obtenido del paquete Dolphin del equipo destino; no se incluye en el repo.
- **Noto Sans / Google**: tipografía instalada por el gestor de paquetes, no se incluyen archivos de fuentes. [Fuente y licencia](https://github.com/notofonts/latin-greek-cyrillic).
- **Raycast**: [fondo externo](https://misc-assets.raycast.com/wallpapers/red_distortion_1_preview.png). No se declara libre ni se redistribuye; la instalación opcional lo obtiene de la fuente original. Para redistribuir un fondo dentro de un fork, usar una imagen propia o con licencia adecuada.

Las marcas de aplicaciones y distribuciones pertenecen a sus titulares. No se publican datos de la cuenta del creador, contraseñas, claves, historial, dotfiles privados ni capturas del escritorio original.
