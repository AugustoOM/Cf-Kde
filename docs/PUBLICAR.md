# Publicación pública en GitHub

El proyecto está preparado con Git en la rama main, archivos de texto publicables, documentación, licencias, fuentes modificadas, commits de dependencias fijados y CI. No contiene los repositorios externos, plugins compilados, capturas personales ni respaldos. No se ha creado automáticamente un repositorio remoto.

Configurar identidad local de Git y autenticar GitHub CLI. El correo noreply de la cuenta permite evitar publicar el correo personal:

```bash
cd ~/Cf-Kde
git config user.name "Tu nombre o alias"
git config user.email "TU_CORREO_NOREPLY_DE_GITHUB"
gh auth login
./scripts/publish.sh
```

El script ejecuta las pruebas y el control de archivos, crea el commit inicial con la identidad configurada y ejecuta `gh repo create Cf-Kde --public --source . --remote origin --push`. Ese paso publica todos los archivos versionados de este proyecto. Si Cf-Kde ya existe en la cuenta o hay un remoto configurado, revisar el remoto y publicar manualmente; no se elimina ni sobrescribe un repo existente.

Antes de añadir una captura al README, crear una sesión limpia sin documentos, cuentas, notificaciones o terminales personales. Revisar la imagen. Las imágenes están ignoradas por defecto y no se necesita una captura para instalar. El fondo Raycast no debe añadirse como recurso del repo sin derechos de redistribución acreditados.

Al publicar nuevas versiones, actualizar CHANGELOG, ejecutar pruebas, revisar licencias y validar sobre KDE. Un cambio de dependencies.lock.json requiere nueva compilación y comprobación del parche. CI valida código y recursos; no renderiza un escritorio KDE ni prueba login real.
