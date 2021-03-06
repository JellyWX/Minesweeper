import sys
import os
from urllib.request import urlopen

clean_install = True
binary_version = 0
binary_update = True
installer_version = 0
installer_update = True
asset_version = 0
asset_update = True

asset_list_existing = []
asset_list = []

def download(url,filename):
  r = urlopen(url)

  CHUNK = 16 * 1024
  with open(filename,'wb') as f:
    while True:
      chunk = r.read(CHUNK)
      if not chunk:
        break
      f.write(chunk)

if sys.platform == 'linux':
  print('Auto-detected Linux client.')
  plat = 0
else:
  print('Auto-detected Windows or Mac client.')
  plat = 1

print('Beginning directory formation...')
try:
  os.mkdir('assets')
  os.mkdir('assets/images')
  print('Created directory structure. Finding meta files...')
except FileExistsError:
  print('Directories already present. Finding meta files...')
  for f in os.listdir('assets/images'):
    ap = f.split('.')[0]
    asset_list_existing.append(ap)

try:
  with open('.meta','r') as f:
    version_list_old = f.read().split(';')
    binary_version = int(version_list_old[0])
    installer_version = int(version_list_old[1])
    asset_version = int(version_list_old[3])
  clean_install = False
except FileNotFoundError:
  print('No meta files found. This version is old or non-existant. Will perform full install')
  clean_install = True

print('Downloading meta files...')
download('https://raw.githubusercontent.com/JellyWX/Minesweeper/master/.meta','.meta')

with open('.meta','r') as f:
  version_list = f.read().split(';')
  if int(version_list[0]) == binary_version:
    binary_update = False
    print('Not queueing binary update...')
  if int(version_list[1]) == installer_version:
    installer_update = False
    print('Not queueing installer update...')
  if int(version_list[3]) == asset_version:
    asset_update = False
    print('Not queueing asset update...')
  asset_list = version_list[2].split(',')

for item in asset_list:
  if item in asset_list_existing and not asset_update:
    print('Not downloading ' + item + '.png as it already exists.')
  else:
    print('Downloading ' + item + '.png...')
    download('https://raw.githubusercontent.com/JellyWX/Minesweeper/master/assets/images/' + item + '.png','assets/images/' + item + '.png')

if clean_install or binary_update:
  if plat == 0:
    print('Downloading main...')
    download('https://raw.githubusercontent.com/JellyWX/Minesweeper/master/main','main')
  else:
    print('Downloading main.exe...')
    download('https://raw.githubusercontent.com/JellyWX/Minesweeper/master/main.exe','main.exe')

if clean_install or installer_update:
  if plat == 0:
    print('Downloading installer...')
    download('https://raw.githubusercontent.com/JellyWX/Minesweeper/master/installer','installer')
  else:
    print('Downloading installer.exe...')
    download('https://raw.githubusercontent.com/JellyWX/Minesweeper/master/installer.exe','installer.exe')
