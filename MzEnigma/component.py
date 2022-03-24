from typing import TypeVar,  Union, Optional, Callable, Dict,  List,  Tuple
import random
import copy

stdAlphabet : str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
sgsAlphabet : str = 'ABCDEFGHIJKLMNOPQRSTUVXYZÅÄÖ'

class Umkehrwalze: pass
class Steckerbrett: pass
class Zusatzwalze: pass
class Walze: pass
Component = TypeVar('Component', Umkehrwalze, Steckerbrett, Zusatzwalze, Walze)

class Umkehrwalze(object):
 """Represents an Umkehrwalze (UKW == reflector)

.. csv-table:: Wheel Controls
   :header: "Item", "Value"
   :widths: 30, 30
   
   *encryption*, forward only 
   *ring*, none
   *notches*, none 

:param name: name of the Umkehrwalze
:param wiring: wiring of the Umkehrwalze, positions related to the *alphabet*
:param alphabet: unencoded alphabet to be used
:param notify: notification function (e.g. print)
 """
 def __init__(self, 
  name  : str = '', 
  wiring : Union[str, Dict[str, str]] = '', 
  alphabet  : str = stdAlphabet, 
  notify : Optional[Callable[[str], None]] = None) -> None:
  self.notify = notify
  self._nextComponent : Optional[Component]  = None
  self._prevComponent : Optional[Component] = None
  assert name, '{}: At least 1 character in name required'.format(self.__class__.__name__)
  self._name = name
  assert alphabet, '{}/{}: At least 1 character in alphabet required'.format(self.__class__.__name__, self._name)
  self._alphabet = alphabet
  self._numberOfPositions = len(self.alphabet)
 
  if isinstance(wiring, dict):
   wiringList = self.alphabet.split('')
   for src, tgt in wiring.items():
    assert src in self.alphabet, '{}: Source character {} not in {}'.format(self.__class__.__name__, src, self.alphabet)
    srcID = self.alphabet.index(src)
    wiringList[srcID] = tgt
   wiring = ''.join(wiringList)
  self.wiring = wiring
  if self.__class__.__name__ == 'Umkehrwalze':
   for n, c in enumerate(self._alphabet):
    assert wiring[n] != c, '{}: Character {} reflected to itself'.format(self.__class__.__name__, c)
  
 def copy(self) -> Component:
  return copy.deepcopy(self)
 
 def nCC(self) -> int:
  ncc = 0
  for n, c in enumerate(self._wiring):
   ncc += (self._alphabet[n] != c)
  return ncc
  
 @property
 def name(self) -> str:
  """
  :getter: Returns the name of the componenrt  :setter: None
  """
  return self._name
 
 @property
 def alphabet(self) -> str:
  """
  :getter: Returns the alphabet of the engine
  :setter: None
  """
  return self._alphabet

 @property
 def numberOfPositions(self) -> int:
  """
  :getter: Returns the number of positions, usually len(alphabet)
  :setter: None
  """
  return self._numberOfPositions

 @property
 def wiring(self) -> str:
  """
  :getter: Returns the wiring
  :setter: Sets wiring and reverse wiring
  """
  return self._wiring

 @wiring.setter
 def wiring(self, newWiring : str) -> None:
  assert len(newWiring) == self._numberOfPositions,'{} {}: len(wiring) = {} != len(alphabet) = {}'.format(self.__class__.__name__, self._name, len(newWiring), self._numberOfPositions)
  _wiring = ''
  for n, c in enumerate(newWiring): 
   assert c in self.alphabet, '{}/wiring: Character {} not in {}'.format(self.__class__.__name__, c, self.alphabet)
   assert c not in _wiring, '{}/wiring: Duplicate character {} in wiring'.format(self.__class__.__name__, c)
   _wiring += c
  self._wiring = _wiring
  if '_rwiring' in vars(self):
   rwiringList = [' '] * self._numberOfPositions
   for n, c in enumerate(self._wiring):
    nr = self.alphabet.index(c)
    rwiringList[nr] = self.alphabet[n]
   self._rwiring = ''.join(rwiringList)
 
 @property
 def nextComponent(self) -> str:
  """
  :getter: Returns the next component in the chain
  :setter: Sets wiring and reverse wiring, if any 
  """
  return self._nextComponent
  
 @nextComponent.setter
 def nextComponent(self, component : Component) -> None:
  self._nextComponent = component

 @property
 def prevComponent(self) -> str:
  """
  :getter: Returns the previous component in the chain
  :setter: Sets wiring and reverse wiring
  """
  return self._prevComponent
  
 @prevComponent.setter
 def prevComponent(self, component : Component) -> None:
  if self.__class__.__name__ == 'Umkehrwalze':
   raise TypeError('{} is unidirectional'.format(self.__class__.__name__))
  self._prevComponent = component

 def encode(self, c : str, forward : bool, componentOnly : bool = False) -> str:
  """Runs forward or backward through a component

:param c: single character
:param forward: direction
:param componentOnly: do not go to next or previous component
:returns: encoded character (mapped back to the alphabet) 
  """
  assert len(c) == 1, '{}.encode({})/{}: len({}) != 1'.format(self.__class__.__name__, forward, self.name, c)
  assert c in self._alphabet, '{}.encode({})/{}: Character {} out of range'.format(self.__class__.__name__, forward, self.name, c)
  if '_ringstellung' in vars(self):
   state = self._alphabet.index(self._ringstellung)
  else:
   state = 0
  if forward:
   output = self._wiring[(self._alphabet.index(c) + state) % self._numberOfPositions]            
  else:
   output = self._alphabet[(self._alphabet.index(self._rwiring[self._alphabet.index(c)]) - state)  % self._numberOfPositions]     
  if self.notify is not None:
   self.notify('{}.encode({})/{}: {} => {}'.format(self.__class__.__name__, forward, self.name, c, output))
  if not componentOnly:
   if self._nextComponent and self.__class__ == Umkehrwalze:
    return self._nextComponent.encode(output, forward = False)
   elif self._nextComponent and forward:
    return self._nextComponent.encode(output, forward = True)
   elif self._prevComponent and not forward:
    return self._prevComponent.encode(output, forward = False)
  return output

 def chain(self, forward : bool = True) -> List[Tuple[Component, bool]]:
  """Creates a chain of visited components

:param forward: direction
:param _chain: current chain list (do not use)
:returns: (component, forward) list
  """
  chainList = list()
  lastComponent = self
  while lastComponent is not None:
   chainList.append((lastComponent, forward or lastComponent.__class__ == Umkehrwalze))
   if self.notify is not None:
    self.notify('{}.chain({})/{}'.format(self.__class__.__name__, forward, self.name))
   if lastComponent.__class__ == Umkehrwalze:
    lastComponent = lastComponent.nextComponent
    forward = False
   elif forward:
    lastComponent = lastComponent.nextComponent
   else:
    lastComponent = lastComponent.prevComponent
  return chainList
  
 def wiringToDict(self, connectedOnly : bool = False) -> Dict[str, str]:
  """Creates a dictionary starting from the wiring

:param connectedOnly: include only characters not connected to itself
:returns: dictionary of alphabet vs. wiring character
  """
  wiringDict = dict()
  for nc, c in enumerate(self.alphabet):
   if c != self.wiring[nc] or not connectedOnly:
    wiringDict[c] = self.wiring[nc]
  return wiringDict  

 def dictToWiring(self, wiringDict : Dict[str, str]) -> None:
  """Creates a dictionary starting from the wiring

:param wiringDict: dictionary of (at least connected) wirings
  """
  self.wiring = list(self.alphabet)
  for src, tgt in wiringDict.items():
   self.wiring[self.alphabet.index(src)] = tgt
  self.wiring = ''.join(self.wiring)  

 def __eq__(self, component : Component) -> bool:
  return self._name == component.name \
     and self._alphabet == component.alphabet \
     and self._wiring == component.wiring 

 def __repr__(self) -> str:
  return 'class: {}\nname: {}\nalphabet: {}\nwiring: {}'.format(
              self.__class__.__name__, self._name, self._alphabet, self._wiring)

