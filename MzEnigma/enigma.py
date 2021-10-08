from typing import Optional, Callable, List, Tuple,  Dict

import MzEnigma

class Enigma: pass

class Enigma(object):
 """Represents an Enigma with all accessories
 
 :param model: model of the Enigma
  """
 def __init__(self, 
  model  : str = '', 
  umkehrwalzen : List[MzEnigma.Umkehrwalze] = list(), 
  walzen : List[MzEnigma.Walze] = list(), 
  numberOfWalzen : int = 0, 
  numberOfSteckers : int = 0, 
  zusatzwalzen : List[MzEnigma.Zusatzwalze] = list()) -> None:
  """
  Initialization
  """
  assert model, '{}: At least 1 character in model required'.format(self.__class__.__model__)
  self._model = model
  assert umkehrwalzen, '{}: At least 1 umkehrwalze required'.format(self.__class__.__model__)
  alphabet = umkehrwalzen[0].alphabet
  assert all(v.alphabet == alphabet for v in umkehrwalzen), '{}: Alphabets in all umkehrwalzen must match'.format(self.__class__.__model__)
  self._umkehrwalzen = umkehrwalzen
  assert walzen, '{}: At least 1 walze required'.format(self.__class__.__model__)
  assert all(v.alphabet == alphabet for v in walzen), '{}: Alphabets in all walzen must match'.format(self.__class__.__model__)
  self._walzen = walzen
  assert numberOfWalzen > 0 and numberOfWalzen <= len(walzen), '{}: 0 < numberOfWalzen < {}  required'.format(self.__class__.__model__, len(walzen))
  self._numberOfWalzen = numberOfWalzen
  assert numberOfSteckers >= 0, '{}: numberOfSteckers >= 0 required'.format(self.__class__.__model__)
  self._numberOfSteckers = numberOfSteckers
  if zusatzwalzen:
   assert all(v.alphabet == alphabet for v in zusatzwalzen), '{}: Alphabets in all zusatzwalzen must match'.format(self.__class__.__model__)
  self._zusatzwalzen = zusatzwalzen

 @property
 def alphabet(self) -> str:
  return self._umkehrwalzen[0].alphabet

 @property
 def model(self) -> str:
  return self._model

 @property
 def umkehrwalzen(self) -> List[MzEnigma.Umkehrwalze]:
  return self._umkehrwalzen

 @property
 def walzen(self) -> List[MzEnigma.Walze]:
  return self._walzen

 @property
 def numberOfWalzen(self) -> int:
  return self._numberOfWalzen

 @property
 def numberOfSteckers(self) -> int:
  return self._numberOfSteckers

 @property
 def zusatzwalzen(self) -> List[MzEnigma.Zusatzwalze]:
  return self._zusatzwalzen

 def __eq__(self, enigma : Enigma) -> bool:
  return self._model == enigma.model \
     and self._umkehrwalzen == enigma.umkehrwalzen \
     and self._walzen == enigma.walzen \
     and self._numberOfWalzen == enigma.numberOfWalzen \
     and self._numberOfSteckers == enigma.numberOfSteckers \
     and self._zusatzwalzen == enigma.zusatzwalzen 

 def __repr__(self) -> str:
  content = 'class: {}\nmodel: {}\nalphabet: {}\nUmkehrwalzen:'.format(self.__class__.__name__, self._model, self.alphabet)
  for walze in self._umkehrwalzen:
   for line in walze.__repr__().split('\n'):
    if 'class:' not in line and 'alphabet:' not in line:
     content += ' ' + line
  content += '\nnumber of Walzen: {}\nWalzen:'.format(self._numberOfWalzen)
  for walze in self._walzen:
   for line in walze.__repr__().split('\n'):
    if 'class:' not in line and 'alphabet:' not in line:
     content += ' ' + line
  if self._numberOfSteckers > 0:
   content += '\nnumber of Steckers: {}'.format(self._numberOfSteckers)
  if self._zusatzwalzen:
   content += '\nZusatzwalzen:'
   for walze in self._zusatzwalzen:
    for line in walze.__repr__().split('\n'):
     if 'class:' not in line and 'alphabet:' not in line:
      content += ' ' + line

class Tagesschluessel: pass

