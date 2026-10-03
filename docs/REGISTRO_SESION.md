# Cambios aplicados

## Configuración y componentes

La lista exacta de rutas restaurables está en `changed-paths.txt`. Se desactivó el autostart de Caelestia (`Hidden=true` y `X-GNOME-Autostart-enabled=false`), se deshabilitaron/detuvieron `kde-material-you-colors.service` y `caelestia-update-checker.timer`. Sus estados previos eran enabled/active; el autostart estaba activo. No se modificaron los repositorios de Caelestia ni se quitaron paquetes.

Shell de Plasma: `org.kde.plasma.desktop`. Paneles nuevos: superiores 3 y 26; docks 23 y 46. En la comprobación final, pantalla Plasma 0 = DP-1, geometría (1920,0) 2560×1440; pantalla 1 = HDMI-A-2, geometría (0,0) 1920×1080. Los índices cambiaron respecto de la inspección inicial al recargar Plasma: no son identificadores permanentes de conector. Mapeo final comprobado por screenGeometry(), sin cambiar frecuencia ni escala. `panels.js` reutiliza paneles marcados GoldenGate en sucesivas ejecuciones.

Esquema GoldenGate basado en BreezeDark con acento rojo; estilo de widgets y decoración Breeze, botones IAX a la derecha. Tipografía Noto Sans. Iconos MacTahoe-red y MacTahoe-red-dark. Dolphin predeterminado para inode/directory; no se alteraron asociaciones de documentos. KRunner flotante con Alt+Space/Alt+F2; se recuperaron los atajos almacenados por Caelestia. Scripts KWin de Caelestia/tiling involucrados deshabilitados, sin detener KWin.

Panel Colorizer instalado como plasmoide local y plugin Qt6 compilado en usuario. Variables QML_IMPORT_PATH y QML2_IMPORT_PATH se añaden mediante `~/.config/plasma-workspace/env/golden-gate-qml.sh`. Correcciones locales: permisos de ejecución de las herramientas y normalización de configuración diferida con Qt.callLater para evitar un bucle de binding. Parche conservado en `colorizer-binding.patch`. Cuatro lanzadores `.desktop` para perfiles.

Se recargó únicamente plasmashell para cargar las correcciones. SwayNC obtuvo el nombre D-Bus de notificaciones durante una recarga: se detuvo y se bloqueó su activación solo temporalmente mientras arrancaba Plasma. El bloqueo temporal se retiró y swaync permanece disabled; Plasma posee ahora org.freedesktop.Notifications. No se desinstaló SwayNC ni se añadió un bloqueo persistente.

SDDM: tres archivos del tema local, fondo Raycast y override zz-golden-gate.conf. `theme.conf` anterior con Sugar Candy se conserva. `/etc/sddm.conf` contiene Autologin/Session y no Theme/Current; el override posterior gana dentro de conf.d. No se cambiaron ajustes ajenos. `instalar-login.sh` exige la huella del tema probado, instala con sudo y verifica la configuración efectiva. El usuario introdujo sudo en terminal y la instalación terminó con resultado 0.

Inventarios y evidencia locales: `paquetes-final.txt`, `kwin-final.txt`, `plasma-final.log`, `paneles-verificados.jsonl`, exportaciones de menús y capturas. No se añadieron ni actualizaron paquetes respecto del inventario previo. No se tocaron drivers, kernel, red, Bluetooth, distribución del teclado o configuración de monitores.

## Fuentes y licencias

