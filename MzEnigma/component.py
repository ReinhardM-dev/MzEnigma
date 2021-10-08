from typing import TypeVar,  Union, Optional, Callable, List, Dict
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

:param name: name of the walze
:param wiring: wiring of the walze, positions related to the *alphabet*
:param alphabet: unencoded alphabet to be used
:param notify: notification function (e.g. print)
 """
 def __init__(self, 
  name  : str = '', 
  wiring : Union[str, Dict[str, str]] = '', 
  alphabet  : str = stdAlphabet, 
  notify : Optional[Callable[[str], None]] = None) -> None:
  """
  Initialization
  """
  self.notify = notify
  self._nextComponent : Optional[Component]  = None
  assert name, '{}: At least 1 character in name required'.format(self.__class__.__name__)
  self._name = name
  assert alphabet, '{}/{}: At least 1 character in alphabet required'.format(self.__class__.__name__, self._name)
  self._alphabet = alphabet
  self._numberOfPositions = len(self.alphabet)
 
  if isinstance(wiring, str):
   assert len(wiring) == self._numberOfPositions,'{} {}: len(wiring) = {} != len(alphabet) = {}'.format(self.__class__.__name__, self._name, len(wiring), self._numberOfPositions)
  else:
   wiringList = self.alphabet.split('')
   for src, tgt in wiring.items():
    assert src in self.alphabet, '{}: Source character {} not in {}'.format(self.__class__.__name__, src, self.alphabet)
    srcID = self.alphabet.index(src)
    wiringList[srcID] = tgt
   wiring = ''.join(wiringList)
  self._wiring = ''
  for c in wiring:
   assert c not in self._wiring, '{}: Duplicate character {} in wiring'.format(self.__class__.__name__, c)
   assert c in self.alphabet, '{}: Encrypted character {} not in {}'.format(self.__class__.__name__, c, self.alphabet)
   self._wiring += c
  if self.__class__.__name__ == 'Umkehrwalze':
   for n, c in enumerate(self._alphabet):
    assert self._wiring[n] != c, '{}: Character {} reflected to itself'.format(self.__class__.__name__, c)
  
 def copy(self) -> Component:
  return copy.deepcopy(self)
  
 @property
 def name(self) -> str:
  return self._name
 
 @property
 def alphabet(self) -> str:
  return self._alphabet

 @property
 def numberOfPositions(self) -> int:
  return self._numberOfPositions

 @property
 def wiring(self) -> str:
  return self._wiring

 @property
 def nextComponent(self) -> str:
  return self._nextComponent
  
 @nextComponent.setter
 def nextComponent(self, component : Component) -> None:
  self._nextComponent = component

 def encodeForward(self, c : str = '') -> str:
  assert len(c) == 1, '{}.encodeForward {}: len({}) != 1'.format(self.__class__.__name__, self.name, c)
  assert c in self._alphabet, '{}.encodeForward {}: Character {} out of range'.format(self.__class__.__name__, self.name, c)
  if '_ringstellung' in vars(self):
   state = self._alphabet.index(self._ringstellung)
   output = self._wiring[(state + self._alphabet.index(c)) % self._numberOfPositions]            
  else:
   output = self._wiring[self._alphabet.index(c) % self._numberOfPositions]            
  if self.notify is not None:
   self.notify('{}.encodeForward {}: {} => {}'.format(self.__class__.__name__, self.name, input, output))
  if self._nextComponent:
   return self._nextComponent.encodeForward(output)
  else:
   return output

 def __eq__(self, component : Component) -> bool:
  return self._name == component.name \
     and self._alphabet == component.alphabet \
     and self._wiring == component.wiring 

 def __repr__(self) -> str:
  return 'class: {}\nname: {}\nalphabet: {}\nwiring: {}'.format(
              self.__class__.__name__, self._name, self._alphabet, self._wiring)

class Steckerbrett(Umkehrwalze):
 """Represents an Umkehrwalze (UKW == reflector)

.. csv-table:: Wheel Controls
   :header: "Item", "Value"
   :widths: 30, 30
   
   *encryption*, forward and backward
   *ring*, none
   *notches*, none 

