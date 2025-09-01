# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['app_launcher.py'],   # your main script
    pathex=[],
    binaries=[],
    datas=[
        ('templates', 'templates'),   # include templates folder
        ('static', 'static'),         # include static folder
        ('db.sqlite3', '.'),          # include database file
        ('SICKGigEVisionTL.cti', '.'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='app_launcher',   # name of your exe
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True  # change to False if you don’t want console window
)