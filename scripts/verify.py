#!/usr/bin/env python3
"""Comprobación de archivos publicables, sintaxis y recursos."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
root=Path(__file__).resolve().parents[1]
excluded={'.git','__pycache__','.cache','build','dist','backups'}
files=[p for p in root.rglob('*') if p.is_file() and not excluded.intersection(p.relative_to(root).parts)]
for path in files:
    if path.suffix in {'.png','.jpg','.zip','.gz','.so','.log'}: raise SystemExit('Archivo privado/binario inesperado: '+str(path))
    text=path.read_text()
    if re.search(r'/home/(?!USUARIO\b|usuario\b)[A-Za-z0-9_-]+',text): raise SystemExit('HOME personal: '+str(path))
    if ('-'*5+'BEGIN ' in text and 'PRIVATE'+' KEY-----' in text) or re.search(r'(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})',text): raise SystemExit('Secreto: '+str(path))
    if path.suffix=='.sh': subprocess.run(['bash','-n',str(path)],check=True)
    if path.suffix=='.py': compile(text,str(path),'exec')
    if path.suffix=='.svg': ET.fromstring(text)
    if path.suffix=='.json': json.loads(text)
print('Verificación correcta:',len(files),'archivos de texto; scripts y SVG válidos; sin HOME personal ni secretos reconocibles.')
