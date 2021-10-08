import sys
import platform
import winreg
import os, os.path
import pytest


fileDirectory = os.path.dirname(os.path.abspath(__file__)) 
sys.path.insert(0, os.path.dirname(fileDirectory))

def pytest_addoption(parser):
 home = homeFolder()
 parser.addoption("--component", action="store", help = "Regular expression of the components")
 parser.addoption("--wiring", action="store_true", default = False, help = "Check component wiring")

@pytest.helpers.register
def homeFolder() -> str: 
 if platform.system() == 'Windows':
  try:
   handle= winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders")
   return winreg.QueryValueEx(handle,'Personal')[0] 
  except:
   pass
 return os.path.expanduser('~')
 
