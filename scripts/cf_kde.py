#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""Instalación reproducible de Cf-Kde; ejecutarse como usuario de la sesión KDE."""
import argparse
import copy
import datetime
import gzip
import hashlib
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tempfile
import time
import uuid
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
HOME = Path.home()
SYSTEM_SHARE = Path('/usr/share')
CONFIG = Path(os.environ.get('XDG_CONFIG_HOME', HOME / '.config'))
DATA = Path(os.environ.get('XDG_DATA_HOME', HOME / '.local/share'))
STATE = Path(os.environ.get('XDG_STATE_HOME', HOME / '.local/state')) / 'cf-kde'
CACHE = Path(os.environ.get('XDG_CACHE_HOME', HOME / '.cache')) / 'cf-kde'
RUNTIME = DATA / 'cf-kde'
PROFILES = {'suave': (.84,.12,6,3,1), 'equilibrado': (.67,.18,9,7,2),
            'intenso': (.48,.24,12,11,3), 'opaco': (1,.10,4,0,0)}
CONFIG_FILES = ['kde-mimeapps.list','kdeglobals','kwinrc','plasmarc','plasmashellrc',
                'plasma-org.kde.plasma.desktop-appletsrc','krunnerrc','kglobalshortcutsrc',
                'dolphinrc','mimeapps.list']
UNITS = ['kde-material-you-colors.service','caelestia-update-checker.timer']

def run(*args, capture=False, check=True, **kwargs):
    return subprocess.run([str(a) for a in args],check=check,text=True,
                          stdout=subprocess.PIPE if capture else None, **kwargs)

def qdbus(service, path, method, *args):
    return run('qdbus6', service, path, method, *args, capture=True).stdout.strip()

def config(file, group, key, value):
    run('kwriteconfig6','--file',file,'--group',group,'--key',key,str(value))

def allowed_paths(migrate=False):
    paths = [CONFIG / f for f in CONFIG_FILES]
    paths += [CONFIG/'plasma-workspace/env/cf-kde-qml.sh',
              CONFIG/'systemd/user/plasma-krunner.service.d/cf-kde.conf',
              CONFIG/'systemd/user/plasma-plasmashell.service.d/cf-kde.conf',
              DATA/'color-schemes/Cf-Kde.colors', DATA/'plasma/desktoptheme/Cf-Kde',
              DATA/'aurorae/themes/Cf-Kde-Windows', DATA/'icons/Cf-Kde-red',
              DATA/'icons/Cf-Kde-red-dark', DATA/'plasma/plasmoids/luisbocanegra.panel.colorizer',
              HOME/'.local/lib/qt6/qml/org/kde/plasma/panelcolorizer', RUNTIME]
    paths += [DATA/f'applications/cf-kde-{name}.desktop' for name in PROFILES]
    if migrate: paths.append(CONFIG/'autostart/caelestiashell.desktop')
    return paths

def exists(path):
    return path.exists() or path.is_symlink()

def remove(path):
    if path.is_symlink() or path.is_file(): path.unlink()
    elif path.exists(): shutil.rmtree(path)

def copy_path(src, dst):
    dst.parent.mkdir(parents=True,exist_ok=True)
    if src.is_symlink(): dst.symlink_to(os.readlink(src))
    elif src.is_dir(): shutil.copytree(src,dst,symlinks=True)
    else: shutil.copy2(src,dst)

def fingerprint(path):
    if path.is_symlink(): return 'link:'+os.readlink(path)
    if path.is_file(): return hashlib.sha256(path.read_bytes()).hexdigest()
    if path.is_dir():
        return hashlib.sha256(json.dumps([(p.relative_to(path).as_posix(),fingerprint(p))
              for p in sorted(path.iterdir())],ensure_ascii=True).encode()).hexdigest()
    return 'absent'

