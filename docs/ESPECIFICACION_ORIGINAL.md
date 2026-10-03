# CachyOS KDE — Golden Gate con Liquid Glass regulable

## Instrucción para Codex CLI

Trabajá directamente en mi computadora Linux para implementar este escritorio. Primero inspeccioná el sistema, creá y verificá una copia de seguridad restaurable de Caelestia y las configuraciones afectadas; después construí el nuevo entorno desde cero sobre KDE Plasma. No te limites a proponer comandos: ejecutá los cambios autorizados y verificá los resultados que puedas comprobar localmente. Respondé en español y explicá los avances brevemente.

Este documento autoriza respaldar, instalar componentes necesarios y configurar esta personalización. Solicitá intervención solamente cuando falten permisos, haya una decisión relevante sin resolver o sea necesaria una acción que cierre mi sesión. No reinicies, cierres sesión ni reinicies SDDM automáticamente. No ejecutes Codex como root: usá privilegios únicamente para operaciones concretas del sistema. Si sudo requiere contraseña, dejá que la introduzca en mi terminal, sin pedirla en el chat.

## 1. Resultado acordado

| Componente | Requisito |
| --- | --- |
| Apariencia | Inspiración macOS «Golden Gate», usando el Reddit como referencia visual. Vidrio, transparencias, bordes suaves y sombras moderadas; no hace falta una réplica exacta. |
| Liquid Glass | Intensidad regulable, con perfiles y acceso sencillo a sus ajustes. Priorizar lectura y estabilidad. |
| Base | CachyOS, KDE Plasma 6, Wayland; conservar KDE/KWin. |
| Caelestia | Copia de seguridad completa de sus componentes y ajustes; desactivar su interfaz y automatismos, crear paneles nuevos de Plasma. No borrar su respaldo ni desinstalar dependencias compartidas. |
| Dock | Uno abajo y centrado en cada monitor; flotante, ajustado al contenido, ocultación automática real. Sin aumento de tamaño de iconos al pasar el cursor. |
| Barra superior | Una por monitor, siempre visible, con menú de la aplicación activa, bandeja del sistema, hora con segundos y fecha. |
| Ventanas | Botones normales como Windows: minimizar, maximizar/restaurar, cerrar, de izquierda a derecha en el extremo superior derecho. Sin semáforos de colores. |
| Archivos | Dolphin predeterminado con apariencia inspirada en Finder, conservando sus funciones. |
| Buscador | Aspecto Spotlight, invocado con Alt izquierdo + Espacio. Elegir el componente compatible que mejor permita ese estilo. |
| Login | SDDM, composición centrada y sencilla con avatar/usuario, contraseña y fondo Raycast indicado más abajo. |
| Hardware | NVIDIA RTX 3070 Ti y dos monitores; detectar configuración vigente. |

Decisiones por defecto para evitar preguntas innecesarias: esquema oscuro con acento rojo discreto acorde al fondo, vidrio equilibrado, tipografía libre legible, dock con iconos de 44–48 píxeles lógicos y panel superior de aproximadamente 30–36 píxeles lógicos. Ajustar estas medidas a la escala real. Conservar el fondo de escritorio actual inicialmente; el fondo Raycast es obligatorio para el login, no fue solicitado como reemplazo del escritorio.

## 2. Contexto conocido, sujeto a inspección

- Usuario histórico: `USUARIO`. Resolver HOME y usuario reales en vez de fijar rutas a ciegas.
- Caelestia instalado anteriormente desde `~/caelestia-dots-kde`, con Darkly, Kvantum, Quickshell y Fuzzel. Puede haber versiones y rutas diferentes.
- Repositorio histórico: https://github.com/ladybug-me/caelestia-dots-kde ; actualmente redirige a https://github.com/ladybug-me/caelestia-kde . No actualizarlo como parte de esta migración.
- SDDM histórico con Sugar Candy en `/usr/share/sddm/themes/Sugar-Candy` y personalización `theme.conf.user`. Hubo un icono de usuario recortado; el nuevo login no debe reproducirlo.
- Bluetooth: conservar BlueZ y Bluedevil, la interfaz de KDE.
- KRunner tenía Alt+Espacio desactivado para dejarlo a Fuzzel; el cambio a Fuzzel podía estar pendiente. Auditar ambos antes de registrar el nuevo atajo.
- Monitores históricos: HDMI-A-1 1920×1080 a 120 Hz, DP-3 2560×1440 a ~165 Hz principal. Son datos orientativos de Hyprland, NO instrucciones para reconfigurar KWin.
- No tocar drivers NVIDIA, kernel, red, Bluetooth, monitores, distribución de teclado ni las herramientas de desarrollo por este trabajo.

