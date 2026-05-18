# pac-man.spec
block_cipher = None

a = Analysis(
    ['pac-man.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('src/pacman/assets/', 'assets/'),
        ('config.json', '.'),
    ],
    hiddenimports=['pydantic', 'mazegenerator'],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='pac-man',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='pac-man',
)