- Panel Colorizer: https://github.com/luisbocanegra/plasma-panel-colorizer — commit d0b1d4cab773f05cdcda2c1b2970093a5c367b54, GPL-3.0 según LICENSE local. Fuentes en sources/plasma-panel-colorizer.
- MacTahoe icon theme: https://github.com/vinceliuice/MacTahoe-icon-theme — commit 839848b9a8a38a92a6936e30c4abe35cc6f2546d, GPL-3.0 según COPYING local. Se instaló únicamente la variante roja y su variante oscura.
- Breeze: componentes existentes de KDE; no se copiaron/alteraron archivos del paquete. Tema SDDM Golden Gate local: MIT (cabecera en Main.qml).
- API SDDM: https://github.com/sddm/sddm/blob/develop/docs/THEMING.md ; opciones de prueba confirmadas con sddm-greeter-qt6 --help de la versión local.
- API Plasma: https://develop.kde.org/docs/plasma/scripting/ ; API de KWin para prueba temporal de foco: https://develop.kde.org/docs/plasma/kwin/api/ . Script temporal descargado de KWin tras la prueba, sin plugin instalado.
- Raycast: https://misc-assets.raycast.com/wallpapers/red_distortion_1_preview.png — PNG validado, 1400×789. No se atribuye licencia libre a este fondo ni se publica en un repo.
- Liquid Glass widgets inspeccionados y conservados en sources/liquidglass-kde-widgets; no instalados por contener fuentes/iconos de Apple. No se instalaron clima, asistentes o widgets adicionales.

Versiones: plasma-workspace y kwin 6.7.5-1.1, Qt6 base 6.11.2-3.1, SDDM 0.21.0-8, Dolphin 26.08.1-1.1. CachyOS, Wayland; compositor OpenGL/EGL con RTX 3070 Ti.

## Ajustes solicitados después de la entrega

- Icono de los dos lanzadores: ruta explícita `/usr/share/icons/cachyos.svg`, evitando el icono Apple del tema MacTahoe.
- Reloj movido entre dos espaciadores nativos expansibles; bandeja a la derecha. Fuente Noto Sans, tamaño 14, fontWeight=700, Bold. Altura superior 38 para dar margen.
- KRunner: override del servicio con QT_SCALE_FACTOR=1.5 y XDG_DATA_DIRS con carpeta local prioritaria. La copia del tema Breeze Dark para este proceso contiene un SVG nine-slice con máscara redondeada y radio 16; paneles y otras aplicaciones siguen usando su tema habitual. Se reinició únicamente KRunner. FreeFloating y atajo intactos.
- Los dos nuevos elementos locales están registrados en changed-paths.txt para la restauración. Configuración previa de esta ronda guardada en ajustes-20261003/.

## Decoración Windows solicitada

Se reemplazó Breeze por Golden Gate Windows en el motor Aurorae ya instalado (KDecoration3, Plasma 6.7.5). Configuración KWin: library=org.kde.kwin.aurorae, theme=__aurorae__svg__GoldenGate-Windows; orden IAX y lado izquierdo vacío. Tema local y fuente reproducible en sources/GoldenGate-Windows, registrado en changed-paths.txt.

Marco adaptado del tema Lavender-Dark-transparent instalado, autor Dharam Dhurandhar, GPLv3: fondo neutral oscuro y texto claro sin sombra. Botones SVG originales de guion, cuadrado, cuadrados superpuestos y equis, GPLv3; zona de clic 36×28. Se conserva título de 28 px con márgenes y cierre con fondo rojizo solo en hover. Configuración anterior guardada en ajustes-decoracion/kwinrc-anterior. No se añadieron paquetes ni se reinició KWin; se aplicó por reconfigure.

## Resaltado redondeado del dock

Override local de Breeze Dark en ~/.local/share/plasma/desktoptheme/breeze-dark/: se conservan metadata, colores y plasmarc originales y se cambia únicamente widgets/tasks.svg. Los cuatro prefijos focus (cada orientación) tienen esquinas de 16 px y conservan el color de acento. Tras corregir la diferencia observada en Spotify, los estados normal, hover y atención también usan radio 16. Progreso y hints de espaciado permanecen del SVG original. Fuente y captura en ajustes-highlight/.

La carpeta del tema está registrada para restauración. Se ajustó el XDG_DATA_HOME de KRunner a su overlay previo para que siga usando su fondo redondeado propio; su krunnerstaterc enlaza al archivo habitual. Se recargó el estilo y reinició solo KRunner.

Icono de Dolphin: org.kde.dolphin.svg en ambas variantes MacTahoe y sus fuentes staged-icons reemplazado por el icono oficial del paquete Dolphin (/usr/share/icons/hicolor/scalable/apps/org.kde.dolphin.svg). Se conserva el resto del tema de iconos. Cachés regeneradas y cambio notificado a KDE; evidencia en ajustes-icono-dolphin/resultado.png.