## 3. Inspección y respaldo obligatorio

Antes de cambiar archivos, crear `~/kde-golden-gate/` para scripts, fuentes locales y documentación, y un respaldo independiente con fecha bajo `~/Backups/kde-pre-golden-gate/`. Proteger el respaldo contra lectura por otros usuarios. No versionar datos privados en un repositorio público.

Inspeccionar versión de Plasma, Qt, KWin, SDDM, sesión actual, paquetes relevantes, efectos habilitados, autostarts, servicios de usuario, enlaces simbólicos y scripts de Caelestia. Usar `rg` para búsquedas delimitadas. Comandos de diagnóstico orientativos:

```bash
plasmashell --version
kwin_wayland --version
pacman -Q
pacman -Qqe
pacman -Qqm
kscreen-doctor -o
systemctl --user list-unit-files
systemctl --user --failed
systemctl status display-manager.service --no-pager
```

Si un comando no existe, usar una alternativa instalada. No instalar utilidades solamente para ejecutar este listado.

Respaldar, cuando existan:

- `~/.config/plasma-org.kde.plasma.desktop-appletsrc`, `plasmashellrc`, `kdeglobals`, `kwinrc`, reglas de ventanas, `kglobalshortcutsrc`, configuración de KRunner, `dolphinrc`, `konsolerc` y preferencias GTK relacionadas.
- Configuración de Caelestia, Quickshell, Fuzzel, Kvantum, Darkly, autostart y unidades/overrides de systemd de usuario involucrados.
- Repositorio local de Caelestia completo, incluidos cambios sin commit, submódulos y archivos no rastreados relevantes; registrar commit y estado de git.
- Temas, plasmoides, efectos, decoraciones y scripts personalizados en `~/.local/share/` afectados; destinos de enlaces simbólicos que estén fuera del árbol respaldado.
- `/etc/sddm.conf`, `/etc/sddm.conf.d/`, overrides del servicio si existen, y tema Sugar Candy completo, respetando propiedad y permisos originales.
- Inventario de paquetes, estado previo de servicios habilitados/enmascarados, shortcuts, mapas de pantallas y lista de archivos que no existían antes del trabajo.

Identificar el alcance real en los scripts instalados; no asumir que Caelestia vive únicamente en su repositorio. Registrar archivos administrados por paquetes y cómo restaurarlos si fueran afectados. No hacer un borrado masivo de `~/.config` o `~/.local/share`.

Verificar la copia: listar contenido, comparar hashes de los archivos esenciales y comprobar que contiene los destinos de symlinks y las unidades que deberán recuperarse. Crear `RESTAURAR.md` y un script de restauración antes de desactivar Caelestia. El script debe validar el respaldo y restaurar solo los elementos de esta migración, sin eliminar cambios ajenos. Debe funcionar desde una TTY sin depender del escritorio nuevo.

## 4. Estrategia de implementación

### Retirar la interfaz de Caelestia de forma reversible

Identificar y desactivar solamente sus entradas de autostart, servicios, barras y procesos concretos. No usar `killall quickshell` ni quitar todos los servicios Qt. Revisar si scripts dinámicos de colores, wallpaper o tiling podrían volver a sobrescribir los ajustes. Desactivar los que pertenezcan al escritorio anterior y guardar su estado para la restauración. Conservar paquetes compartidos necesarios para KDE y otros programas.

