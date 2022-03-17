# from typing import Dict, Tuple, Any
import pytest

import re
import copy
import MzEnigma

def test_steckerbrett(pytestconfig):
 if pytestconfig.getoption('wiring'):
  for name, cls in vars(MzEnigma).items():
   if cls.__class__ == MzEnigma.Steckerbrett:
    print('\n -{}'.format(cls))
    
def test_ringstellung(pytestconfig):
 if pytestconfig.getoption('wiring'):
  print('\n--- test_ringstellung ---')
  for name, cls in vars(MzEnigma).items():
   if isinstance(cls, MzEnigma.Walze):
    encoded = str()
    for c in cls.alphabet:
     cls.ringstellung = c
     encoded += cls.encode(cls.alphabet[0], True)
    assert encoded == cls.wiring, 'Ringstellung of component {} failed'.format(cls.name)
    print('- {} completed'.format(cls.name))

def test_wiring(pytestconfig):
 if pytestconfig.getoption('wiring'):
  print('\n--- test_wiring ---')
  for name, cls in vars(MzEnigma).items():
   if isinstance(cls, MzEnigma.Steckerbrett):
    cls.notify = pytest.helpers.notify(pytestconfig)
    alphabet = cls.alphabet
    pos = 17
    if '_ringstellung' in vars(cls):
     cls.ringstellung = alphabet[pos]
    encoded = str()
    for c in alphabet:
     encoded += cls.encode(c, True, componentOnly = True)
    if '_ringstellung' in vars(cls):
     expectedWiring = cls.wiring[pos:] + cls.wiring[:pos]
    else:
     expectedWiring = cls.wiring
    assert encoded == expectedWiring, 'Reverse wiring of component {} failed, expected = {}, got = {}'.format(cls.name, encoded, expectedWiring)
    got = str()
    for n, c in enumerate(alphabet):
     got += cls.encode(encoded[n], False)
    assert alphabet == got, 'Reverse wiring of component {} failed, expected = {}, got = {}'.format(cls.name, encoded,  got)
    print('- {} completed'.format(cls.name))
 
def test_step(pytestconfig):
 if pytestconfig.getoption('wiring'):
  print('\n--- test_step ---')
  for name, cls1 in vars(MzEnigma).items():
   if isinstance(cls1, MzEnigma.Walze):
    cls1.ringstellung = cls1.alphabet[0]
    cls2 = copy.deepcopy(cls1)
    cls1.nextComponent = cls2
    ringstellung1 = cls1.alphabet.index(cls1.ringstellung)
    ringstellung2 = ringstellung1
    for c in cls1.alphabet:
     ringstellung1 = (ringstellung1 + 1) % len(cls1.alphabet)
     ringstellung2 += int(cls1.ringstellung in cls1.notches)
     cls1.step()
     assert cls1.alphabet[ringstellung1] == cls1.ringstellung and cls1.alphabet[ringstellung2] == cls2.ringstellung, 'Stepping of component {} failed'.format(cls1.name)
    print('- {} completed'.format(cls1.name))

if __name__ == "__main__":
 import sys
 pattern = 'I_.+'
 for name, cls in vars(MzEnigma).items():
  if isinstance(cls, MzEnigma.Umkehrwalze) and re.fullmatch(pattern, name):
   print('\n{}'.format(cls))
 pytest.main([__file__])  
 print(MzEnigma.I_A)