def snapshot(paths):
    dest=STATE/'backups'/(datetime.datetime.now().strftime('%Y%m%d-%H%M%S')+'-'+uuid.uuid4().hex[:8])
    dest.mkdir(parents=True,mode=0o700)
    records=[]
    for index,path in enumerate(paths):
        # Refuse external config symlinks: never silently overwrite their targets.
        for parent in [path,*path.parents]:
            if parent==HOME: break
            if parent.is_symlink(): raise RuntimeError(f'Ruta enlazada: {parent}; resolverla antes de instalar.')
        item={'path':str(path),'slot':str(index),'before':fingerprint(path)}
        if exists(path): copy_path(path,dest/'files'/str(index))
        records.append(item)
    payload={'schema':1,'home':str(HOME),'files':records,'services':{}}
    (dest/'manifest.json').write_text(json.dumps(payload,indent=2)+'\n')
    (STATE/'latest').write_text(str(dest)+'\n')
    return dest,payload

def save_manifest(dest,payload):
    (dest/'manifest.json').write_text(json.dumps(payload,indent=2)+'\n')

def restore(dest, dry_run=False):
    dest=Path(dest).expanduser().resolve()
    payload=json.loads((dest/'manifest.json').read_text())
    if payload.get('schema')!=1 or payload['home']!=str(HOME): raise RuntimeError('Respaldo de otro usuario o formato desconocido.')
    allowed={str(p) for p in allowed_paths(True)}
    for item in payload['files']:
        if item['path'] not in allowed or not item['slot'].isdigit(): raise RuntimeError('Ruta no permitida en respaldo.')
        src=dest/'files'/item['slot']
        if fingerprint(src)!=item['before']: raise RuntimeError('El respaldo no supera la comprobación de integridad: '+item['path'])
    if dry_run:
        print('Respaldo válido. Se restaurarían',len(payload['files']),'rutas y estados de servicios.'); return
    # Restoration from a TTY prevents Plasma overwriting the recovered layout.
    live=run('pgrep','-u',str(os.getuid()),'-x','plasmashell',capture=True,check=False)
    if live.returncode==0: raise RuntimeError('Cerrar la sesión gráfica y ejecutar restaurar desde una TTY.')
    recovery=dest/'before-restore'/uuid.uuid4().hex
    for item in payload['files']:
        path=Path(item['path']); src=dest/'files'/item['slot']
        for parent in path.parents:
            if parent==HOME: break
            if parent.is_symlink(): raise RuntimeError('Padre enlazado durante restauración: '+str(parent))
        if exists(path): copy_path(path,recovery/item['slot']); remove(path)
        if exists(src): copy_path(src,path)
    run('systemctl','--user','daemon-reload',check=False)
    for unit,previous in payload.get('services',{}).items():
        if unit not in UNITS: raise RuntimeError('Unidad desconocida en respaldo.')
        mode=previous['enabled']
        if mode in ('enabled','enabled-runtime'): run('systemctl','--user','enable',unit,check=False)
        elif mode=='disabled': run('systemctl','--user','disable',unit,check=False)
        if previous['active']=='active': run('systemctl','--user','start',unit,check=False)
    print('Restaurado. Los archivos anteriores a esta restauración están en',recovery)

def checkout(name, lock):
    # Every attempt uses a fresh tree; modified cache cannot contaminate the build.
    source=CACHE/'sources'/name
    remove(source); source.mkdir(parents=True)
    run('git','init','-q',source)
    run('git','-C',source,'remote','add','origin',lock['url'])
    run('git','-C',source,'fetch','--depth=1','origin',lock['commit'])
    run('git','-C',source,'checkout','--detach','FETCH_HEAD')
    got=run('git','-C',source,'rev-parse','HEAD',capture=True).stdout.strip()
    if got!=lock['commit']: raise RuntimeError('Commit de dependencia incorrecto.')
    return source

