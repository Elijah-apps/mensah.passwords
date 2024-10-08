# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files
from PyInstaller.building.build_main import Analysis, PYZ, EXE

# Analysis object setup
a = Analysis(
    ['main.py'],  # Entry point of your application
    pathex=['.'],  # Adjust this if needed
    binaries=[],
    datas=[
        ('resources/icon.ico', '.'),  # Include icon.ico in the root directory of the build
        ('resources/icon.png', '.'),  # Include icon.png in the root directory of the build
        ('passwords.db', '.'),  # Include passwords.db in the root directory of the build
        ('resources/profile_photo.jpg', '.'),  # Include profile_photo.jpg in the root directory of the build
    ],
    hiddenimports=[
        'password_manager',  # Include password_manager module
        'password_generator',  # Include password_generator module
        'database',  # Include database module
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

# Create the PYZ object
pyz = PYZ(a.pure, a.zipped_data)

# Create the EXE object
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='MensahPasswords',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to False for a windowed application
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    windowed=True,
    icon='resources/icon.ico',  # Path to your .ico file for the executable icon
)
