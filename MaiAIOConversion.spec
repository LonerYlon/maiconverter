# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['maimai.py'],
    pathex=[],
    binaries=[],
    datas=[('crid', 'crid'), ('ffmpeg', 'ffmpeg'), ('flac', 'flac'), ('vgmstream-win64', 'vgmstream-win64'), ('maiforge', 'maiforge'), ('assetstudiocli', 'assetstudiocli')],
    hiddenimports=['converters.mp4', 'converters.mp3', 'converters.flac', 'converters.image', 'converters.database', 'tools.tools', 'tools.parser', 'winsound', 'msvcrt'],
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
    name='MaiAIOConversion',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