def prepare(stage):
    locks=json.loads((ROOT/'dependencies.lock.json').read_text())
    colorizer=checkout('colorizer',locks['colorizer'])
    run('git','-C',colorizer,'apply',ROOT/'patches/colorizer-binding.patch')
    build=stage/'build'
    run('cmake','-S',colorizer,'-B',build,'-DBUILD_PLUGIN=ON','-DINSTALL_PLASMOID=ON',
        '-DCMAKE_BUILD_TYPE=Release','-DCMAKE_INSTALL_RPATH=',f'-DCMAKE_INSTALL_PREFIX={stage}', '-DKDE_INSTALL_QMLDIR=lib/qt6/qml')
    run('cmake','--build',build,'--parallel',str(min(os.cpu_count() or 2,8)))
    run('cmake','--install',build)
    tools=stage/'share/plasma/plasmoids/luisbocanegra.panel.colorizer/contents/ui/tools'
    for path in tools.rglob('*'):
        if path.suffix in ('.sh','.py'): path.chmod(path.stat().st_mode|0o100)
    icons=checkout('icons',locks['icons'])
    (stage/'share/icons').mkdir(parents=True,exist_ok=True)
    run('bash',icons/'install.sh','-d',stage/'share/icons','-n','Cf-Kde','-t','red',cwd=icons)
    official=SYSTEM_SHARE/'icons/hicolor/scalable/apps/org.kde.dolphin.svg'
    if not official.is_file(): raise RuntimeError('Falta el icono oficial de Dolphin.')
    for name in ['Cf-Kde-red','Cf-Kde-red-dark']:
        icon=stage/'share/icons'/name/'apps/scalable/org.kde.dolphin.svg'
        remove(icon); shutil.copy2(official,icon)
    run('c++',ROOT/'assets/keycode.cpp','-o',stage/'keycode',*shlex.split(run('pkg-config','--cflags','--libs','Qt6Core','Qt6Gui',capture=True).stdout))
    for name in ['Cf-Kde-red','Cf-Kde-red-dark']:
        run('gtk-update-icon-cache','-f','-t',stage/'share/icons'/name)
    preset=json.loads((colorizer/'package/contents/ui/presets/Translucent/settings.json').read_text())
    return preset

def build_tasks(original, additions):
    ET.register_namespace('','http://www.w3.org/2000/svg')
    root=ET.fromstring(original)
    new=ET.fromstring(additions)
    ids={e.get('id') for e in new}
    for e in list(root):
        if e.get('id') in ids: root.remove(e)
    root.extend(list(new))
    return ET.tostring(root,encoding='unicode')