class Tagesschluessel(object):
 """Represents the Tagesschluessel of an Enigma
 
 :param model: model of the Enigma
  """
 def __init__(self,
  enigma : Optional[Enigma] = None,  
  umkehrwalze : Optional[MzEnigma.Umkehrwalze] = None, 
  walzen : List[MzEnigma.Walze] = list(),
  tagesWalzenStellungen : Optional[str] = None, 
  steckerbrett : Optional[MzEnigma.Steckerbrett] = None, 
  zusatzwalze : Optional[MzEnigma.Zusatzwalze] = None) -> None:
  assert enigma, '{}: Enigma required'.format(self.__class__.__model__)
  self.enigma =enigma
  alphabet = self.enigma.alphabet
  assert umkehrwalze, '{}: Umkehrwalze required'.format(self.__class__.__model__)
  assert umkehrwalze.alphabet == alphabet, '{}: Alphabet in umkehrwalze must match enigma'.format(self.__class__.__model__)
  self.umkehrwalze = umkehrwalze.copy()
  assert walzen, '{}: At least 1 walze required'.format(self.__class__.__model__)
  assert all(v.alphabet == alphabet for v in walzen), '{}: Alphabet in all walzen must match enigma'.format(self.__class__.__model__)
  self.walzen = walzen.copy()
  if tagesWalzenStellungen:
   assert len(tagesWalzenStellungen) == len(walzen), '{}: Walzenstellung, number of characters must match the number of walzen'.format(self.__class__.__model__)
   assert all(v in alphabet for v in tagesWalzenStellungen), '{}: Walzenstellung, all characters must be in alphabet'.format(self.__class__.__model__)
  else:
    tagesWalzenStellungen =  alphabet [0] * len(walzen)
  self.tagesWalzenStellungen =tagesWalzenStellungen
  self.spruchWalzenStellungen = None
  if steckerbrett:
   assert steckerbrett.alphabet == alphabet, '{}: Alphabet in steckerBrett must match enigma'.format(self.__class__.__model__)
  self.steckerbrett = steckerbrett.copy()
  if zusatzwalze:
   assert zusatzwalze.alphabet == alphabet, '{}: Alphabet in zusatzwalze must match enigma'.format(self.__class__.__model__)
  self.zusatzwalze = zusatzwalze.copy()

 def encode(self, spruch : str, spruchWalzenStellungen : Optional[str] = None) -> str:
  '''
   If the walzenStellungen is not None, the ...
  '''
  if spruchWalzenStellungen == self.walzenStellungen:
   spruchWalzenStellungen = None
  if spruchWalzenStellungen:
   assert len(spruchWalzenStellungen) == len(self.tagesWalzenStellungen), '{}: Walzenstellung, number of characters must match the number of walzen'.format(self.__class__.__model__)
   assert all(v in self.alphabet for v in spruchWalzenStellungen), '{}: Walzenstellung, all characters must be in alphabet'.format(self.__class__.__model__)
  for walze, ringstellung in zip(self.walzen, self.tagesWalzenStellungen):
   walze.ringstellung = ringstellung
  out = str()
  if spruchWalzenStellungen:
   for n in range(2):
    for c in self.tagesWalzenStellungen:
     out += self._encodeLetter(c)
   for walze, ringstellung in zip(self.walzen, spruchWalzenStellungen):
    walze.ringstellung = ringstellung
  for c in spruch:
   out += self._encodeLetter(c)
  return out
     
 def decode(self, spruch : str, useSpruchWalzenStellungen : bool = False) -> str:
  '''
   If the walzenStellungen is not None, the ...
  '''
  for walze, ringstellung in zip(self.walzen, self.tagesWalzenStellungen):
   walze.ringstellung = ringstellung
  if useSpruchWalzenStellungen:
   spruchWalzenStellungen = 2 * str()
   for n in range(2):
    for c in self.tagesWalzenStellungen:
     spruchWalzenStellungen[n] += self._encodeLetter(c)
   assert spruchWalzenStellungen[0] == spruchWalzenStellungen[1], '{}: Inconsistent Spruchschlüssel {}'.format(self.__class__.__model__, spruchWalzenStellungen)
   for walze, ringstellung in zip(self.walzen, spruchWalzenStellungen[0]):
    walze.ringstellung = ringstellung
  out = str()
  for c in spruch:
   out += self._encodeLetter(c)
  return out
     
 def _encodeLetter(self, c : str) -> str:
  """ Takes a letter as input, steps rotors accordingly, and returns letter output.
      Because Enigma is symmetrical, this works the same whether you encode or decode.
  """
  assert len(c) == 1, '{}.encodeLetter {}: len({}) != 1'.format(self.__class__.__name__, self.name, c)
  assert c in self.tagesschluessel.alphabet, '{}.encodeLetter: letter ({}) not in alphabet'.format(self.__class__.__name__, c)
  out = c
  self.tagesschluessel.enigma.walzen[0].step()
  if self.tagesschluessel.steckerbrett:
   out = self.tagesschluessel.steckerBrett.encodeForward(out)
  out = self.tagesschluessel.walzen[0].encodeForward(out)
  out = self.tagesschluessel.umkehrwalze.encodeForward(out)
  if self.tagesschluessel.zusatzwalze:
   out = self.tagesschluessel.umkehrwalze.encodeBackward(out)
  else:
   out = self.tagesschluessel.walzen[-1].encodeBackward(out)
  if self.tagesschluessel.steckerbrett:
   out = self.tagesschluessel.steckerBrett.encodeBackward(out)
  return out

 @property
 def alphabet(self) -> str:
  return self.enigma.alphabet

 def __eq__(self, tagesschluessel : Tagesschluessel) -> bool:
  return self.enigma == tagesschluessel.enigma \
     and self.umkehrwalze == tagesschluessel.umkehrwalze \
     and self.walzen == tagesschluessel.walzen \
     and self.steckerBrett == tagesschluessel.steckerBrett \
     and self.zusatzwalzen == tagesschluessel.zusatzwalzen  

 def __repr__(self) -> str:
  content = 'class: {}\nmodel: {}\nalphabet: {}\nUmkehrwalze'.format(self.__class__.__name__, self._model, self.alphabet)
  for line in self.umkehrwalze.__repr__().split('\n'):
   if 'class:' not in line and 'alphabet:' not in line:
    content += ' ' + line
  content += '\nWalzen:'
  for walze in self._walzen:
   for line in walze.__repr__().split('\n'):
    if 'class:' not in line and 'alphabet:' not in line:
     content += ' ' + line
  if self.steckerBrett:
   content += '\nSteckerbrett:'
   for line in self.steckerBrett.__repr__().split('\n'):
    if 'class:' not in line and 'alphabet:' not in line:
     content += ' ' + line
  if self.zusatzwalzen:
   content += '\nZusatzwalze:'
   for line in self.zusatzwalze.__repr__().split('\n'):
    if 'class:' not in line and 'alphabet:' not in line:
     content += ' ' + line

