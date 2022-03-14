# from typing import Dict, Tuple, Any
import pytest

import copy
import random
import re
import MzEnigma

notify = [None, print]

def setWorstTagesWalzenStellungen(tagesschluessel : MzEnigma.Tagesschluessel) -> None:
 tagesWalzenStellungen = str()
 for walze in tagesschluessel.walzen:
  tagesWalzenStellungen += walze.notches[0]
 tagesschluessel.tagesWalzenStellungen = tagesWalzenStellungen

def test_print(pytestconfig):
 pattern = pytestconfig.getoption('component')
 if pattern:
  print('\n--- test_print: pattern = {} ---'.format(pattern))
  for name, cls in vars(MzEnigma).items():
   if (isinstance(cls, MzEnigma.Umkehrwalze) \
    or isinstance(cls, MzEnigma.Enigma) \
    or isinstance(cls, MzEnigma.Tagesschluessel)) \
    and re.fullmatch(pattern, name):
    print('\n -{}'.format(cls))

def test_basicencode(pytestconfig):
 print('\n--- test_basicencode ---')
 enigma = MzEnigma.Enigma(model = 'Enigma Test', walzen = [MzEnigma.I, MzEnigma.II], umkehrwalzen = [MzEnigma.UKW_B], numberOfWalzen = 2)
 msg = enigma.alphabet[:2]
 print(enigma)
 enigmaSetting = MzEnigma.Tagesschluessel(enigma, walzen = [MzEnigma.I, MzEnigma.II], tagesWalzenStellungen = 'AA', notify = pytest.helpers.notify(pytestconfig))
 # chainList = enigmaSetting.chain()
 eMsg = enigmaSetting.encode(msg)
 newMsg = enigmaSetting.decode(eMsg)
 assert msg == newMsg, 'Encoding of msg {} failed on enigma {}'.format(msg, enigma.model)

def test_chain(pytestconfig):
 msg = pytest.helpers.message(pytestconfig)
 pattern = pytestconfig.getoption('component')
 if pattern:
  print('\n--- test_chain ---\nmessage: {}'.format(msg))
  for name, enigma in vars(MzEnigma).items():
   if isinstance(enigma, MzEnigma.Enigma) and re.fullmatch(pattern, name):
    enigmaSetting = MzEnigma.Tagesschluessel(enigma, notify = pytest.helpers.notify(pytestconfig))
    enigmaSetting.chain()
    print('- {} completed'.format(name))

def test_encode(pytestconfig):
 msg = pytest.helpers.message(pytestconfig)
 pattern = pytestconfig.getoption('component')
 if pattern:
  print('\n--- test_encode ---\n')
  for name, enigma in vars(MzEnigma).items():
   if isinstance(enigma, MzEnigma.Enigma) and re.fullmatch(pattern, name):
    enigmaSetting = MzEnigma.Tagesschluessel(enigma, notify = pytest.helpers.notify(pytestconfig))
    setWorstTagesWalzenStellungen(enigmaSetting)
    print(enigmaSetting)
    if msg:
     actMsg = msg
    else:
     actMsg = enigma.alphabet
    eMsg = enigmaSetting.encode(actMsg)
    newMsg = enigmaSetting.decode(eMsg)
    assert actMsg == newMsg, 'Encoding of msg {} failed on enigma {}'.format(actMsg, enigma.model)
    print('- {} completed'.format(name))

def test_encode2(pytestconfig):
 msg = pytest.helpers.message(pytestconfig)
 pattern = pytestconfig.getoption('component')
 if pattern:
  print('\n--- test_encode2 (using Spruchschluessel) ---\n')
  for name, enigma in vars(MzEnigma).items():
   if isinstance(enigma, MzEnigma.Enigma) and re.fullmatch(pattern, name):
    enigmaSetting = MzEnigma.Tagesschluessel(enigma, notify = pytest.helpers.notify(pytestconfig))
    setWorstTagesWalzenStellungen(enigmaSetting)
    print(enigmaSetting)
    if msg:
     actMsg = msg
    else:
     actMsg = enigma.alphabet    
    eMsg = enigmaSetting.encode(actMsg, spruchWalzenStellungen = ''.join(random.sample(actMsg, enigma.numberOfWalzen)))
    newMsg = enigmaSetting.decode(eMsg, useSpruchWalzenStellungen = True)
    print('{} -> {} -> {}'.format(msg, eMsg,  newMsg))
    assert actMsg == newMsg, 'Encoding of msg {} failed on enigma {}'.format(actMsg, enigma.model)
    print('- {} completed'.format(name))

if __name__ == "__main__":
 pattern = '.+'
 for name, enigma in vars(MzEnigma).items():
  if isinstance(enigma, MzEnigma.Enigma) and re.fullmatch(pattern, name):
   enigmaSetting = MzEnigma.Tagesschluessel(enigma,  notify = None)
   spruchWalzenStellungen = ''.join(random.sample(enigma.alphabet, enigma.numberOfWalzen))
   twiceEncodedSpruchWalzenStellungen = enigmaSetting.encode(spruchWalzenStellungen + spruchWalzenStellungen)
   print('{}/{} -> {}: decoded = {}'.format(enigmaSetting.tagesWalzenStellungen, spruchWalzenStellungen + spruchWalzenStellungen, twiceEncodedSpruchWalzenStellungen, enigmaSetting.decode(twiceEncodedSpruchWalzenStellungen)))
   break