def desktop_theme(target):
    base=SYSTEM_SHARE/'plasma/desktoptheme/breeze-dark'
    target.mkdir(parents=True,exist_ok=True)
    for name in ['colors','plasmarc']: shutil.copy2(base/name,target/name)
    metadata=json.loads((base/'metadata.json').read_text())
    metadata['KPlugin']['Id']='Cf-Kde'; metadata['KPlugin']['Name']='Cf-Kde'; metadata['KPlugin']['Version']='1.0.0'
    for key in list(metadata['KPlugin']):
        if key.startswith('Name['): del metadata['KPlugin'][key]
    (target/'metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
    original=gzip.decompress((SYSTEM_SHARE/'plasma/desktoptheme/default/widgets/tasks.svgz').read_bytes())
    (target/'widgets').mkdir(exist_ok=True)
    (target/'widgets/tasks.svg').write_text(build_tasks(original,(ROOT/'assets/task-states.svg').read_bytes()))

def launchers():
    dirs=[DATA/'applications',Path('/usr/local/share/applications'),Path('/usr/share/applications')]
    def installed(name): return any((d/name).is_file() for d in dirs)
    browser=run('xdg-settings','get','default-web-browser',capture=True,check=False).stdout.strip()
    if not browser or not installed(browser): browser=next((x for x in ['firefox.desktop','chromium.desktop'] if installed(x)),None)
    terminal=next((x for x in ['kitty.desktop','org.kde.konsole.desktop'] if installed(x)),None)
    return ['applications:'+x for x in ['org.kde.dolphin.desktop',browser,terminal,'systemsettings.desktop'] if x and installed(x)]

def profile(name, preset=None):
    if preset is None: preset=json.loads((RUNTIME/'preset.json').read_text())
    s=copy.deepcopy(preset['globalSettings']); alpha,border,shadow,blur,noise=PROFILES[name]
    panel=s['panel']['normal']
    panel['backgroundColor'].update(alpha=alpha,sourceType=0,custom='#211b20')
    panel['border'].update(enabled=True,width=1)
    panel['border']['color'].update(alpha=border,sourceType=0,custom='#e6c5cd')
    panel['shadow']['background'].update(enabled=True,size=shadow)
    panel['shadow']['background']['color'].update(alpha=.24,sourceType=0,custom='#000000')
    panel['radius'].update(enabled=True,corner=dict.fromkeys(['topLeft','topRight','bottomRight','bottomLeft'],12))
    panel['blurBehind']=blur>0
    s['nativePanel']['background']['opacity']=0
    s['widgets']['normal']['enabled']=False; s['trayWidgets']['normal']['enabled']=False
    for key in ['lengthMode','thickness','visible']: s['stockPanelSettings'][key]['enabled']=False
    js="var settings="+json.dumps(s)+";panels().forEach(function(p){p.currentConfigGroup=['CfKde'];if(!p.readConfig('role',''))return;p.widgets().forEach(function(w){if(w.type==='luisbocanegra.panel.colorizer'){w.currentConfigGroup=['General'];w.writeConfig('globalSettings',JSON.stringify(settings));w.writeConfig('isEnabled',true);w.reloadConfig();}});});"
    qdbus('org.kde.plasmashell','/PlasmaShell','org.kde.PlasmaShell.evaluateScript',js)
    config('kwinrc','Plugins','blurEnabled',str(blur>0).lower())
    config('kwinrc','Effect-blur','BlurStrength',blur); config('kwinrc','Effect-blur','NoiseStrength',noise)
    qdbus('org.kde.KWin','/KWin','reconfigure')
    print('Perfil:',name)

def shortcuts(migrate=False, helper=None):
    import dbus
    bus=dbus.SessionBus()
    accel=dbus.Interface(bus.get_object('org.kde.kglobalaccel','/kglobalaccel'),'org.kde.KGlobalAccel')
    if migrate:
        cfg=CONFIG/'kglobalshortcutsrc'
        for line in cfg.read_text().splitlines() if cfg.exists() else []:
            if line.startswith('caelestia-shortcut-'):
                accel.unregister('caelestia-shell',line.split('=',1)[0])
        stolen=CONFIG/'caelestia/stolen-shortcuts.json'
        if stolen.is_file():
            for item in json.loads(stolen.read_text()):
                identity=dbus.Array([item['component'],item['action'],item['component'],item.get('actionFriendlyName',item['action'])],signature='s')
                codes=run(helper,*item['keys'],capture=True).stdout.splitlines()
                accel.setShortcut(identity,dbus.Array([int(x) for x in codes if int(x)],signature='i'),dbus.UInt32(4))
    identity=dbus.Array(['org.kde.krunner.desktop','_launch','KRunner','KRunner'],signature='s')
    # Qt::ALT | Qt::Key_Space, Qt::ALT | Qt::Key_F2, Qt::Key_Search.
    requested=dbus.Array([134217760,150994993,16777362],signature='i')
    actual=accel.setShortcut(identity,requested,dbus.UInt32(4))
    if 134217760 not in actual: raise RuntimeError('Alt+Espacio está en conflicto; resolverlo en Preferencias > Atajos y repetir.')

def install(args):
    if args.dry_run:
        print('Cf-Kde 1.0.0 — simulación: sin descargas, sudo ni cambios de escritorio.')
        print('Destino: KDE Plasma 6 Wayland; una barra y un dock por pantalla detectada por Plasma.')
        print('Compilar Colorizer; iconos rojos; Dolphin oficial; reloj centrado 14pt negrita; KRunner ×1.5; Aurorae IAX.')
        print('Perfil:',args.profile,'/ SDDM:',args.sddm,'/ migrar Caelestia:',args.migrate_caelestia)
        print('Rutas respaldadas:')
        for p in allowed_paths(args.migrate_caelestia): print(' ',p)
        return
    if os.geteuid()==0: raise RuntimeError('Ejecutar como usuario normal dentro de KDE, sin sudo.')
    if os.environ.get('XDG_SESSION_TYPE')!='wayland' or 'KDE' not in os.environ.get('XDG_CURRENT_DESKTOP',''):
        raise RuntimeError('Se requiere una sesión KDE Plasma 6 Wayland activa.')
    if args.install_deps:
        if not shutil.which('pacman'): raise RuntimeError('--install-deps requiere CachyOS/Arch.')
        run('sudo','pacman','-Syu','--needed','base-devel','cmake','extra-cmake-modules','git',
            'python','python-dbus','qt6-base','qt6-declarative','qt6-svg','qt6-tools','libplasma',
            'plasma-workspace','breeze','dolphin','konsole','noto-fonts','gtk3','curl',
            *(['sddm','ripgrep'] if args.sddm else []))
    required=['cmake','git','c++','pkg-config','gtk-update-icon-cache','qdbus6','kwriteconfig6','plasma-apply-colorscheme',
              'plasma-apply-desktoptheme','systemctl','xdg-settings','xdg-mime','kbuildsycoca6']
    if args.sddm: required+=['sddm-greeter-qt6','curl','timeout','rg']
    missing=[p for p in required if not shutil.which(p)]
    if missing: raise RuntimeError('Faltan herramientas: '+', '.join(missing)+'; usar --install-deps en CachyOS/Arch.')
    import dbus  # Fail before downloading if shortcut support is missing.
    version=run('plasmashell','--version',capture=True).stdout.strip()
    import re
    match=re.search(r'(\d+)\.(\d+)',version)
    if not match or int(match[1])!=6 or int(match[2])<3: raise RuntimeError('Se requiere Plasma 6.3 o posterior de la serie 6.')
    qdbus('org.kde.plasmashell','/PlasmaShell','org.kde.PlasmaShell.evaluateScript','print(screenCount);')
    CACHE.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='stage-',dir=CACHE) as stage_dir:
        stage=Path(stage_dir); preset=prepare(stage)
        dest,payload=snapshot(allowed_paths(args.migrate_caelestia))
        print('Respaldo:',dest,flush=True)
        try:
            replacements={stage/'share/icons/Cf-Kde-red':DATA/'icons/Cf-Kde-red',
                stage/'share/icons/Cf-Kde-red-dark':DATA/'icons/Cf-Kde-red-dark',
                stage/'share/plasma/plasmoids/luisbocanegra.panel.colorizer':DATA/'plasma/plasmoids/luisbocanegra.panel.colorizer',
                stage/'lib/qt6/qml/org/kde/plasma/panelcolorizer':HOME/'.local/lib/qt6/qml/org/kde/plasma/panelcolorizer',
                ROOT/'assets/aurorae':DATA/'aurorae/themes/Cf-Kde-Windows'}
            for src,target in replacements.items(): remove(target); copy_path(src,target)
            RUNTIME.mkdir(parents=True,exist_ok=True)
            shutil.copy2(__file__,RUNTIME/'cf_kde.py')
            (RUNTIME/'preset.json').write_text(json.dumps(preset))
            desktop_theme(DATA/'plasma/desktoptheme/Cf-Kde')
            overlay=RUNTIME/'krunner-data/plasma/desktoptheme/Cf-Kde'
            overlay.mkdir(parents=True,exist_ok=True)
            for name in ['metadata.json','plasmarc','colors']:
                shutil.copy2(DATA/'plasma/desktoptheme/Cf-Kde'/name,overlay/name)
            for folder in ['dialogs','translucent/dialogs']:
                (overlay/folder).mkdir(parents=True,exist_ok=True)
                shutil.copy2(ROOT/'assets/krunner/background.svg',overlay/folder/'background.svg')
            state=RUNTIME/'krunner-data/krunnerstaterc'
            remove(state); state.symlink_to(DATA/'krunnerstaterc')
            env=CONFIG/'plasma-workspace/env/cf-kde-qml.sh'; env.parent.mkdir(parents=True,exist_ok=True)
            env.write_text('#!/bin/sh\nexport QML_IMPORT_PATH="$HOME/.local/lib/qt6/qml${QML_IMPORT_PATH:+:$QML_IMPORT_PATH}"\nexport QML2_IMPORT_PATH="$HOME/.local/lib/qt6/qml${QML2_IMPORT_PATH:+:$QML2_IMPORT_PATH}"\n')
            env.chmod(0o755)
            def unit_env(unit, pairs):
                path=CONFIG/f'systemd/user/{unit}.service.d/cf-kde.conf'
                path.parent.mkdir(parents=True,exist_ok=True)
                path.write_text('[Service]\n'+''.join('Environment='+json.dumps(k+'='+v)+'\n' for k,v in pairs.items()))
            qml=str(HOME/'.local/lib/qt6/qml')
            qml+=':'+os.environ['QML_IMPORT_PATH'] if os.environ.get('QML_IMPORT_PATH') else ''
            unit_env('plasma-plasmashell',{'QML_IMPORT_PATH':qml,'QML2_IMPORT_PATH':qml})
            unit_env('plasma-krunner',{'QT_SCALE_FACTOR':'1.5','XDG_DATA_HOME':str(RUNTIME/'krunner-data'),
                'XDG_DATA_DIRS':str(DATA)+':'+os.environ.get('XDG_DATA_DIRS','/usr/local/share:/usr/share')})
            scheme=DATA/'color-schemes/Cf-Kde.colors'; scheme.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(SYSTEM_SHARE/'color-schemes/BreezeDark.colors',scheme)
            scheme.write_text('\n'.join(line for line in scheme.read_text().splitlines() if not line.startswith('Name['))+'\n')
            config(scheme,'General','Name','Cf-Kde'); config(scheme,'General','ColorScheme','Cf-Kde')
            for group in ['Colors:Button','Colors:Complementary','Colors:Header','Colors:View','Colors:Window']:
                config(scheme,group,'DecorationFocus','190,73,91'); config(scheme,group,'DecorationHover','207,109,123')
            config(scheme,'Colors:Selection','BackgroundNormal','153,57,74')
            run('plasma-apply-colorscheme','Cf-Kde'); run('plasma-apply-desktoptheme','Cf-Kde')
            for group,key,value in [('KDE','widgetStyle','Breeze'),('Icons','Theme','Cf-Kde-red-dark'),
                ('General','font','Noto Sans,10,-1,5,400,0,0,0,0,0')]: config('kdeglobals',group,key,value)
            for key,value in [('library','org.kde.kwin.aurorae'),('theme','__aurorae__svg__Cf-Kde-Windows'),
                ('ButtonsOnLeft',''),('ButtonsOnRight','IAX')]: config('kwinrc','org.kde.kdecoration2',key,value)
            config('krunnerrc','General','FreeFloating','true')
            for group,key,value in [('MainWindow','MenuBar','Enabled'),('General','ShowFullPath','false'),
                ('UiSettings','ColorScheme','Cf-Kde'),('IconsMode','IconSize',48),('IconsMode','PreviewSize',96),('DetailsMode','IconSize',24)]: config('dolphinrc',group,key,value)
            run('xdg-mime','default','org.kde.dolphin.desktop','inode/directory')
            if args.migrate_caelestia:
                for unit in UNITS:
                    prev={k:run('systemctl','--user',verb,unit,capture=True,check=False).stdout.strip()
                          for k,verb in [('enabled','is-enabled'),('active','is-active')]}
                    payload['services'][unit]=prev; save_manifest(dest,payload)
                    if prev['enabled'] not in ('not-found',''):
                        run('systemctl','--user','disable','--now',unit,check=False)
                for key,value in [('Hidden','true'),('X-GNOME-Autostart-enabled','false')]: config(CONFIG/'autostart/caelestiashell.desktop','Desktop Entry',key,value)
                run('systemctl','--user','stop','app-caelestiashell@autostart.service',check=False)
                for plugin in ['kwin_workspace_tracker','quickshell-kde-bridge','polonium','krohnkite']:
                    config('kwinrc','Plugins',plugin+'Enabled','false')
                    run('qdbus6','org.kde.KWin','/Scripting','org.kde.kwin.Scripting.unloadScript',plugin,check=False)
            config('plasmashellrc','Shell','ShellPackage','org.kde.plasma.desktop')
            qdbus('org.kde.plasmashell','/PlasmaShell','org.kde.PlasmaShell.changeShell','org.kde.plasma.desktop')
            run('systemctl','--user','daemon-reload')
            # Prevent the inactive SwayNC service from winning notification activation during reload.
            temporary_mask=False
            sway_mode=run('systemctl','--user','is-enabled','swaync.service',capture=True,check=False).stdout.strip()
            sway_active=run('systemctl','--user','is-active','swaync.service',capture=True,check=False).stdout.strip()
            if sway_mode=='disabled' and sway_active=='inactive':
                run('systemctl','--user','mask','--runtime','swaync.service'); temporary_mask=True
            try:
                run('systemctl','--user','restart','plasma-plasmashell.service')
                # DBus activation waits for Plasma's registration rather than a fixed sleep.
                js=(ROOT/'assets/panels.js').read_text()
                logo='/usr/share/icons/cachyos.svg' if Path('/usr/share/icons/cachyos.svg').exists() else 'start-here-kde'
                js=js.replace('__LAUNCHER_ICON__',json.dumps(logo)).replace('__LAUNCHERS__',json.dumps(launchers()))
                for attempt in range(30):
                    try:
                        qdbus('org.kde.plasmashell','/PlasmaShell','org.kde.PlasmaShell.evaluateScript','print(screenCount);')
                        break
                    except subprocess.CalledProcessError:
                        if attempt==29: raise
                        time.sleep(.25)
                qdbus('org.kde.plasmashell','/PlasmaShell','org.kde.PlasmaShell.evaluateScript',js)
                profile(args.profile,preset); shortcuts(args.migrate_caelestia,stage/'keycode')
            finally:
                if temporary_mask: run('systemctl','--user','unmask','--runtime','swaync.service',check=False)
            run('systemctl','--user','restart','plasma-krunner.service')
            for name in PROFILES:
                path=DATA/f'applications/cf-kde-{name}.desktop'; path.parent.mkdir(parents=True,exist_ok=True)
                exe=str(RUNTIME/'cf_kde.py').replace('\\','\\\\').replace('"','\\"').replace('`','\\`').replace('$','\\$').replace('%','%%')
                path.write_text(f'[Desktop Entry]\nType=Application\nName=Cf-Kde: {name}\nExec=python "{exe}" profile {name}\nIcon=preferences-desktop-theme\nCategories=Settings;DesktopSettings;\nTerminal=false\n')
            run('kbuildsycoca6','--noincremental')
            for item in payload['files']: item['after']=fingerprint(Path(item['path']))
            payload['reference_versions']=run('pacman','-Q','plasma-workspace','kwin','qt6-base',capture=True,check=False).stdout if shutil.which('pacman') else version
            save_manifest(dest,payload)
        except Exception:
            print('Instalación incompleta. Respaldo conservado:',dest,file=sys.stderr)
            raise
    if args.sddm:
        run('bash',ROOT/'scripts/sddm.sh',*([str(Path(args.background).expanduser().resolve())] if args.background else []))
    print('Cf-Kde instalado. No se cerró la sesión. Restaurar: ./restore.sh '+str(dest))

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='command',required=True)
    i=sub.add_parser('install'); i.add_argument('--dry-run',action='store_true')
    i.add_argument('--install-deps',action='store_true'); i.add_argument('--sddm',action='store_true')
    i.add_argument('--background'); i.add_argument('--migrate-caelestia',action='store_true')
    i.add_argument('--profile',choices=PROFILES,default='equilibrado')
    r=sub.add_parser('restore'); r.add_argument('backup'); r.add_argument('--dry-run',action='store_true')
    p=sub.add_parser('profile'); p.add_argument('name',choices=PROFILES)
    args=parser.parse_args()
    if args.command=='install' and args.background and not args.sddm: parser.error('--background requiere --sddm')
    try:
        if args.command=='install': install(args)
        elif args.command=='restore': restore(args.backup,args.dry_run)
        else: profile(args.name)
    except (RuntimeError,subprocess.CalledProcessError,OSError,ValueError) as error:
        print('ERROR:',error,file=sys.stderr); return 1
    return 0

if __name__=='__main__': sys.exit(main())
