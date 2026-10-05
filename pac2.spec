import os
import ctypes

mlx_path = ".venv/lib/python3.10/site-packages/mlx"
mazegen_path = ".venv/lib/python3.10/site-packages/mazegenerator"
binaries = [
    (os.path.join(mlx_path, "libmlx.so"), "mlx"),
]

datas = [
    (os.path.join(mlx_path, "__init__.py"), "mlx"),
    (os.path.join(mlx_path, "mlx.py"), "mlx"),
    (os.path.join(mazegen_path, "mazegenerator.py"), "mazegenerator"),
    (os.path.join(mazegen_path, "__init__.py"), "mazegenerator"),
    ("src/models/assets", "src/models/assets"),
    ("src/ui/menu", "src/ui/menu"),
    ("src/ui/points", "src/ui/points"),
    ("src/ui/power", "src/ui/power"),
    ("src/ui/window", "src/ui/window"),

]

a = Analysis(
    ['pac-man.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=[
		'ctypes',
		'PIL',
		'PIL.Image',
	],
    excludes=['mlx', 'mlx.mlx'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='PACMAN',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Pac-man42',
)
