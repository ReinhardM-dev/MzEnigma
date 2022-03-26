import shutil
import sys
import os, os.path

# Try using setuptools first, if it's installed
from setuptools import setup
# from packaging import version

package = 'MzEnigma'
fileDirectory = os.path.dirname(os.path.abspath(__file__))
packageDirectory = os.path.join(fileDirectory, package)
sys.path.insert(0, fileDirectory)

with open(os.path.join(packageDirectory,'readme.rst'), 'r', encoding = 'utf-8') as f:
 long_description = f.read()
 
import MzEnigma
pkgVersion = MzEnigma.__version__

pythonVersion = sys.version_info[0] + 0.1 * sys.version_info[1]
if pythonVersion < 3.9:
 networkx = 'networkx>=2.2'
else:
 networkx = 'networkx>=2.5'

# Required to ensure a clean environment
shutil.rmtree(os.path.join(fileDirectory, 'build'), ignore_errors = True)

# Need to add all dependencies to setup as we go!
setup(name = package,
  url = 'https://github.com/ReinhardM-dev/MzEnigma', 
  project_urls={ 'Documentation': 'https://reinhardm-dev.github.io/MzEnigma' }, 
  version = pkgVersion,
  packages = [package],
  options={'bdist_wheel':{'universal':True}},
  package_data = {package: ['*.txt', '*.gpl3', '*.rst'] }, 
  description = 'A Simulator for Enigma operation and analysis',
  long_description = long_description, 
  long_description_content_type="text/x-rst",
  author  ='Reinhard Maerz',
  python_requires = '>=3.7', 
  install_requires = [ networkx ],
  setup_requires=['wheel'], 
  classifiers = [
    'Programming Language :: Python', 
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3 :: Only',
    'Development Status :: 4 - Beta', 
    'Natural Language :: English', 
    'Topic :: Security :: Cryptography'])

