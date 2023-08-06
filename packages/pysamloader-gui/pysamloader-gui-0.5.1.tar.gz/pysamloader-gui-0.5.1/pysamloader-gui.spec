# -*- mode: python -*-

import os
import platform
import PyInstaller.config

if platform.system() == 'Windows':
    from kivy.deps import sdl2, glew
    trees = (sdl2.dep_bins + glew.dep_bins)
    himports = ['win32timezone',]
else:
    trees = ()
    himports = []

# Configure paths
target = 'binary-{0}'.format(platform.system().lower())

workpath = os.path.join(os.getcwd(), 'build', target)
if not os.path.exists(workpath):
    os.makedirs(workpath)
PyInstaller.config.CONF['workpath'] = workpath

distpath = os.path.join(os.getcwd(), 'dist', target)
if not os.path.exists(distpath):
    os.makedirs(distpath)
PyInstaller.config.CONF['distpath'] = distpath

# Build
block_cipher = None


a = Analysis(
    ['rungui.py'],
    pathex=[os.path.split(SPECPATH)[0]],
    binaries=[],
    datas=[
        ('pysamloader_gui/assets', 'pysamloader_gui/assets'),
        ('pysamloader_gui/assets/connectors.png', 'pysamloader_gui/assets'),
        ('pysamloader_gui/assets/finish.png', 'pysamloader_gui/assets'),
        ('pysamloader_gui/assets/info.png', 'pysamloader_gui/assets'),
        ('pysamloader_gui/assets/logo-full.png', 'pysamloader_gui/assets'),
        ('pysamloader_gui/assets/sam-ic.png', 'pysamloader_gui/assets'),
        ('pysamloader_gui/assets/verify.png', 'pysamloader_gui/assets'),
        ('pysamloader_gui/assets/write.png', 'pysamloader_gui/assets'),
		('pysamloader_gui/assets/icon.png', 'pysamloader_gui/assets'),
		('pysamloader_gui/assets/icon.ico', 'pysamloader_gui/assets'),
    ],
    hiddenimports=himports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    *[Tree(p) for p in trees],
    name='pysamloader-gui',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    runtime_tmpdir=None,
    console=True,
	icon='pysamloader_gui/assets/icon.ico',
)