class Steckerbrett(Umkehrwalze):
 """Represents a Steckerbrett (plugboard)

.. csv-table:: Wheel Controls
   :header: "Item", "Value"
   :widths: 30, 30
   
   *encryption*, forward and backward
   *ring*, none
   *notches*, none 

:param name: name of the Steckerbrett
:param wiring: wiring of the Steckerbrett, positions related to the *alphabet*
:param alphabet: unencoded alphabet to be used
:param notify: notification function (e.g. print)
 """
 def __init__(self, 
  name  : str = '', 
  wiring : Union[str, Dict[str, str]] = '', 
  alphabet  : str = stdAlphabet, 
  notify : Optional[Callable[[str], None]] = None) -> None:
  self._rwiring = ''
  super(Steckerbrett, self).__init__(name, wiring, alphabet, notify)
  if self.__class__ == Steckerbrett:
   if name == 'Mark 1':
    for group, groupWiring in zip([alphabet[:len(alphabet)//2], alphabet[len(alphabet)//2:]], [wiring[:len(alphabet)//2], wiring[len(alphabet)//2:]]):
     for ec in groupWiring:
      assert ec in group, '{} {}: Character {} not in {}'.format(self.__class__.__name__, self._name, ec, group)
   elif name == 'Mark 3':
    for c, ec in zip(alphabet, wiring):
     ecIndex = alphabet.index(ec)
     assert c == ec or c == wiring[ecIndex], '{} {}: Invalid connection {} -> {}'.format(self.__class__.__name__, self._name, c, ec)
 
 @staticmethod
 def Mark_1(
  replacement : bool = True, 
  alphabet : str = stdAlphabet, 
  notify : Optional[Callable[[str], None]] = None) -> Steckerbrett:
  """
  Random Initialization of a Mark 1 Steckerbrett (`crytomuseumSB`_)
  The contacts are splitted into 2 separated groups (sockets 1-13 and sockets 14-26)
  
.. _crytomuseumSB: https://www.cryptomuseum.com/crypto/enigma/i/sb.htm
  """
  wiring = str()
  for group in [alphabet[:len(alphabet)//2], alphabet[len(alphabet)//2:]]:
   while True: 
    actWiring = ''.join(random.sample(group, len(group)))
    hasReplacement = False
    if not replacement:
     for c, ec in zip(group, actWiring):
      if c == ec:
       hasReplacement = False
    if not hasReplacement:
     wiring += actWiring
     break
  return Steckerbrett('Mark 1', wiring, alphabet, notify)
     
 @staticmethod
 def Mark_2(
  replacement : bool = True, 
  alphabet : str = stdAlphabet, 
  notify : Optional[Callable[[str], None]] = None) -> Steckerbrett:
  """
  Random Initialization of a Mark 2 Steckerbrett (`crytomuseumSB`_)
  The 52 contacts are connected in unlimited fashion
  
.. _crytomuseumSB: https://www.cryptomuseum.com/crypto/enigma/i/sb.htm
  """
  wiring = str()
  while True: 
   actWiring = ''.join(random.sample(alphabet, len(alphabet)))
   hasReplacement = False
   if not replacement:
    for c, ec in zip(alphabet, actWiring):
     if c == ec:
      hasReplacement = False
   if not hasReplacement:
    wiring += actWiring
    break
  return Steckerbrett('Mark 2', wiring, alphabet, notify)

 @staticmethod
 def Mark_3(
  nConnections : int = 10, 
  alphabet : str = stdAlphabet, 
  notify : Optional[Callable[[str], None]] = None) -> Steckerbrett:
  """
  Random Initialization of a Mark 3 Steckerbrett (`crytomuseumSB`_)
  The 26 contacts are cross-connected, i.e. MU is combined with UM
  
.. _crytomuseumSB: https://www.cryptomuseum.com/crypto/enigma/i/sb.htm
  """
  assert nConnections >= 0 and nConnections <= len(alphabet) // 2, '{}: 0 < nConnections = {} < {} required'.format(Steckerbrett.__class__.__name__, nConnections, len(alphabet) // 2)
  sources = ''.join(random.sample(alphabet, nConnections))
  targetAlphabet = str()
  for c in alphabet:
   if c not in sources:
    targetAlphabet += c
  targets = ''.join(random.sample(targetAlphabet, nConnections))
  wiring = list(alphabet)
  for src, tgt in zip(sources, targets):
   srcIndex = alphabet.index(src)
   tgtIndex = alphabet.index(tgt)
   wiring[srcIndex] = tgt
   wiring[tgtIndex] = src
  return Steckerbrett('Mark 3', ''.join(wiring), alphabet, notify)
  
 def isMark1(self) -> bool:
  """
  Checks, if the steckerbrett is of type Mark1

:returns: indicator
  """
  halfAlphabet2 = self.alphabet[len(self.alphabet)//2:]
  for c in self.alphabet[:len(self.alphabet)//2]:
   if c not in halfAlphabet2:
    return False
  return True

 def isMark3(self) -> bool:
  """
  Checks, if the steckerbrett is of type Mark3
  
:returns: indicator
  """
  return self.wiring == self.rwiring
  
 def nConnections(self) -> int:
  """
  Counts the number of connections of a steckerbrett
  """
  nConnections2 = 0
  for n, c in enumerate(self.alphabet):
   if self.wiring[n] != c:
    nConnections2 += 1
  return nConnections2 // 2

 @staticmethod
 def _replaceChar(actStr : str, index : str, newStr : str) -> str:
  return actStr[:index] + newStr + actStr[index+1:]

 def clearMark3Setting(self, c : str) -> None:
  """
  Clear one setting of a Steckerbrett (`crytomuseumSB`_)
  """
  assert len(c) == 1, '{}.clearMark3Setting: {} is not a single character'.format(self.__class__.__name__, c)
  assert c in self.alphabet, '{}.clearMark3Setting: {} is not in alphabet'.format(self.__class__.__name__, c)
  srcIndex = self.alphabet.index(c)
  tgtIndex = self.alphabet.index(self.wiring[srcIndex])
  if srcIndex == tgtIndex:
   return
  assert c == self.wiring[tgtIndex], '{}.clearMark3Setting: {} is not in Mark 3 steckerbrett'.format(self.__class__.__name__, self.name)
  wiring = self.wiring
  wiring = self._replaceChar(wiring, srcIndex, self.alphabet[srcIndex])
  wiring = self._replaceChar(wiring, tgtIndex, self.alphabet[tgtIndex])
  self.wiring = wiring

 def addMark3Setting(self, src : str, tgt : str) -> None:
  """
  Add one setting to a Steckerbrett (`crytomuseumSB`_)
  """
  assert len(src) == 1 and len(tgt) == 1, '{}.addMark3Setting: Either src = {} and tgt = {} are not single characters'.format(
             self.__class__.__name__, src, tgt)
  assert src in self.alphabet and tgt in self.alphabet, '{}.addMark3Setting: Either src = {} and tgt = {} is not in alphabet'.format(
             self.__class__.__name__, src, tgt)
  if src == tgt:
   self.clearMark3Setting(src)
  srcIndex = self.alphabet.index(src)
  tgtIndex = self.alphabet.index(tgt)
  if src == self.wiring[tgtIndex] and tgt == self.wiring[srcIndex]:
   return
  assert src == self.wiring[srcIndex], '{}.addMark3Setting: src = {} is already connected'.format(self.__class__.__name__, src)
  assert tgt == self.wiring[tgtIndex], '{}.addMark3Setting: tgt = {} is already connected'.format(self.__class__.__name__, tgt)
  wiring = self.wiring
  wiring = self._replaceChar(wiring, srcIndex, tgt)
  wiring = self._replaceChar(wiring, tgtIndex, src)
  self.wiring = wiring

 def exchangeMark3Setting(self, c1 : str, c2 : str) -> None:
  """
  Exchanges 2 settings of a Steckerbrett (`crytomuseumSB`_)
  """
  assert len(c1) == 1 and len(c2) == 1, '{}.exchangeMark3Setting: Either src = {} and tgt = {} are not single characters'.format(
             self.__class__.__name__, c1, c2)
  assert c1 in self.alphabet and c2 in self.alphabet, '{}.exchangeMark3Setting: Either src = {} and tgt = {} is not in alphabet'.format(
             self.__class__.__name__, c1, c2)
  if c1 == c2:
   return
  c1Index = self.wiring.index(c1)
  assert c1 != self.alphabet[c1Index], '{}.exchangeMark3Setting: c1 = {} is unconnected'.format(self.__class__.__name__, c1)
  c2Index = self.wiring.index(c2)
  assert c2 != self.alphabet[c2Index], '{}.exchangeMark3Setting: c2 = {} is unconnected'.format(self.__class__.__name__, c2)
  wiring = self.wiring
  wiring = self._replaceChar(wiring, c1Index, c2)
  wiring = self._replaceChar(wiring, c2Index, c1)
  self.wiring = wiring

 @property
 def rwiring(self) -> str:
  """
  :getter: Returns the reverse wiring
  """
  return self._rwiring

 def __repr__(self) -> str:
  return super(Steckerbrett, self).__repr__() + '\nreverse wiring: {}'.format(self._rwiring)

class Zusatzwalze(Steckerbrett) : 
 """Represents an Zusatzwalze (ZW == extra rotor)

.. csv-table:: Wheel Controls
   :header: "Item", "Value"
   :widths: 30, 30
   
   *encryption*, forward and backward
   *ring*, yes
   *notches*, none 

:param name: name of the Zusatzwalze
:param wiring: wiring of the Zusatzwalze, positions related to the *alphabet*
:param alphabet: unencoded alphabet to be used
:param notify: notification function (e.g. print)
 """
 def __init__(self, 
  name  : str = '', 
  wiring : Union[str, Dict[str, str]] = '', 
  ringstellung : Optional[str] = None, 
  alphabet  : str = stdAlphabet, 
  notify : Optional[Callable[[str], None]] = None) -> None:
  """
  Initialization
  """
  super(Zusatzwalze, self).__init__(name, wiring, alphabet, notify)
  self._prevComponent : Optional[Component] = None
  if ringstellung is None:
   self._ringstellung = self._alphabet[0]
  else:
   assert len(ringstellung) == 1
   assert ringstellung in self._alphabet
   self._ringstellung = ringstellung

 @property
 def ringstellung(self) -> str:
  """
  :getter: Returns the ringstellung
  :setter: Sets the ringstellung
  """
  return self._ringstellung
  
 @ringstellung.setter
 def ringstellung(self, ringstellung : str) -> None:
   assert len(ringstellung) == 1, '{}.ringstellung {}: 1 character expected, {} got'.format(self.__class__.__name__, self._name, ringstellung)
   assert ringstellung in self._alphabet
   self._ringstellung = ringstellung

 def __eq__(self, component : Component) -> bool:
  return super(Zusatzwalze, self).__eq__(component) and self._ringstellung == component._ringstellung

 def __repr__(self) -> str:
  return super(Zusatzwalze, self).__repr__() + '\nringstellung: {}'.format(self._ringstellung)

class Walze(Zusatzwalze):
 """Represents a Walze (rotor)

.. csv-table:: Wheel Controls
   :header: "Item", "Value"
   :widths: 30, 30
   
   *encryption*, forward and backward
   *ring*, yes
   *notches*, yes 

:param name: name of the walze
:param wiring: wiring of the walze, positions related to the *alphabet*
:param ringstellung: visible character at the beginning, position related to the *alphabet*
:param notches: visible characters for the notches, positions related to the *alphabet*
:param alphabet: unencoded alphabet to be used
:param notify: notification function (e.g. print)

 """
 def __init__(self, 
  name  : str = '', 
  wiring : Union[str, Dict[str, str]] = '', 
  ringstellung : Optional[str] = None, 
  notches : str  = '', 
  alphabet : str = stdAlphabet, 
  notify : Optional[Callable[[str], None]] = None) -> None:
  """
  Initialization
  """
  super(Walze, self).__init__(name, wiring, ringstellung, alphabet, notify)
  assert notches, '{} {}: At least 1 notch required'.format(self.__class__.__name__, self._name)
  self._notches = ''
  for notch in notches:
   assert notch in self._alphabet, '{} {}: Notch {} out of range'.format(self.__class__.__name__, self._name, notch)
   assert notch not in self._notches, '{} {}: Duplicate notch {}'.format(self.__class__.__name__, self._name, notch)
   self._notches += notch
   
 def stepN(self, n : int)-> None:
  """
  Steps the Walze n times
  """
  assert n > 0, '{} {}: n == {} <= 0'.format(self.__class__.__name__, self._name, n)
  for _ in range(n):
   self.step()

 def step(self)-> None:
  """
  Steps the Walze and inititiates of the next Walze if available
  
   III	II	I	<-- wheel order
   A	D	O
   A	D	P
   A	D	Q
   A	E	R	<-- 1st step of middle wheel
   B	F	S	<-- 2nd step of middle wheel
   B	F	T
   B	F	U  
  """
  notchFound = self._ringstellung in self._notches
  if notchFound:
   if self._nextComponent and self._nextComponent.__class__.__name__ == 'Walze':
    self._nextComponent.step()
  self._ringstellung = self._alphabet[(self._alphabet.index(self._ringstellung) + 1) % self._numberOfPositions]
  if self.notify:
   self.notify('{}.step {}: {}, notch = {}'.format(self.__class__.__name__, self.name, self._ringstellung, notchFound))

 def __eq__(self, component : Component) -> bool:
  return super(Walze, self).__eq__(component) and self._notches == component._notches

 def __repr__(self) -> str:
  return super(Walze, self).__repr__() + '\nnotches: {}'.format(self._notches)

 @property
 def notches(self) -> str:
  """
  :getter: Returns the notches
  :setter: None
  """
  return self._notches
