import sys
import platform
import winreg
import os, os.path
import pytest


fileDirectory = os.path.dirname(os.path.abspath(__file__)) 
sys.path.insert(0, os.path.dirname(fileDirectory))

def pytest_addoption(parser):
 home = homeFolder()
 parser.addoption("--notify", action="store_true", default = False, help = "Enable notify")
 parser.addoption("--component", action="store", help = "Regular expression of components or enigmas")
 parser.addoption("--wiring", action="store_true", default = False, help = "Check component wiring")
 parser.addoption("--message", action="store", help = "Message to be tested")

#"A calm and modest life brings more happiness than the pursuit of success combined with constant restlessness"

@pytest.helpers.register
def notify(pytestconfig): 
 return [None, print][pytestconfig.getoption('notify')]

@pytest.helpers.register
def message(pytestconfig): 
 rawMsg = pytestconfig.getoption('message')
 if rawMsg:
  msg = str()
  for c in rawMsg.upper():
   if c == ' ':
    c = 'X'
   msg += c
  print('message = {}'.format(msg))
 else:
  msg = None
  print('message = actual Alphabet')
 return msg

@pytest.helpers.register
def homeFolder() -> str: 
 if platform.system() == 'Windows':
  try:
   handle= winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders")
   return winreg.QueryValueEx(handle,'Personal')[0] 
  except:
   pass
 return os.path.expanduser('~')
 
