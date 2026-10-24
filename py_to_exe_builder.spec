# -*- mode: python ; coding: utf-8 -*-
# py_to_exe_builder.spec  v0.9.3 — PyInstaller: один файл, без консоли, без UPX.
# Сборка: build_exe.bat  (или: python -m PyInstaller --noconfirm --clean py_to_exe_builder.spec)

# Лишние модули Qt — не нужны сборщику, только раздувают EXE.
QT_EXCLUDES = [
    "PySide6.QtWebEngineCore", "PySide6.QtWebEngineWidgets", "PySide6.QtWebEngineQuick",
    "PySide6.QtWebChannel", "PySide6.QtWebSockets",
    "PySide6.Qt3DCore", "PySide6.Qt3DRender", "PySide6.Qt3DInput", "PySide6.Qt3DLogic",
    "PySide6.Qt3DExtras", "PySide6.Qt3DAnimation",
    "PySide6.QtMultimedia", "PySide6.QtMultimediaWidgets",
    "PySide6.QtQuick", "PySide6.QtQuickWidgets", "PySide6.QtQuickControls2", "PySide6.QtQuick3D",
    "PySide6.QtQml",
    "PySide6.QtCharts", "PySide6.QtDataVisualization",
]

a = Analysis(
    ["py_to_exe_builder.pyw"],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=["gh_update", "gh_update_qt", "gh_update_help"],  # 0.9.0: обновление с GitHub
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=QT_EXCLUDES + ["tkinter"],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="py_to_exe_builder",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
