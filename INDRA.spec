# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['UI\\main_window.py'],
    pathex=[],
    binaries=[],
    datas=[('runner.py', '.'), ('UI/themes', 'themes'), ('UI/settings.json', '.'), ('UI/app_icon.ico', '.')],
    hiddenimports=['runner', 'docx', 'docx.document', 'PyPDF2'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='INDRA',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='UI/app_icon.ico',
)
