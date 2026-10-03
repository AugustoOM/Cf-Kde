# Archivos afectados en la sesión original

Lista exacta registrada durante Golden Gate y sus ajustes posteriores. $HOME representa el usuario del equipo original y evita publicar su identidad. Los nombres históricos no son los nombres de instalación portable: Cf-Kde emplea recursos propios y no sobrescribe el tema local breeze-dark.

```text
$HOME/.config/autostart/caelestiashell.desktop
$HOME/.config/systemd/user/graphical-session.target.wants/kde-material-you-colors.service
$HOME/.config/systemd/user/timers.target.wants/caelestia-update-checker.timer
$HOME/.config/plasma-org.kde.plasma.desktop-appletsrc
$HOME/.config/plasmashellrc
$HOME/.config/plasmarc
$HOME/.config/kdeglobals
$HOME/.config/kwinrc
$HOME/.config/kglobalshortcutsrc
$HOME/.config/krunnerrc
$HOME/.config/dolphinrc
$HOME/.config/mimeapps.list
$HOME/.config/plasma-workspace/env/golden-gate-qml.sh
$HOME/.local/share/color-schemes/GoldenGate.colors
$HOME/.local/share/plasma/plasmoids/luisbocanegra.panel.colorizer
$HOME/.local/lib/qt6/qml/org/kde/plasma/panelcolorizer
$HOME/.local/share/icons/MacTahoe-red
$HOME/.local/share/icons/MacTahoe-red-dark
$HOME/.local/share/applications/golden-gate-suave.desktop
$HOME/.local/share/applications/golden-gate-equilibrado.desktop
$HOME/.local/share/applications/golden-gate-intenso.desktop
$HOME/.local/share/applications/golden-gate-opaco.desktop
/etc/sddm.conf.d/zz-golden-gate.conf
/usr/share/sddm/themes/golden-gate
/usr/share/backgrounds/custom/golden-gate-raycast.png
$HOME/.config/systemd/user/plasma-krunner.service.d/golden-gate.conf
$HOME/.local/share/golden-gate-krunner
$HOME/.local/share/aurorae/themes/GoldenGate-Windows
$HOME/.local/share/plasma/desktoptheme/breeze-dark
```

Se añadieron/editaron recursos de usuario y configuración; los links de habilitación se retiraron al desactivar los servicios. La carpeta de iconos tiene la sustitución final de org.kde.dolphin.svg en ambas variantes. El SVG widgets/tasks.svg contiene focus/normal/hover/attention redondeados. El overlay KRunner incorpora dialogs/background.svg y translucent/dialogs/background.svg y enlaza el historial normal. No se publican contenidos de configuraciones privadas ni respaldos.

Para las rutas del nuevo instalador, ejecutar `./install.sh --dry-run`. Valores, decisiones y estados de servicios: [MODIFICACIONES](MODIFICACIONES.md) y [REGISTRO_SESION](REGISTRO_SESION.md). El registro histórico menciona inventarios y capturas que solo existen en el proyecto local anterior.
