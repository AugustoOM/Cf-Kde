# Instalación, adaptación y mantenimiento

## Requisitos

CachyOS/Arch con sesión KDE Plasma 6 Wayland activa, usuario normal, bus D-Bus de sesión y systemd de usuario. Qt6 y Plasma deben estar actualizados de manera coherente. Se requiere conexión a GitHub para las dependencias fijadas; Raycast solo si se pide SDDM sin fondo local. El equipo puede tener uno o varios monitores y cualquier GPU compatible con KDE.

`./install.sh --help` enumera las opciones. `--dry-run` enumera el plan y rutas sin compilar, descargar ni alterar archivos del escritorio; no certifica dependencias o renderizado. La compilación y preparación de fuentes ocurren antes del respaldo y de los cambios visuales.

Dependencias: base-devel, CMake, ECM, Git, Python y python-dbus, Qt6 base/declarative/svg/tools, libplasma, plasma-workspace, Breeze, Dolphin, Noto y utilidades xdg/GTK. `--install-deps` solo funciona en CachyOS/Arch y ejecuta sudo pacman -Syu --needed; no hacer actualizaciones parciales. El login también requiere SDDM Qt6, curl, timeout y rg; en CachyOS con SDDM suelen estar instalados. Si falta SDDM, instalar el paquete con el gestor de paquetes antes de pedir `--sddm`.

El script descarga commits exactos, aplica el parche incluido, compila y prepara en staging. Cambios finales: esquema, iconos, Aurorae, temas Plasma/KRunner, paneles y configuración Dolphin. Reinicia plasmashell y KRunner para cargar recursos; puede desaparecer la barra durante unos segundos. No reinicia KWin, SDDM ni el equipo. No cierra aplicaciones ni la sesión. La primera aplicación sustituye todos los paneles previos; el respaldo permite recuperarlos. Ejecuciones siguientes reutilizan los paneles marcados CfKde.

## Adaptación a otros dispositivos

- Pantallas: la API screenCount/screenGeometry de Plasma; no hay nombres DP/HDMI, resoluciones o IDs guardados.
- Favoritos: Dolphin, navegador predeterminado que tenga .desktop instalado, Kitty o Konsole y Preferencias. Aplicaciones no instaladas se omiten.
- Lanzador: recurso CachyOS del sistema; alternativa KDE si no existe. Sin descargar un logo de terceros.
- Icono Dolphin: SVG oficial del paquete instalado en el destino.
- Tema base: Breeze Dark y SVG del paquete KDE del destino. El script incorpora los estados redondeados y conserva progreso/márgenes originales.
- Plugin: compilado para las bibliotecas del destino, sin copiar el .so de la máquina original.
- Rutas: HOME y variables XDG. El plugin usa ~/.local/lib/qt6/qml por convención; se exporta la ruta a Plasma.
- Tamaños: píxeles lógicos; KRunner multiplica su escala por 1.5, por lo que HiDPI puede hacerlo visualmente mayor. No modifica escala global.
- Fecha: nombres de días/meses siguen el locale Qt/KDE del destino. Configurar español en Preferencias > Región e idioma para reproducir «sábado/octubre». No se cambia timezone ni locale del sistema automáticamente.

## Caelestia y atajos

`--migrate-caelestia` desactiva el autostart conocido y los automatismos KDE Material You Colors y Caelestia update checker cuando existen. Recupera atajos de stolen-shortcuts.json mediante Qt, desregistra acciones caelestia-shortcut y configura KRunner. Desactiva los scripts KWin conocidos de la migración, incluidos Polonium/Krohnkite; no usar la opción si se quieren mantener esos scripts.

No borra repositorios ni paquetes de Caelestia. No hace una copia completa de repositorios ajenos que no modifica: respalda cada ruta/configuración que sí cambia y estados de servicios. Migraciones desde una versión de Caelestia con unidades/rutas diferentes requieren revisar esos automatismos antes de instalar. El respaldo completo del equipo de referencia permanece fuera de Git.

Alt+Espacio corresponde a Alt en KDE; no distingue necesariamente el lado izquierdo. Un conflicto que KDE no pueda resolver se informa como error, con respaldo conservado. Revisar Preferencias > Atajos > KRunner. No se cambia XKB para capturar AltGr.

## SDDM

`--sddm` activa el login tras una prueba Qt6 offscreen, que revisa errores QML. Es una comprobación de carga, no prueba de autenticación ni validación visual del monitor físico. No modifica PAM, contraseña, autologin o backend vigente. La prueba real del login corresponde al próximo cierre de sesión voluntario.

La instalación con sudo guarda los archivos previos en /var/lib/cf-kde/backups y genera restore.sh. Un override define Current=cf-kde. Si /etc/sddm.conf ya contiene Theme/Current, cambia únicamente esa clave porque tiene precedencia. Verifica el valor efectivo antes de finalizar. No reemplaza Sugar Candy ni otros temas.

Por defecto descarga el PNG de Raycast; `--background /ruta/imagen.png` permite un recurso propio. El login no depende de acceso al HOME privado. El wallpaper del escritorio se conserva.

## Límites y actualizaciones

El menú global depende de que cada aplicación exporte su menú. Aurorae controla decoraciones del servidor; Firefox, Spotify/Electron y otras aplicaciones pueden dibujar sus propios botones o pedir no tener borde. Kitty puede ocultar la decoración con hide_window_decorations: revisar esa preferencia si faltan botones. El tema no fuerza ni edita preferencias privadas de cada aplicación.

Una barra por pantalla admite el reloj, pero la fecha larga puede desbordar en resoluciones pequeñas: reducir fontSize en la configuración del reloj. Las APIs usadas se comprobaron en Plasma 6.7.5; probar visualmente al instalar sobre otra versión. Cambios ABI de Plasma/Qt pueden requerir recompilar: repetir el instalador, que crea un nuevo respaldo. Revisar nuevas versiones upstream antes de editar dependencies.lock.json; el parche se aplica solamente si coincide el código esperado.
