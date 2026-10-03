import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('cf',ROOT/'scripts/cf_kde.py')
cf=importlib.util.module_from_spec(spec);spec.loader.exec_module(cf)

class InstallerTests(unittest.TestCase):
    def test_backup_restore_and_integrity(self):
        with tempfile.TemporaryDirectory() as d:
            home=Path(d); config=home/'.config';config.mkdir(); state=home/'state'
            target=config/'kwinrc';target.write_text('original')
            absent=config/'new'
            with patch.multiple(cf,HOME=home,STATE=state), patch.object(cf,'allowed_paths',return_value=[target,absent]):
                dest,payload=cf.snapshot([target,absent]);target.write_text('new');absent.write_text('new')
                with patch.object(cf,'run') as run:
                    run.return_value.returncode=1
                    cf.restore(dest)
                self.assertEqual(target.read_text(),'original');self.assertFalse(absent.exists())
                (dest/'files/0').write_text('corrupt')
                with self.assertRaisesRegex(RuntimeError,'integridad'): cf.restore(dest,True)
    def test_external_symlink_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            home=Path(d); target=home/'linked';target.symlink_to('/tmp')
            with patch.multiple(cf,HOME=home,STATE=home/'state'):
                with self.assertRaisesRegex(RuntimeError,'enlazada'): cf.snapshot([target/'config'])
    def test_manifest_escape_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            dest=Path(d);(dest/'manifest.json').write_text(json.dumps({'schema':1,'home':str(cf.HOME),'files':[{'path':'/etc/passwd','slot':'0','before':'absent'}]}))
            with self.assertRaisesRegex(RuntimeError,'permitida'): cf.restore(dest,True)
    def test_svg_states_preserve_other_elements(self):
        xml='<svg xmlns="http://www.w3.org/2000/svg"><g id="progress-center"/><g id="focus-center"/></svg>'
        result=ET.fromstring(cf.build_tasks(xml,(ROOT/'assets/task-states.svg').read_bytes()))
        ids=[e.get('id') for e in result]
        self.assertEqual(ids.count('focus-center'),1);self.assertIn('progress-center',ids)
        for orientation in ('','north-','west-','east-'):
            for state in ('focus','normal','hover','attention'):
                self.assertIn(orientation+state+'-topleft',ids)
    def test_panels_dynamic_and_custom_clock(self):
        js=(ROOT/'assets/panels.js').read_text()
        self.assertIn('s<screenCount',js);self.assertIn('dd/MM',js)
        self.assertIn('fontWeight",700',js);self.assertIn('__LAUNCHERS__',js)
    def test_profile_settings(self):
        preset={'globalSettings':{'panel':{'normal':{'backgroundColor':{},'border':{'color':{}},'shadow':{'background':{'color':{}}},'radius':{}}},'nativePanel':{'background':{}},'widgets':{'normal':{}},'trayWidgets':{'normal':{}},'stockPanelSettings':{k:{} for k in ['lengthMode','thickness','visible']}}}
        with patch.object(cf,'qdbus') as bus,patch.object(cf,'config'):
            cf.profile('opaco',preset)
            script=bus.call_args_list[0].args[-1]
            self.assertIn('"blurBehind": false',script);self.assertIn('"alpha": 1',script)
        self.assertNotIn('alpha',preset['globalSettings']['panel']['normal']['backgroundColor'])
    def test_full_install_in_temporary_home(self):
        import argparse,subprocess,os
        with tempfile.TemporaryDirectory() as directory:
            home=Path(directory);data=home/'.local/share';config=home/'.config'
            system=home/'system-share';base=system/'plasma/desktoptheme/breeze-dark'
            base.mkdir(parents=True)
            (base/'metadata.json').write_text(json.dumps({'KPlugin':{'Name':'Breeze Dark','Version':'system'}}))
            (base/'colors').write_text('[Colors:Window]\nBackgroundNormal=20,20,20\n')
            (base/'plasmarc').write_text('[AdaptiveTransparency]\nenabled=true\n')
            tasks=system/'plasma/desktoptheme/default/widgets/tasks.svgz';tasks.parent.mkdir(parents=True)
            import gzip
            tasks.write_bytes(gzip.compress(b'<svg xmlns="http://www.w3.org/2000/svg"><g id="progress-center"/></svg>'))
            palette=system/'color-schemes/BreezeDark.colors';palette.parent.mkdir(parents=True)
            palette.write_text('[General]\nName=Breeze Dark\n')
            cache=home/'.cache';runtime=data/'cf-kde';state=home/'state'
            def prepare(stage):
                for rel in ['share/icons/Cf-Kde-red','share/icons/Cf-Kde-red-dark',
                    'share/plasma/plasmoids/luisbocanegra.panel.colorizer',
                    'lib/qt6/qml/org/kde/plasma/panelcolorizer']:
                    (stage/rel).mkdir(parents=True)
                return {'globalSettings':{}}
            def run(*args,**kwargs):
                output=''
                if args[:2]==('plasmashell','--version'): output='plasmashell 6.7.5'
                if 'is-enabled' in args: output='disabled'
                if 'is-active' in args: output='inactive'
                return subprocess.CompletedProcess(args,0,output,'')
            args=argparse.Namespace(dry_run=False,install_deps=False,sddm=False,
                background=None,migrate_caelestia=False,profile='equilibrado')
            import sys,types
            with patch.multiple(cf,HOME=home,CONFIG=config,DATA=data,CACHE=cache,RUNTIME=runtime,STATE=state,SYSTEM_SHARE=system), \
                 patch.dict(os.environ,{'XDG_SESSION_TYPE':'wayland','XDG_CURRENT_DESKTOP':'KDE'}), \
                 patch.dict(sys.modules,{'dbus':types.ModuleType('dbus')}), \
                 patch.object(cf.shutil,'which',return_value='/usr/bin/mock'), \
                 patch.object(cf,'prepare',side_effect=prepare),patch.object(cf,'run',side_effect=run), \
                 patch.object(cf,'profile'),patch.object(cf,'shortcuts'),patch.object(cf.os,'geteuid',return_value=1000):
                cf.install(args)
                self.assertTrue((data/'plasma/desktoptheme/Cf-Kde/widgets/tasks.svg').is_file())
                self.assertTrue((runtime/'krunner-data/krunnerstaterc').is_symlink())
                self.assertIn(str(home),(config/'systemd/user/plasma-krunner.service.d/cf-kde.conf').read_text())
                latest=Path((state/'latest').read_text().strip())
                cf.restore(latest,True)

    def test_dry_run_makes_no_calls(self):
        import argparse
        args=argparse.Namespace(dry_run=True,profile='equilibrado',sddm=True,migrate_caelestia=False)
        with patch.object(cf,'run',side_effect=AssertionError('No ejecutar comandos en dry-run')):
            cf.install(args)

if __name__=='__main__':unittest.main()
