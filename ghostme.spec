import os

block_cipher = None
base_dir = os.path.dirname(os.path.abspath(SPEC))

a = Analysis(
    [os.path.join(base_dir, 'ghostme', '__main__.py')],
    pathex=[base_dir],
    binaries=[],
    datas=[
        (os.path.join(base_dir, 'ghostme', 'templates'), 'ghostme/templates'),
        (os.path.join(base_dir, 'ghostme', 'static'), 'ghostme/static'),
    ],
    hiddenimports=[
        'pymobiledevice3',
        'pymobiledevice3.usbmux',
        'pymobiledevice3.lockdown',
        'pymobiledevice3.services.simulate_location',
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='GhostMe',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon=None,
)

if os.name == 'darwin':
    app = BUNDLE(
        exe,
        name='GhostMe.app',
        icon=None,
        bundle_identifier='com.ghostme.app',
        info_plist={
            'CFBundleName': 'GhostMe',
            'CFBundleDisplayName': 'GhostMe',
            'CFBundleVersion': '1.0.0',
            'CFBundleShortVersionString': '1.0.0',
        },
    )
