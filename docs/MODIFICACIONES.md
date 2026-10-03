# Registro respecto del documento original

Referencia: [ESPECIFICACION_ORIGINAL](ESPECIFICACION_ORIGINAL.md), copia del documento de instrucciones original con el nombre histórico de usuario anonimizado. No era un tema instalable: Cf-Kde convierte las decisiones implementadas y los pedidos posteriores en recursos y scripts reproducibles. Fecha de consolidación: 2026-10-03.

| Elemento | Documento original | Resultado final y motivo |
| --- | --- | --- |
| Nombre | Golden Gate | Cf-Kde para publicación; nombres internos propios, sin sobrescribir Breeze Dark del paquete |
| Entorno | CachyOS, Plasma 6, Wayland | Se conserva; paneles nativos, sin Latte ni sustitución de KWin |
| Caelestia | Respaldar y desactivar interfaz | En el equipo original se verificó respaldo completo, se desactivaron autostart y automatismos de colores/actualizaciones; se conservaron repositorios y paquetes. En el instalador portable es opcional con `--migrate-caelestia` |
| Pantallas | Dos monitores, índices orientativos | Una barra y un dock por `screenCount`, sin índices de conectores ni cambio de escala/frecuencias |
| Dock | Flotante, centrado, contenido, autohide, iconos 44–48 | Panel de 64 px, `lengthMode=fit`, autohide, tareas solo del monitor actual, favoritos equivalentes y sin efecto de aumento |
| Barra | 30–36 px, fecha y bandeja a la derecha | 38 px; lanzador y menú global a la izquierda, reloj entre dos espaciadores nativos, bandeja a la derecha |
| Lanzador | Icono discreto, tema inspirado en macOS | Icono CachyOS explícito; reemplaza Apple. Si no existe el recurso CachyOS, usa el lanzador KDE |
| Reloj | `sáb 03/10/2026 · 17:12:37` | Pedido posterior: `03/10 -  sábado 03 de octubre - 18:32:12`. Noto Sans 14, peso 700, 24 h y segundos siempre visibles |
| KRunner | Spotlight, Alt izquierdo + Espacio | KRunner nativo, FreeFloating, Alt+Espacio/Alt+F2/Search, escala por proceso 1.5; SVG con radio lógico 16. Se conserva posición nativa y funcionalidades |
| Decoración | Botones Windows, Breeze permitido | Pedido posterior: Aurorae Cf-Kde-Windows con —, cuadrado/restaurar y ×; IAX a la derecha, título 28 y zonas 36×28, cierre rojo en hover |
| Resaltado de tareas | No especificaba un radio | Pedido posterior: esquinas de 16 px. Corrección adicional para Spotify: redondear focus, normal, hover y attention en las cuatro orientaciones; conservar progreso y hints nativos |
| Iconos | MacTahoe candidato, Dolphin inspirado en Finder | MacTahoe rojo/oscuro; pedido final reemplaza Finder por el SVG oficial de Dolphin, conservando otros iconos |
| Esquema | Oscuro, acento rojo | Base Breeze Dark, foco 190/73/91, hover 207/109/123, selección 153/57/74; Noto Sans 10 global |
| Vidrio | Tres intensidades y alternativa opaca | Panel Colorizer 8.0.0 compilado localmente, perfiles suave/equilibrado/intenso/opaco; transparencia y blur, sin afirmar refracción |
| Colorizer | Revisar compatibilidad | Parche de normalización diferida con `Qt.callLater` y guardia de valor previo; permisos ejecutables corregidos para herramientas del plasmoide |
| Dolphin | Conservar todas las funciones | Menú local disponible, rutas completas desactivadas, iconos 48, previews 96, detalles 24; asociación solo de carpetas |
| Menú global | Apps compatibles, no universal | Widget appmenu; aplicaciones con menús propios o decoración cliente pueden no exportarlos |
| Login | SDDM Qt6, composición centrada, Raycast | QML propio MIT, selección de usuario/sesión/teclado y apagado/reinicio según permisos. Preview antes de activar; no modifica PAM ni autologin |
| Fondo | Raycast solo login; conservar escritorio | Se mantiene la distinción. Fondo externo descargado al instalar, no redistribuido en Git |
| Notificaciones | No especificaba transición | En la sesión original SwayNC ganó D-Bus al recargar Plasma: bloqueo temporal retirado tras recuperar KDE. Instalador portable limita esa medida al servicio disabled/inactive |
| Servicios/tiling | Retirar automatismos anteriores | En la migración se desactivan los cuatro scripts involucrados: workspace tracker, bridge, Polonium y Krohnkite. Fuera de `--migrate-caelestia` se conservan |
| Recursos inspeccionados | Liquid Glass como candidato | No se instaló: contenía fuentes/iconos Apple. No se agregaron widgets de clima, IA, calendarios o asistentes |
| Hardware/sistema | No tocar controladores ni configuración ajena | Sin cambios deliberados a NVIDIA, kernel, red, Bluetooth, monitores o XKB. Instalar dependencias puede actualizar paquetes mediante pacman; documentado explícitamente |
| Publicación | Entrega local de scripts | Repo público preparado con GPL/MIT, fuentes fijadas, pruebas, CI, instalador y restauración; excluye binarios, datos privados y evidencia visual personal |

## Parámetros de perfiles

| Perfil | Opacidad del panel | Alfa del borde | Sombra | Blur KWin | Ruido KWin |
| --- | ---: | ---: | ---: | ---: | ---: |
| suave | 0.84 | 0.12 | 6 | 3 | 1 |
| equilibrado | 0.67 | 0.18 | 9 | 7 | 2 |
| intenso | 0.48 | 0.24 | 12 | 11 | 3 |
| opaco | 1.00 | 0.10 | 4 | 0 | 0 |

Tinte #211b20, borde de 1 px #e6c5cd, sombra negra alfa 0.24, radio de panel 12. Colorizer no reemplaza la política nativa de tamaño u ocultación del panel. El registro de la sesión conserva los nombres Golden Gate para distinguir el estado aplicado de la nueva distribución Cf-Kde.

## Rutas reproducidas

El instalador enumera todas las rutas afectadas con `./install.sh --dry-run`. Configuración: kdeglobals, kwinrc, plasmarc, plasmashellrc, plasma-org.kde.plasma.desktop-appletsrc, krunnerrc, kglobalshortcutsrc, dolphinrc y mimeapps.list bajo XDG_CONFIG_HOME. Recursos: esquema, tema Plasma, Aurorae, iconos, plasmoide, plugin QML, overlay KRunner, lanzadores de perfiles y overrides systemd propios. SDDM añade únicamente su carpeta de tema, fondo y override, más Theme/Current del archivo principal si ya existe esa clave.

La [lista exacta de rutas originales](ARCHIVOS_MODIFICADOS.md) también está conservada. Las modificaciones de la máquina original están descritas en [REGISTRO_SESION](REGISTRO_SESION.md). Sus respaldos y capturas quedan localmente en el proyecto anterior; no forman parte del repo público.
