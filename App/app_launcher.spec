# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['app_launcher.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('templates', 'templates'),
        ('static', 'static'),
        ('db.sqlite3', '.'),
        ('SICKGigEVisionTL.cti', '.'),
        ('media', 'media'),  # Add this if you have a media folder
    ],
    hiddenimports=[
        'cv2',
        'cv2.cv2',
        'scipy',
        'scipy.special',
        'scipy.special._ufuncs',
        'scipy.sparse',
        'django.core.management',
        'django.core.handlers.wsgi',
        'django.utils',
        'PIL',
        'Pillow',
        'harvesters',
        'orjson',
        # Add other modules you use
    ],
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
    name='app_launcher',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True
)
