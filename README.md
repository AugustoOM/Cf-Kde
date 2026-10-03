# Cf-Kde

Tema oscuro con acento rojo para **CachyOS, KDE Plasma 6 y Wayland**, nacido de la personalización Golden Gate y sus ajustes posteriores. Versión inicial: **1.0.0**.

Incluye barra superior y dock por monitor, reloj centrado y legible, paneles translúcidos regulables, KRunner ampliado con esquinas redondeadas, iconos rojos y decoración de ventanas con minimizar, maximizar/restaurar y cerrar a la derecha. Dolphin usa su icono oficial. El login SDDM es opcional.

El reloj muestra, con locale español: `03/10 -  sábado 03 de octubre - 18:32:12`. Es una fecha dinámica, con segundos reales. Barra de 38 píxeles lógicos; Noto Sans 14, negrita 700. Dock nativo de 64 píxeles, flotante, centrado, ajustado al contenido y con ocultación automática, sin magnificación.

## Instalación

Clonar este repositorio y ejecutar dentro de una sesión KDE Plasma Wayland como usuario normal:

```bash
./install.sh --dry-run
./install.sh --install-deps --sddm
```

`--install-deps` instala dependencias desde CachyOS/Arch mediante una actualización coherente `pacman -Syu --needed`, que puede actualizar otros paquetes. Si las dependencias ya están instaladas, omitirlo. `--sddm` descarga el fondo Raycast, prueba el greeter Qt6 e instala el login con sudo, sin cerrar sesión ni reiniciar SDDM. Para usar un PNG propio: `--sddm --background /ruta/fondo.png`.

En equipos que todavía ejecutan la interfaz Caelestia:

```bash
./install.sh --install-deps --sddm --migrate-caelestia
```

El instalador **reemplaza la disposición de paneles** la primera vez y guarda un respaldo privado antes de cambiarla. Al repetirlo reutiliza sus paneles. Detecta monitores mediante Plasma y favoritos según aplicaciones instaladas; no depende de conectores, GPU, resolución o nombre de usuario del equipo original. Conserva el fondo del escritorio. Compila el plugin de Panel Colorizer contra las bibliotecas del equipo de destino; no distribuye binarios de esta computadora.

Probado en CachyOS con Plasma **6.7.5**, Qt **6.11.2**, Wayland y dos monitores. El instalador exige Plasma 6.3 o posterior de la serie 6; eso es un requisito mínimo, no una certificación de todas esas versiones. Otros equipos y distribuciones necesitan las comprobaciones descritas en [VALIDACION](docs/VALIDACION.md). No es un instalador para Windows, GNOME o Plasma 5.

## Perfiles y recuperación

Hay lanzadores de aplicaciones para `suave`, `equilibrado`, `intenso` y `opaco`. También:

```bash
python ~/.local/share/cf-kde/cf_kde.py profile intenso
```

Los perfiles modifican tintes, opacidad, bordes, sombras y blur de KWin; no implementan refracción óptica. El blur de KWin es global. `opaco` lo desactiva.

El instalador muestra la ruta del respaldo. Para verificarlo o restaurarlo:

```bash
./restore.sh /ruta/al/respaldo --dry-run
# Después de cerrar la sesión gráfica, desde una TTY:
./restore.sh /ruta/al/respaldo
```

SDDM tiene un respaldo separado y un comando de restauración con sudo que se imprime al instalar. Consultar [RESTAURACION](docs/RESTAURACION.md).

## Documentación y publicación

- [Cambios respecto del archivo original](docs/MODIFICACIONES.md), [especificación original anonimizada](docs/ESPECIFICACION_ORIGINAL.md) y [registro detallado de la sesión](docs/REGISTRO_SESION.md).
- [Herramientas, versiones y fuentes](docs/HERRAMIENTAS_Y_VERSIONES.md); commits en [dependencies.lock.json](dependencies.lock.json).
- [Instalación y límites](docs/INSTALACION.md), [validación](docs/VALIDACION.md) y [publicación en GitHub](docs/PUBLICAR.md).

Para crear el repo público **Cf-Kde** cuando estés listo: `./scripts/publish.sh`. Este paquete preparado localmente no publica por sí solo.

## Créditos y licencia

Código propio y decoración derivados bajo GPL-3.0; login original bajo MIT. Panel Colorizer de Luis Bocanegra, iconos MacTahoe de vinceliuice y marco Aurorae derivado de Lavender de Dharam Dhurandhar/CachyOS. Breeze y Dolphin proceden de los paquetes KDE del destino. Atribuciones completas en [NOTICE](NOTICE.md).

El fondo de Raycast no se incluye en Git. Se descarga desde su fuente al solicitar el login o se proporciona un PNG propio. No se incluyen capturas de pantalla personales, dotfiles privados, respaldos, historial de KRunner, repositorios de Caelestia ni recursos extraídos de macOS. Cf-Kde no está afiliado a CachyOS, KDE, Apple, Microsoft o Raycast.
