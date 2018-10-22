# -*- mode: python -*-

block_cipher = None


a = Analysis(['plextray.py'],
             pathex=['/home/terje/Documents/Projects/PlexTray-debian/'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
a.datas += [('plex.png','/home/terje/Documents/Projects/PlexTray-debian/plex.png', "DATA"),
            ('dc.png','/home/terje/Documents/Projects/PlexTray-debian/dc.png', "DATA")]
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='PlexTray',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
