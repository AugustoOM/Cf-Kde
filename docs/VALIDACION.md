# Validación y alcance

Fecha: 2026-10-03. Equipo de referencia: CachyOS, Plasma 6.7.5, Qt 6.11.2, Wayland. Se distingue el escritorio Golden Gate aplicado durante la sesión de la distribución portable Cf-Kde preparada posteriormente.

## Escritorio de referencia

Verificados durante la implementación: backup íntegro y recuperable de la configuración anterior; geometrías de ambas pantallas sin modificar escala/frecuencia; dos docks nativos autohide y barras superiores; menú exportado por Dolphin y otra app Qt; perfiles Colorizer; estado de plugins KWin y ownership de notificaciones; KRunner por D-Bus; carga de SDDM en modo de prueba; SVG de decoración y tareas válidos.

Pedidos posteriores comprobados por configuración y revisión de la interfaz: icono CachyOS, reloj centrado en espaciadores nativos y fuente 14/700, formato largo con segundos, KRunner ampliado/redondeado, nueva decoración Aurorae, estados de tareas redondeados —incluida la corrección normal/hover/attention tras la observación de Spotify— e icono Dolphin oficial. El usuario confirmó que la posición y el atajo de KRunner eran correctos.

Las capturas/evidencias de esa sesión se conservan solo en el proyecto local anterior. No se incluyen ni se regeneraron capturas con datos personales para la publicación.

## Paquete portable Cf-Kde

- Se descargaron desde GitHub los dos commits fijados y se aplicó el parche limpio de Colorizer.
- Se compiló realmente el plugin Qt6/Plasma con CMake y se instaló únicamente en staging temporal. Plasmoide, plugin y preset correctos. CMake emitió avisos upstream sobre KDEInstallDirs, sin error de compilación.
- Se generaron los iconos Cf-Kde rojo/oscuro en staging y se sustituyó el icono Dolphin por el oficial del sistema. Los iconos no se activaron sobre el escritorio actual.
- Se compiló el conversor C++ de QKeySequence: Alt+Space=134217760, Alt+F2=150994993 y Search=16777362; coinciden con los códigos empleados por el instalador.
- Preview offscreen del SDDM renombrado Cf-Kde: carga sin errores QML; timeout esperado al mantener abierto el greeter de prueba. No se activó de nuevo SDDM.
- **8 pruebas automatizadas**: snapshot/restauración, corrupción de respaldo, rechazo de symlink externo, validación de rutas de manifiesto, conservación de elementos SVG y estados redondeados, paneles dinámicos/reloj, perfiles y simulación sin comandos. Una prueba recorre la instalación completa en HOME temporal con recursos de sistema ficticios y D-Bus/comandos simulados.
- bash -n para todos los scripts shell; compilación sintáctica de Python; parseo XML de todos los SVG y JSON de manifiestos/locks.
- Revisión automática de recursos publicables: solo texto, sin rutas HOME personales, tokens reconocibles, claves privadas, imágenes, archivos de backup o binarios. No sustituye una revisión humana de archivos nuevos que se añadan después.
- CI reproduce comprobaciones de texto y pruebas en Linux sin escritorio; no es un test gráfico de KDE.

El instalador nuevo **no se ejecutó sobre la sesión real** para cambiarla otra vez. Las pruebas de flujo con comandos simulados no demuestran una instalación completa en un segundo dispositivo; esta prueba queda pendiente. La compilación desde las fuentes fijadas sí se ejecutó realmente.

## Pruebas humanas al replicar

1. Confirmar barra/dock por pantalla, posición del reloj, tooltip y autohide sin zoom, incluidas ventanas maximizadas y fullscreen.
2. Abrir KRunner con Alt+Espacio, buscar, Enter/Escape, revisar AltGr y tamaño en HiDPI.
3. Revisar botones de minimizar/maximizar/restaurar/cerrar en Dolphin, Kitty, Firefox y Spotify; revisar opciones de decoración propia en aplicaciones que lo necesiten.
4. Cambiar los cuatro perfiles y confirmar contraste/blur sin artefactos con la GPU del nuevo equipo.
5. Revisar visualmente el login y probar autenticación solo al cerrar sesión voluntariamente; preview no autentica.
6. Revisar persistencia tras nuevo login y reconexión de pantallas. Pantallas agregadas después requieren volver a ejecutar el instalador o disponer sus paneles desde KDE.

No se certifican equipos ARM, GPUs distintas, todas las versiones de Plasma 6, escritorios ajenos o plataformas sin systemd. El script se adapta a rutas/pantallas y compila contra el destino, pero cada entorno requiere sus pruebas visuales.
