# Respaldo y restauración

Cada instalación guarda un snapshot privado bajo XDG_STATE_HOME/cf-kde/backups (normalmente ~/.local/state/cf-kde/backups), con permisos 700. El manifiesto enumera archivos que existían y los que creó el instalador, huellas SHA-256 y estados de los servicios modificados. El snapshot se realiza después de preparar dependencias y antes de cambiar el escritorio. Las descargas y compilaciones en ~/.cache/cf-kde no son configuraciones y pueden eliminarse posteriormente.

Verificar sin cambiar nada:

```bash
./restore.sh /ruta/al/respaldo --dry-run
```

Cerrar la sesión KDE voluntariamente y entrar en una TTY (Ctrl+Alt+F3, por ejemplo). Restaurar como el mismo usuario, sin sudo:

```bash
cd ~/Cf-Kde
./restore.sh /ruta/al/respaldo
```

El restaurador valida las huellas antes de recuperar archivos y rechaza rutas ajenas al alcance de Cf-Kde. Si detecta plasmashell activo se detiene para evitar que vuelva a guardar los paneles nuevos encima de los antiguos. Conserva una copia de los archivos actuales en before-restore antes de reemplazarlos. Los archivos creados por Cf-Kde que antes no existían se retiran. Restaura enable/active de los servicios que desactivó la migración y recarga systemd. No desinstala paquetes compartidos.

El snapshot guarda archivos de configuración completos. Si hiciste cambios posteriores en esos mismos archivos, recuperarlos sustituye también esos ajustes por el estado del snapshot; puedes rescatarlo desde before-restore. Elegir el respaldo anterior a la instalación que se quiere revertir. Si solo se desea cambiar paneles/transparencia, usar las preferencias KDE o perfiles en vez de restaurar todo.

SDDM es independiente: ejecutar con sudo el restore.sh impreso por scripts/sddm.sh, guardado en /var/lib/cf-kde/backups/FECHA. Recupera únicamente las rutas del login y conserva su estado actual en before-restore. No reinicia display-manager. También recupera el archivo principal completo si existía, por lo que conviene hacerlo antes de nuevos cambios manuales al login.

Si la instalación falla, el script informa la ruta del respaldo. No hace rollback automático dentro de la sesión para evitar sobrescribir archivos mientras Plasma los usa. Los snapshots y sus manifiestos contienen información privada; no subirlos al repo. La copia completa histórica de Caelestia creada en el equipo original queda fuera de este proyecto público.