Crear una disposición nueva de paneles. Usar APIs de scripting de Plasma verificadas para la versión instalada, con scripts idempotentes que no dupliquen paneles al repetirse. No inventar identificadores de plasmoides ni valores de configuración. Si una operación exige editar el archivo de paneles, coordinar la escritura con plasmashell para que no la sobrescriba y preparar su recuperación antes. No detener KWin en Wayland.

### Dock en ambos monitores

Preferir paneles nativos de Plasma y un gestor de tareas por iconos. Evaluar FancyTasksNG únicamente si su versión es compatible y aporta estética sin comprometer el comportamiento. No basar la solución en una versión antigua de Latte Dock.

- Panel inferior centrado en cada salida vigente, tamaño al contenido, flotante y con ocultación automática al retirar el cursor, incluso cuando ninguna ventana lo cubre.
- Iconos fijos y equivalentes en ambos docks: Dolphin, navegador predeterminado, terminal habitual y Preferencias del sistema. Añadir otras apps frecuentes solamente si el inventario lo justifica. Resolver los `.desktop` reales.
- Como decisión por defecto, mostrar ventanas del monitor correspondiente y mantener los mismos favoritos. Registrar esta elección como ajustable.
- Desactivar magnificación, zoom y cualquier animación que aumente iconos en hover. Puede haber indicación sutil de foco o tooltip.
- Comprobar bordes de activación, ventanas maximizadas, pantalla completa y persistencia tras reconectar monitores. Asociar paneles usando el mapeo de Plasma actual; no asumir que número de pantalla y conector coinciden.

### Barra superior y menú global

En ambos monitores: lanzador discreto a la izquierda, nombre de app activa si es compatible, menú global funcional, espacio flexible, bandeja y fecha/hora a la derecha. Usar widgets nativos cuando alcancen el diseño.

Formato objetivo: `sáb 03/10/2026 · 17:12:37`, con fecha local del sistema y segundos siempre visibles. No cambiar la zona horaria para lograrlo; respetar el locale español disponible. Verificar el formato admitido por el reloj instalado.

Probar el menú con Dolphin y al menos otra app Qt que exporte menús. Mantener acceso al menú local cuando la aplicación no exporte menú global. Firefox, Electron, GTK y apps con decoración propia pueden tener comportamientos distintos: documentar lo observado, sin prometer compatibilidad universal ni ocultar menús que dejen funciones inaccesibles.

### Vidrio regulable

Evaluar Panel Colorizer y componentes Liquid Glass compatibles con Plasma 6. Leer README, licencia, dependencias y scripts antes de instalar. El proyecto de widgets ofrece shaders y parámetros, pero no aplica vidrio automáticamente a todas las superficies del escritorio.

Implementar tres perfiles seleccionables: `suave`, `equilibrado` (inicial) y `intenso`. Permitir ajustar al menos opacidad/tinte, desenfoque donde lo soporte el componente y bordes/sombras. Añadir refracción solo en superficies que realmente la implementen. No presentar transparencia con blur como si fuese refracción Liquid Glass real.

Entregar controles accesibles: módulos existentes y sus rutas exactas, más un pequeño script o lanzadores para los perfiles cuando puedan cambiarse de manera fiable. Preferir ajustes propios del usuario sobre parches a archivos de paquetes. Registrar las claves reales y qué superficie afecta cada parámetro. Si algún efecto no admite ajuste dinámico, explicarlo y aplicar los perfiles solo a parámetros compatibles.

No instalar widgets de clima, asistentes IA, mirroring o calendarios adicionales por aparecer en las referencias. Si el efecto requiere código local, limitarlo a componentes necesarios, conservar fuente y utilizar APIs Qt6 soportadas. Probar shaders con NVIDIA y priorizar ausencia de artefactos. No desactivar el compositor para sortear errores. Conservar una opción de paneles opacos funcionales.

### Ventanas y aplicaciones

Elegir decoración Plasma 6 compatible, con geometría sobria, esquinas moderadas y botones normales a la derecha. Breeze es una base válida si otras decoraciones imponen semáforos. El cierre debe quedar al extremo derecho y el botón central alternar maximizar/restaurar. Verificar ventanas maximizadas y decoraciones cliente; documentar excepciones de apps que controlan sus propios botones.