:param name: name of the walze
:param wiring: wiring of the walze, positions related to the *alphabet*
:param alphabet: unencoded alphabet to be used
:param notify: notification function (e.g. print)
 """
 def __init__(self, 
  name  : str = '', 
  wiring : Union[str, Dict[str, str]] = '', 
  alphabet  : str = stdAlphabet, 
  notify : Optional[Callable[[str], None]] = None) -> None:
  """
  Initialization
  """
  super(Steckerbrett, self).__init__(name, wiring, alphabet, notify)
  self._prevComponent : Optional[Component] = None
  rwiringList = [' '] * self._numberOfPositions
  for n, c in enumerate(self._wiring):
   assert c in self._alphabet, '{} {}: Character {} out of range'.format(self.__class__.__name__, self._name, c)
   assert self._alphabet[n] not in rwiringList, '{} {}: Duplicate character {}'.format(self.__class__.__name__, self._name, c)
   rwiringList[self._alphabet.index(c)] = self._alphabet[n]
  self._rwiring = ''.join(rwiringList)
 
 @classmethod
 def RandomSteckerbrett(cls,
  name  : str = '', 
  nConnections : int = -1, 
  selfEncoding : bool = False, 
  alphabet  : str = stdAlphabet, 
  notify : Optional[Callable[[str], None]] = None) -> Steckerbrett:
  """
  Random Initialization
  """
  assert nConnections >= 0 and nConnections <= len(alphabet), '{} {}: invalid number of connections {}'.format('Steckerbrett', name, nConnections)
  for n in range(100):
   wiring = ''.join(random.sample(alphabet, len(alphabet)))
   if not selfEncoding:
    wiringList = list()
    for ec, c in zip(wiring, alphabet):
     if ec != c:
      wiringList.append(ec)
    wiring = ''.join(wiringList)
   if len(wiring) >= nConnections:
    return Steckerbrett(name, wiring, alphabet, notify)
  raise ValueError('Random Initialization of Steckerbrett {}  with {} connections failed'.format(name, nConnections))
     
 @property
 def rwiring(self) -> str:
  return self._rwiring

 @property
 def prevComponent(self) -> str:
  return self._prevComponent
  
 @prevComponent.setter
 def prevComponent(self, component : Component) -> None:
   self._prevComponent = component

 def encodeBackward(self, c : str = '') -> str:
  assert len(c) == 1, '{}.encodeBackward {}: len({}) != 1'.format(self.__class__.__name__, self._name, c)
  assert c in self._alphabet, '{}.encodeBackward {}: Character {} out of range'.format(self.__class__.__name__, self._name, c)
  state = self._alphabet.index(self._ringstellung)
  output = self._rwiring[(state + self._alphabet.index(c)) % self._numberOfPositions]            
  if self.notify is not None:
   self.notify('Steckerbrett.encodeBackward {}: {} => {}'.format(self._name, input, output))
  if self._prevComponent:
   return self._prevComponent.encodeBackward(output)
  else:
   return output

class Zusatzwalze(Steckerbrett) : 
 """Represents an Zusatzwalze (ZW == extra rotor)

.. csv-table:: Wheel Controls
   :header: "Item", "Value"
   :widths: 30, 30
   
   *encryption*, forward and backward
   *ring*, yes
   *notches*, none 

:param name: name of the walze
:param wiring: wiring of the walze, positions related to the *alphabet*
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
  if ringstellung is None:
   self._ringstellung = self._alphabet[0]
  else:
   assert len(ringstellung) == 1
   assert ringstellung in self._alphabet
   self._ringstellung = ringstellung

 @property
 def ringstellung(self) -> str:
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
   
 def step(self) -> int:
  """
  Steps the Walze.
  If a next Walze is specified, do the check to see if we've reached the notch,
  thus requiring that Walze to step.
  """
  notchFound = self._ringstellung in self._notches
  if notchFound:
   offset = 2
   if self._nextComponent:
    self._nextComponent.step()
  else:
   offset = 1
  self._ringstellung = self._alphabet[(self._alphabet.index(self._ringstellung) + offset) % self._numberOfPositions]
  if self.notify:
   self.notify('{}.step {}: {}, notch = {}'.format(self.__class__.__name__, self.name, self._ringstellung, notchFound))
  return self._alphabet.index(self._ringstellung)

 def __eq__(self, component : Component) -> bool:
  return super(Walze, self).__eq__(component) and self._notches == component._notches

 def __repr__(self) -> str:
  return super(Walze, self).__repr__() + '\nnotches: {}'.format(self._notches)

 @property
 def notches(self) -> str:
  return self._notches

