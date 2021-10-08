from typing import Dict, Tuple, Any
import pytest

import re
import MzEnigma

def test_print(pytestconfig):
 pattern = pytestconfig.getoption('component')
 if pattern:
  print('\n--- test_print: pattern = {} ---'.format(pattern))
  for name, cls in vars(MzEnigma).items():
   if isinstance(cls, MzEnigma.Umkehrwalze) and re.fullmatch(pattern, name):
    print('---\n{}'.format(cls))

def test_ringstellung(pytestconfig):
 if pytestconfig.getoption('wiring'):
  print('\n--- test_ringstellung ---')
  for name, cls in vars(MzEnigma).items():
   if isinstance(cls, MzEnigma.Zusatzwalze):
    encoded = str()
    for c in cls.alphabet:
     cls.ringstellung = c
     encoded += cls.encodeForward(cls.alphabet[0])
    assert encoded == cls.wiring, 'Ringstellung of component {} failed'.format(cls.name)
    print('- {} completed'.format(cls.name))

def test_wiring(pytestconfig):
 if pytestconfig.getoption('wiring'):
  print('\n--- test_wiring ---')
  for name, cls in vars(MzEnigma).items():
   if isinstance(cls, MzEnigma.Umkehrwalze):
    if '_ringstellung' in vars(cls):
     cls.ringstellung = cls.alphabet[0]
    encoded = str()
    for c in cls.alphabet:
     encoded += cls.encodeForward(c)
    assert encoded == cls.wiring, 'Wiring of component {} failed'.format(cls.name)
    if isinstance(cls, MzEnigma.Steckerbrett):
     encoded = str()
     for c in cls.alphabet:
      encoded += cls.encodeBackward(c)
     assert encoded == cls.rwiring, 'Reverse wiring of component {} failed'.format(cls.name)
    print('- {} completed'.format(cls.name))

def test_step(pytestconfig):
 if pytestconfig.getoption('wiring'):
  print('\n--- test_step ---')
  for name, cls1 in vars(MzEnigma).items():
   if isinstance(cls1, MzEnigma.Walze):
    cls1.ringstellung = cls1.alphabet[0]
    cls2 = cls1.copy()
    cls1.nextComponent = cls2
    ringstellung1 = cls1.ringstellung
    ringstellung2 = cls2.ringstellung
    for c in cls1.alphabet:
     if ringstellung1 in cls1.notches:
      offset1 = 2
      ringstellung2 = cls1.alphabet[(cls1.alphabet.index(ringstellung2) + 1) % cls1.numberOfPositions]
     else:
      offset1 = 2
     ringstellung1 = cls1.alphabet[(cls1.alphabet.index(ringstellung1) + offset1) % cls1.numberOfPositions]
     cls1.step()
     assert ringstellung1 == cls1.ringstellung and ringstellung2 == cls2.ringstellung, 'Stepping of component {} failed'.format(cls1.name)
    print('- {} completed'.format(cls.name))


if __name__ == "__main__":
 import sys
 pattern = 'I_.+'
 for name, cls in vars(MzEnigma).items():
  if isinstance(cls, MzEnigma.Umkehrwalze) and re.fullmatch(pattern, name):
   print('\n{}'.format(cls))
 pytest.main([__file__])  
 print(MzEnigma.I_A)

