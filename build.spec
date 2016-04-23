# -*- mode: python -*-

block_cipher = None
mainAnalysis = Analysis(
	['main.py'],
	pathex=['C:\\Users\\f266s662\\code\\nasa-tlx'],
	binaries=None,
	datas=None,
	hiddenimports=[],
	hookspath=[],
	runtime_hooks=[],
	excludes=[],
	win_no_prefer_redirects=False,
	win_private_assemblies=False,
	cipher=block_cipher
)
configAnalysis = Analysis(
	['config.py'],
	pathex=['C:\\Users\\f266s662\\code\\nasa-tlx'],
	binaries=None,
	datas=None,
	hiddenimports=[],
	hookspath=[],
	runtime_hooks=[],
	excludes=[],
	win_no_prefer_redirects=False,
	win_private_assemblies=False,
	cipher=block_cipher
)

MERGE(
	(mainAnalysis, 'main', 'main'),
	(configAnalysis, 'config', 'config')
)

mainPYZ = PYZ(mainAnalysis.pure, mainAnalysis.zipped_data, cipher=block_cipher)
mainEXE = EXE(mainPYZ, mainAnalysis.scripts, exclude_binaries=True, name='main', debug=False, strip=False, upx=True, console=False)
mainCOLL = COLLECT(mainEXE, mainAnalysis.binaries, mainAnalysis.zipfiles, mainAnalysis.datas, strip=False, upx=True, name='main')

configPYZ = PYZ(configAnalysis.pure, configAnalysis.zipped_data, cipher=block_cipher)
configEXE = EXE(configPYZ, configAnalysis.scripts, exclude_binaries=True, name='config', debug=False, strip=False, upx=True, console=False)
configCOLL = COLLECT(configEXE, configAnalysis.binaries, configAnalysis.zipfiles, configAnalysis.datas, strip=False, upx=True, name='config')

import shutil
shutil.move('%s/config/config.exe' % DISTPATH, '%s/main/config.exe' % DISTPATH)
shutil.rmtree('%s/config' % DISTPATH)