Usar un tema de iconos libre inspirado en macOS, evaluando MacTahoe como candidato. No imponer fuentes propietarias ni recursos extraídos de macOS. Un tema global no debe sobrescribir paneles o botones sin revisión. Evitar combinar múltiples efectos que hagan lo mismo o parches invasivos de KWin.

En Dolphin: barra lateral de Lugares, navegación limpia, barra de herramientas compacta, iconos coherentes, vistas por iconos y detalles, previsualizaciones razonables, carpetas y archivos fáciles de distinguir. Mantener búsqueda, montajes, papelera y archivos ocultos accesibles. No sustituir Dolphin por Nautilus. No cambiar asociaciones de documentos; cambiar gestor de archivos predeterminado solo si hace falta.

### Buscador estilo Spotlight

Evaluar primero KRunner por integración y capacidades; preferirlo si el tema permite un popup sobrio y centrado sin parches frágiles. Si otro lanzador mantenido mejora claramente la apariencia y conserva las funciones necesarias, usarlo y documentar la decisión. Requisitos: búsqueda rápida de apps, apertura con Enter, cierre con Escape y buen contraste.

Configurar `Alt+Space` comprobando conflictos con KRunner, Fuzzel, Caelestia y menú de ventana de KWin. Probar físicamente Alt izquierdo + Espacio; no confundirlo con Meta/Super. Los shortcuts de KDE pueden registrar Alt sin distinguir lados: si Alt derecho es AltGr, comprobar que conserva sus caracteres. Si ambos Alt activan el atajo, documentarlo; no modificar globalmente XKB ni romper AltGr para exigir exclusividad del izquierdo, que el usuario no pidió. No asumir que basta editar un archivo sin recargar el componente pertinente.

### Login SDDM centrado

Mantener SDDM y su backend vigente salvo incompatibilidad demostrada. Seleccionar/adaptar un tema Qt6 compatible; si se crea uno local, usar la API oficial de SDDM y los componentes de autenticación existentes. No alterar PAM, contraseñas, autologin ni sesiones instaladas.

Fondo solicitado:

```text
https://www.raycast.com/_next/image?url=https%3A%2F%2Fmisc-assets.raycast.com%2Fwallpapers%2Fred_distortion_1_preview.png&w=1920&q=70
```

Archivo fuente candidato equivalente:

```text
https://misc-assets.raycast.com/wallpapers/red_distortion_1_preview.png
```

Descargar con URL correctamente entrecomillada. Validar HTTP, tipo de archivo y dimensiones: nunca guardar HTML como PNG. El acceso a esa imagen no pudo verificarse al preparar este documento. Si ambas URLs fallan, completar los demás cambios y pedir únicamente una copia del fondo para terminar el login; no sustituirlo silenciosamente.

Guardar el fondo en `/usr/share/backgrounds/custom/` y el tema local en `/usr/share/sddm/themes/golden-gate/`, con archivos legibles por el greeter y sin depender de HOME cifrado o privado. No sobreescribir Sugar Candy ni archivos de temas gestionados por paquetes.

Composición: fondo a pantalla completa, recorte proporcional, sombreado suave para contraste, avatar disponible o icono neutro, nombre y contraseña centrados. Controles discretos para sesión, teclado y apagar/reiniciar. Sin tarjeta enorme, relojes gigantes ni campos recortados. Conservar selección de Plasma Wayland y acceso a otras sesiones existentes.

Probar con el binario greeter y modo de prueba disponibles; confirmar las opciones con `--help`. Revisar errores QML y dependencias de importación Qt6. El modo de prueba valida apariencia, no autentica ni demuestra que un login real funcionará. No activar un tema que no renderice. Registrar precedencia de la configuración SDDM y usar un override específico sin pisar ajustes ajenos. No reiniciar `display-manager.service`; reservar prueba real para el siguiente cierre de sesión voluntario.

## 5. Instalación y verificaciones

