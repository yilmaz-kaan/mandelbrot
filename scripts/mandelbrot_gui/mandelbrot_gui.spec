# mandelbot_gui.spec
from PyInstaller.utils.hooks import collect_dynamic_libs
import os

a = Analysis(
    ["main.py"],  # Your main script
    pathex=["."],
    binaries=[("mandelbrot.so", ".")],  # Include compiled C++ shared library
    datas=[],  # Include other data files if needed
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="MandelbotGUI",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
)

app = BUNDLE(
    exe,
    name="MandelbotGUI.app",
    icon=None,  # Add an .icns file if you want an icon
    bundle_identifier="com.yourname.mandelbot",
)