Usar repositorios CachyOS/Arch primero; verificar nombres de paquetes disponibles. Si hace falta AUR, revisar PKGBUILD y fuentes y compilar como usuario normal. No ejecutar instaladores remotos con `curl | sh`, ni aplicar dotfiles de terceros en bloque. No hacer `pacman -Sy` seguido de instalaciones que causen una actualización parcial; evaluar una actualización coherente si es imprescindible y comunicar su alcance.

No prometer equivalencia perfecta con las referencias: son composiciones de temas, extensiones y personalizaciones. Anotar URLs, versiones/commits y licencias de lo realmente instalado. Mantener scripts de aplicación idempotentes y un registro de cambios. Validar scripts de shell creados con comprobación sintáctica y ShellCheck si está disponible.

Lista de aceptación:

- [ ] Respaldo íntegro de Caelestia y restauración preparada antes de modificar.
- [ ] Caelestia no genera barras, atajos duplicados ni recoloreados automáticos conflictivos.
- [ ] Dos docks que se ocultan automáticamente, sin magnificación y en los monitores correctos.
- [ ] Dos barras superiores con fecha, segundos y menú de apps compatibles.
- [ ] Botones minimizar, maximizar/restaurar y cerrar a la derecha, con símbolos normales.
- [ ] Dolphin conserva funciones y presenta un diseño coherente inspirado en Finder.
- [ ] Buscador aparece con Alt izquierdo + Espacio, sin conflictos ni ruptura de AltGr.
- [ ] Perfiles de vidrio funcionan y están documentados; no hay falsas afirmaciones sobre refracción.
- [ ] Tema SDDM renderiza, usa el fondo solicitado y conserva controles esenciales.
- [ ] No hay nuevos errores relevantes de Plasma/KWin, ni artefactos obvios con NVIDIA.
- [ ] Paneles y ajustes se guardan para próximas sesiones; la persistencia real se comprueba tras un reinicio/cierre de sesión voluntario.

Marcar por separado lo verificado por configuración, lo verificado visualmente y lo pendiente de prueba humana. Si no hay herramienta para ver el escritorio, no inventar capturas ni dar por comprobados hover, segundos o shaders. Reducir los pendientes a pruebas concretas y breves, continuando con el resto del trabajo posible.

## 6. Entrega local

Dejar en `~/kde-golden-gate/`:

1. `README.md`: componentes elegidos, uso cotidiano, ajustes de vidrio y atajos.
2. Scripts de aplicación/perfiles necesarios, con rutas y modos de uso exactos.
3. `CAMBIOS.md`: archivos tocados, paquetes agregados y estados de servicios cambiados.
4. `RESTAURAR.md` y script de restauración: respaldo exacto, recuperación desde TTY y reversión del override SDDM. Verificar que el nuevo tema puede desactivarse incluso sin login gráfico. No quitar paquetes compartidos al revertir.
5. `VALIDACION.md`: pruebas hechas, resultados y pendientes reales.

El resultado debe quedar aplicado hasta donde permita la sesión, no solamente diseñado. No cerrar sesión sin mi autorización; si queda una prueba que la requiere, dejarla preparada y explicar el siguiente paso.

## 7. Referencias

- Inspiración principal: https://www.reddit.com/r/unixporn/comments/1uc6g8e/kde_accurate_macos_clone_in_kde_with_actual_macos/
- Inspiración adicional: https://www.youtube.com/watch?v=l9mnvLqxPjo — el video no pudo consultarse al preparar este documento; no asumir componentes específicos por su URL.
- Widgets y shaders configurables: https://github.com/jaxparrow07/liquidglass-kde-widgets
- Panel Colorizer: https://github.com/luisbocanegra/plasma-panel-colorizer
- Iconos candidatos: https://github.com/vinceliuice/MacTahoe-icon-theme
- Scripting de Plasma: https://develop.kde.org/docs/plasma/scripting/
- API de temas SDDM: https://github.com/sddm/sddm/blob/develop/docs/THEMING.md

Estas son fuentes para evaluar, no instrucciones para instalar todo. Comprobar compatibilidad en mi máquina antes de elegir cada componente.
