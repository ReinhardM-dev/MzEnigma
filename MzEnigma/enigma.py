from __future__ import annotations
from typing import Optional, Union, Callable, List, Tuple, Set, Dict

import copy
import itertools
import random
import csv
import os
import math

import MzEnigma

class SpruchScoring(object):
 """Toolbox for scoring of a spruch. In the background, this object holds
 dictionary with character n-grams. By default, the dictionary with the 
 longest n-gram is used.
 
 :param language: language to be used for ngram scoring (required)
 :param normalize: normalize ngram values with respect to maxScore 
 :param logarithmic: 10*math.log10(ngramDict[score]/minScore)
  """
 def __init__(self, language : str, normalize : bool = True, logarithmic : bool = False):
  self.resPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Resources') 
  assert language in ['english', 'german'], "{}: Language {} not supported, use 'english' or 'german'".format(self.__class__.__name__, language)
  self.language = language
  self.normalize = normalize
  self.logarithmic = logarithmic
  self.ngramDict : Dict[int, Dict[str, float]] = dict()
  self.ngramLimits : Dict[int, Dict[str, float]] = dict()
  self.ngramDict[1], self.ngramLimits[1] = self._loadStatistics('{}_monograms.txt'.format(language))
  self.ngramDict[2], self.ngramLimits[2] = self._loadStatistics('{}_bigrams.txt'.format(language))
  self.ngramDict[3], self.ngramLimits[3] = self._loadStatistics('{}_trigrams.txt'.format(language))
  if self.ngramDict[3] is None:
   del self.ngramDict[3]
   del self.ngramLimits[3]
  if self.ngramDict[2] is None:
   del self.ngramDict[2]
   del self.ngramLimits[2]
  if self.ngramDict[1] is None:
   del self.ngramDict[1]
   del self.ngramLimits[1]
  self.numberOfChars = max(self.ngramDict.keys())
  self.saTemperature = 0.0
  self.saThreshold = 0.01
  
 def setSATemperature(self, spruch : str, numberOfChars : int = 0) -> float:
  """Enables the temperature for simulated annealing (used by `newNgramScore`)
 
 :param spruch: spruch of typical length to be scored (required)
 :param numberOfChars: n-gram dictionary to be used (default: longest n-grams) 
  """
  nSpruch = len(spruch)
  if nSpruch == 0:
   self.saTemperature = 0
  elif nSpruch <= 30:
   self.saTemperature = 400.0
  elif nSpruch <= 50:
   self.saTemperature = 400.0 - (400.0 - 315.0) * (nSpruch - 30) / (50 - 30)
  elif nSpruch <= 75:
   self.saTemperature = 315.0 - (315.0 - 240.0) * (nSpruch - 50) / (75 - 50)
  elif nSpruch <= 100:
   self.saTemperature = 240.0 - (240.0 - 220.0) * (nSpruch - 75) / (100 - 75)
  elif nSpruch <= 150:
   self.saTemperature = 220.0 - (220.0 - 200.0) * (nSpruch - 100) / (150 - 100)
  else:
   self.saTemperature = 200.0
  if numberOfChars < 1:
   assert 'numberOfChars' in vars(self), '{}.setSATemperature: no ngrams loaded'.format(self.__class__.__name__)
   numberOfChars = self.numberOfChars
  else:
   assert numberOfChars in self.ngramDict, '{}.setSATemperature: ngramDict[{}] not found'.format(self.__class__.__name__, numberOfChars)
  self.saTemperature /=  10^8
  return self.saTemperature

 def ngramScore(self, spruch : str, numberOfChars : int = 0, validChars : str = MzEnigma.stdAlphabet) -> float:
  """N-gram score of a spruch
 
 :param spruch: spruch to be scored (required)
 :param numberOfChars: n-gram dictionary to be used (default: longest n-grams) 
 :param validChars: alphabet of the spruch
 :returns: N-gram score
  """
  _score = 0
  if numberOfChars < 1:
   assert 'numberOfChars' in vars(self), '{}.ngramScore: no ngrams loaded'.format(self.__class__.__name__)
   numberOfChars = self.numberOfChars
  else:
   assert numberOfChars in self.ngramDict, '{}.ngramScore: ngramDict[{}] not found'.format(self.__class__.__name__, numberOfChars)
  nChars = len(list(self.ngramDict[numberOfChars].keys())[0])
  for c in validChars:
   assert c in self.ngramDict[numberOfChars], '{}.ngramScore: {} not in ngramDict[{}]'.format(self.__class__.__name__, c, numberOfChars)
  for n in range(len(spruch) - nChars + 1):
   ngram = spruch[n: n + nChars]
   for c in ngram:
    if c in validChars:
     _score += self.ngramDict[numberOfChars][ngram]
     break
  return _score/(len(spruch) - nChars + 1)

 def newNgramScore(self, spruch : str, currentScore : float, validChars : str = MzEnigma.stdAlphabet) -> float:
  """Compares the N-gram score of a spruch with the currentScore. 
  Uses simulated if enabled.
 
 :param spruch: spruch to be scored (required)
 :param currentScore: current score (required)
 :param validChars: alphabet of the spruch
 :returns: N-gram score
  """
  score = self.ngramScore(spruch, validChars = validChars)
  diffScore = score - currentScore
  if diffScore >= 0:
   return score
  if self.saTemperature <= 0:
   return currentScore
  diffScore /= self.saTemperature
  prob = math.exp(diffScore)
  if prob <= random.uniform(self.saThreshold, 1.0):
   score = currentScore
  return score

 @staticmethod
 def indexOfCoincidence(spruch : str, validChars : str = MzEnigma.stdAlphabet) -> float:
  """index of coincidence of a spruch,
  i.e. relative frequency of characters independent of the underlying language 
 
 :param spruch: spruch to be scored (required)
 :param validChars: alphabet of the spruch
 :returns: index of coincidence
  """
  nAlphabet = len(validChars)
  nSpruch = len(spruch)
  iocList = nAlphabet * [0.0]
  for c in spruch:
   iocList[validChars.index(c)] += 1
  ioc = 0
  for n in range(nAlphabet):
   ioc += iocList[n] * (iocList[n] - 1)
  return ioc/(nSpruch * (nSpruch-1))

 def _loadStatistics(self, statfile : str) -> Dict[str, float]:
  ngramDict : Dict[str, Union[float, int]] = dict()
  alphabet = set(MzEnigma.stdAlphabet) | set(MzEnigma.sgsAlphabet)
  actPath = os.path.join(self.resPath, statfile)
  if not os.path.exists(actPath):
   return None, None
  with open(actPath, newline='') as csvfile:
   for ngram, nDetected in csv.reader(csvfile, delimiter=' '):
    isInside = True
    for c in ngram:
     isInside &= c in alphabet
    if isInside:
     nDetected = float(nDetected)
     assert nDetected > 0
     ngramDict[ngram] = nDetected
  maxValue = max(ngramDict.values())
  minValue = min(ngramDict.values())
  if self.logarithmic:
   ngramDict.update({ngram : 10*math.log10(ngramDict[ngram]/minValue) for ngram in ngramDict.keys()})
  elif self.normalize:
   ngramDict.update({ngram : ngramDict[ngram]/maxValue for ngram in ngramDict.keys()})
  else:
   minValue /= maxValue
   maxValue = 1
  return ngramDict, (minValue, maxValue)

 def __repr__(self) -> str:
  return '{}\n language: {}\n normalized: {}\n logarithmic: {}'.format(self.__class__.__name__, self.language, self.normalize, self.logarithmic)

class Enigma(object):
 """Represents an Enigma engine with all available accessories. 
    If no umkehrwalzen are defined, the encryption is not symmetric any more !
 
 :param model: model of the Enigma (required)
 :param umkehrwalzen: available objects of type 'Umkehrwalze' (if any)
 :param walzen: available objects of type 'Walze' (at least 1 required)
 :param numberOfWalzen: number of  objects of type 'Walze' to be inserted
 :param steckerbrett: object of type 'Steckerbrett', if any
 :param zusatzwalzen: available objects of type 'Zusatzwalze', if any
 :param notify: notification function (e.g. print)
  """
 def __init__(self, 
  model  : str = '', 
  umkehrwalzen : List[MzEnigma.Umkehrwalze] = None, 
  walzen : List[MzEnigma.Walze] = None, 
  numberOfWalzen : int = 0, 
  steckerbrett : Optional[MzEnigma.Steckerbrett] = None, 
  zusatzwalzen : List[MzEnigma.Zusatzwalze] = None) -> None:
  assert model, '{}: At least 1 character in model required'.format(self.__class__.__name__)
  self._model = model
  assert walzen, '{}: At least 1 walze required'.format(self.__class__.__name__)
  alphabet = walzen[0].alphabet
  assert all(v.alphabet == alphabet for v in walzen), '{}: Alphabets in all walzen must match'.format(self.__class__.__name__)
  self._walzen = walzen
  if umkehrwalzen:
   assert all(v.alphabet == alphabet for v in umkehrwalzen), '{}: Alphabets in all umkehrwalzen must match'.format(self.__class__.__name__)
  self._umkehrwalzen = umkehrwalzen
  assert numberOfWalzen > 0 and numberOfWalzen <= len(walzen), '{}: 0 < numberOfWalzen < {}  required'.format(self.__class__.__name__, len(walzen))
  self._numberOfWalzen = numberOfWalzen
  if steckerbrett:
   assert steckerbrett.alphabet == alphabet, '{}: Alphabets in steckerbrett must match'.format(self.__class__.__name__)
  self._steckerbrett = steckerbrett
  if zusatzwalzen:
   assert all(v.alphabet == alphabet for v in zusatzwalzen), '{}: Alphabets in all zusatzwalzen must match'.format(self.__class__.__name__)
  self._zusatzwalzen = zusatzwalzen

 @staticmethod
 def validCribPositions(encodedSpruch : str = '', crib : str = '') -> List[int]:
  """This function delivers all positions where no crib letter encrypts as itself
  
:param encodedSpruch: message to be decoded
:param crib: substring to be examined
:returns: list of valid positions relative to the encodedSpruch
   """
  assert len(encodedSpruch) > 0, 'validCribPositions: encodedSpruch is missing'
  assert len(crib) > 0, 'validCribPositions: crib is missing'
  assert len(crib) <= len(encodedSpruch), 'validCribPositions: len(encodedSpruch) == {} < len(crib) == {}'.format(len(encodedSpruch), len(crib))

  validPosList = list()
  for startPos in range(0, len(encodedSpruch) - len(crib) + 1):
   # match = difflib.SequenceMatcher(None, encodedSpruch[startPos:], crib)
   isMatched = False
   for ps, pc in zip(encodedSpruch[startPos:], crib):
    if ps == pc:
     isMatched = True
     break
   if not isMatched:
    validPosList.append(startPos)
  return validPosList
  
 @property
 def alphabet(self) -> str:
  """
  :getter: Returns the alphabet of the engine
  :setter: None
  """
  return self._walzen[0].alphabet

 @property
 def model(self) -> str:
  """
  :getter: Returns the name of the engine
  :setter: None
  """
  return self._model

 @property
 def umkehrwalzen(self) -> List[MzEnigma.Umkehrwalze]:
  """
  :getter: Returns a list of Umkehrwalzen
  :setter: None
  """
  return self._umkehrwalzen

 @property
 def walzen(self) -> List[MzEnigma.Walze]:
  """
  :getter: Returns a list of Walzen
  :setter: None
  """
  return self._walzen

 @property
 def numberOfWalzen(self) -> int:
  """
  :getter: Returns a number of Walzen built-in at the engine's operation
  :setter: None
  """
  return self._numberOfWalzen

 @property
 def steckerbrett(self) -> Optional[int]:
  """
  :getter: Returns the steckerbrett if any
  :setter: None
  """
  return self._steckerbrett

 @property
 def zusatzwalzen(self) -> Optional[List[MzEnigma.Zusatzwalze]]:
  """
  :getter: Returns a list of Zusatzwalzen if any
  :setter: None
  """
  return self._zusatzwalzen
  
 def __eq__(self, enigma : Enigma) -> bool:
  return self._model == enigma.model \
     and self._umkehrwalzen == enigma.umkehrwalzen \
     and self._walzen == enigma.walzen \
     and self._numberOfWalzen == enigma.numberOfWalzen \
     and self._steckerbrett == enigma.steckerbrett \
     and self._zusatzwalzen == enigma.zusatzwalzen 

 def __repr__(self) -> str:
  content = 'class: {}\nmodel: {}\nalphabet: {}\nUmkehrwalzen:'.format(self.__class__.__name__, self._model, self.alphabet)
  for walze in self._umkehrwalzen:
   for line in walze.__repr__().split('\n'):
    if 'class:' not in line and 'alphabet:' not in line:
     content += '\n ' + line
  content += '\nnumber of Walzen: {}\nWalzen:'.format(self._numberOfWalzen)
  for walze in self._walzen:
   for line in walze.__repr__().split('\n'):
    if 'class:' not in line and 'alphabet:' not in line:
     content += '\n ' + line
  if self._steckerbrett:
   content += '\nSteckerbrett:'
   for line in self._steckerbrett.__repr__().split('\n'):
    if 'class:' not in line and 'alphabet:' not in line:
     content += '\n ' + line
  if self._zusatzwalzen:
   content += '\nZusatzwalzen:'
   for walze in self._zusatzwalzen:
    for line in walze.__repr__().split('\n'):
     if 'class:' not in line and 'alphabet:' not in line:
      content += '\n ' + line
  return content

class Tagesschluessel(object):
 """Represents the Tagesschluessel of an Enigma
 
:param enigma: model of the Enigma (required)
:param umkehrwalze: 'Umkehrwalze' (if undefined, randomly selected)
:param walzen: List of type 'Walze' (if undefined, randomly selecte(if undefined, randomly selected)
:param zusatzwalze: 'Zusatzwalze' (if undefined, randomly selected)
:param blank: replacement character for a blank
:param notify: notification function (e.g. print)
  """
 def __init__(self,
  enigma : Optional[Enigma] = None,  
  umkehrwalze : Optional[MzEnigma.Umkehrwalze] = None, 
  walzen : Optional[List[MzEnigma.Walze]] = None,
  tagesWalzenStellungen : Optional[str] = None, 
  steckerbrett : Optional[MzEnigma.Steckerbrett] = None, 
  zusatzwalze : Optional[MzEnigma.Zusatzwalze] = None, 
  blank : str = '',  
  notify : Optional[Callable[[str], None]] = None) -> None:
  self.notify = notify
  assert enigma, '{}: Enigma required'.format(self.__class__.__name__)
  self.enigma =enigma
  self.blank = blank
  alphabet = self.enigma.alphabet
  if steckerbrett is None and enigma.steckerbrett:
   self.steckerbrett = copy.deepcopy(enigma.steckerbrett)
   self.steckerbrett.notify = self.notify
  else:
   self.steckerbrett = steckerbrett
  lastWalze = self.steckerbrett
  if not walzen:
   walzen = random.sample(enigma.walzen, enigma.numberOfWalzen)
  assert all(v.alphabet == alphabet for v in walzen), '{}: Alphabet in all walzen must match enigma'.format(self.__class__.__name__)
  self.walzen = list()
  for _walze in walzen:
   walze = copy.deepcopy(_walze)
   walze.notify = self.notify
   self.walzen.append(walze)
   if lastWalze:
    lastWalze.nextComponent = walze
    walze.prevComponent = lastWalze
   lastWalze = walze
  if self.steckerbrett:
   self.firstComponent = self.steckerbrett
  else:
   self.firstComponent = self.walzen[0]
  if tagesWalzenStellungen:
   assert len(tagesWalzenStellungen) == len(walzen), '{}: Walzenstellung, number of characters must match the number of walzen'.format(self.__class__.__name__)
   assert all(v in alphabet for v in tagesWalzenStellungen), '{}: Walzenstellung, all characters must be in alphabet'.format(self.__class__.__name__)
  else:
   tagesWalzenStellungen = ''.join(random.sample(alphabet, enigma.numberOfWalzen))
  self.tagesWalzenStellungen = tagesWalzenStellungen
  if zusatzwalze:
   assert zusatzwalze.alphabet == alphabet, '{}: Alphabet in zusatzwalze must match enigma'.format(self.__class__.__name__)
  elif enigma.zusatzwalzen is not None:
   zusatzwalze = random.sample(enigma.zusatzwalzen, 1)[0]
  if zusatzwalze:
   self.zusatzwalze = copy.deepcopy(zusatzwalze)
   self.zusatzwalze.notify = self.notify
   lastWalze.nextComponent = self.zusatzwalze
   self.zusatzwalze.prevComponent = lastWalze
   lastWalze = self.zusatzwalze
  else:
   self.zusatzwalze = None
  if umkehrwalze:
   assert umkehrwalze.alphabet == alphabet, '{}: Alphabet in umkehrwalze must match enigma alphabet'.format(self.__class__.__name__)
  elif len(enigma.umkehrwalzen) > 0:
   umkehrwalze = random.sample(enigma.umkehrwalzen, 1)[0]
  else:
   self.umkehrwalze = None
  if umkehrwalze:
   self.umkehrwalze = copy.deepcopy(umkehrwalze)
   self.umkehrwalze.notify = self.notify
   lastWalze.nextComponent = self.umkehrwalze
   self.umkehrwalze.nextComponent = lastWalze

 @classmethod
 def changeWalzen(cls, 
   currentTagesschluessel : Tagesschluessel, 
   umkehrwalze : Optional[MzEnigma.Umkehrwalze] = None, 
   walzen : List[MzEnigma.Walze] = None, 
   tagesWalzenStellungen : Optional[str] = None, 
   zusatzwalze : Optional[MzEnigma.Zusatzwalze] = None) -> None:
  """Changes certain elements of a Tagesschluessel
 
:param currentTagesschluessel: current Tagesschluessel (required)
:param tagesWalzenStellungen: changed Tageswalzenstellungen to be used (if undefined, randomly selected)
:param umkehrwalze: 'Umkehrwalze' (if undefined, used from currentTagesschluessel)
:param walzen: List of type 'Walze' (if undefined, used from currentTagesschluessel)
:param zusatzwalze: 'Zusatzwalze' (if undefined, used from currentTagesschluessel)
:returns: Tagesschluessel object
   """
  if umkehrwalze is None:
   umkehrwalze = currentTagesschluessel.umkehrwalze
  if walzen is None:
   walzen = currentTagesschluessel.walzen
  if zusatzwalze is None:
   zusatzwalze = currentTagesschluessel.zusatzwalze
  return cls(
   enigma = currentTagesschluessel.enigma,  
   umkehrwalze = umkehrwalze, 
   steckerbrett = currentTagesschluessel.steckerbrett, 
   walzen = walzen, 
   tagesWalzenStellungen = tagesWalzenStellungen, 
   zusatzwalze = zusatzwalze, 
   blank = currentTagesschluessel.blank,  
   notify = currentTagesschluessel.notify)

 def findPatterns(self, substringList : List[str] = [''], encodedSpruchList : List[str] = []) -> Dict[str, Set[str]]:
  """Find a list of substringList for any tagesWalzenStellungen at any positions
 
:param substringList: list of substrings
:param encodedSpruchList: list of messages to be searched for substrings
:return: dict(substring, set of tagesWalzenStellungen)
  """
  assert len(encodedSpruchList) > 0
  maxSpruchlength = max(encodedSpruchList, key=len)
  charSet = set()
  for substring in substringList:
   for c in substring:
    assert c in self.alphabet, '{}: Character {} not in {}'.format(self.__class__.__name__, c, self.enigma.alphabet)
    charSet.add(c)
  savedTagesWalzenStellungen = self.tagesWalzenStellungen 
  patternDict : Dict[str, Set[str]] = dict()
  for tagesWalzenStellungenTuple in itertools.permutations(self.alphabet, len(savedTagesWalzenStellungen)):
   self.tagesWalzenStellungen = ''.join(tagesWalzenStellungenTuple)
   charEncodingDict = dict()
   for c in charSet:
    charEncodingDict[c] = self.encode(maxSpruchlength * c)
   for encodedSpruch in encodedSpruchList:
    lSpruch = len(encodedSpruch)
    for substring in substringList:
     isInSpruch = False
     ls = lSpruch - len(substring)
     for n, (c0, cExp) in enumerate(zip(encodedSpruch[:ls], charEncodingDict[substring[0]][:ls])):
      if c0 == cExp:
       for m, cm in enumerate(substring[1:]):
        nm = n + m + 1
        if cm == charEncodingDict[substring[m]][nm]:
         if m == len(substring) - 2:
          isInSpruch = True
          break
     if isInSpruch:
      if substring not in patternDict:
       patternDict[substring] = list()
      patternDict[substring].add(self.tagesWalzenStellungen)
  return patternDict

 def findDoublets(self, first : int = 0, second : int = 3, all : bool = True) -> Union[List[List[str]], List[str]]:
  """Find doublets of any character at fixed positions
 
:param first: first position
:param second: second position (> first)
:return: IF ALL it returns a list of doublets for every position ELSE it returns a list of doublets
  """
  assert first >= 0 and second > first
  allDoubletsList = list()
  if all:
   shift = second - first
  else:
   shift = 1
  ecList = list()
  for nc, c in enumerate(self.alphabet):
   ecList.append(list())
   for cs in self.encode((second + shift) * c):
    ecList[-1].append(cs)
  for ns in range(shift):
   doubletsList = list()
   for n, c in enumerate(self.alphabet):
    doubletsList.append(ecList[n][first+ns] + ecList[n][second+ns])
   allDoubletsList.append(doubletsList)
  if not all:
   return doubletsList
  return allDoubletsList

 def findTagesWalzenStellungen(self, rejewskiList : List[Dict[str, Set[str]]], twiceEncodedSpruchWalzenStellungen : Union[List[str], str] = '') -> List[str]:
  if isinstance(twiceEncodedSpruchWalzenStellungen, str):
   twiceEncodedSpruchWalzenStellungen = [twiceEncodedSpruchWalzenStellungen]
  tagesWalzenStellungen = None
  for tesws in twiceEncodedSpruchWalzenStellungen:
   shift = len(tesws) // 2
   assert shift == len(rejewskiList), '{}.findTagesWalzenStellungen: len(twiceEncodedSpruchWalzenStellungen) = {} == 2*len(rejewskiList) = {}'.format(self.__class__.__name__, shift, 2*len(rejewskiList))
   for n, doubletsDict in enumerate(rejewskiList):
    pair = tesws[n] + tesws[n+shift]
    assert pair in rejewskiList[n].keys(), '{}.findTagesWalzenStellungen: {} not a key of rejewskiList[{}]'.format(self.__class__.__name__, pair, n)
    if tagesWalzenStellungen is None:
     tagesWalzenStellungen = rejewskiList[n][pair]
    else:
     tagesWalzenStellungen &= rejewskiList[n][pair]
  return sorted(tagesWalzenStellungen)

 def encode(self, spruch : str, spruchWalzenStellungen : Optional[str] = None) -> str:
  """Runs forward through the enigma
     If the spruchWalzenStellungen is defined, 
     - it is encoded twice using the tagesWalzenStellungen
     - the spruch is then encoded using the spruchWalzenStellungen
     otherwise the spruch is encoded using the tagesWalzenStellungen

:param spruch: message to be encoded
:param spruchWalzenStellungen: see above
:returns: encoded spruch
  """
  for walze, ringstellung in zip(self.walzen, self.tagesWalzenStellungen):
   walze.ringstellung = ringstellung
  out = str()
  if spruchWalzenStellungen:
   assert len(spruchWalzenStellungen) == len(self.tagesWalzenStellungen), '{}.encode: Walzenstellung, number of characters must match the number of walzen'.format(self.__class__.__name__)
   assert all(v in self.alphabet for v in spruchWalzenStellungen), '{}.encode: Walzenstellung, all characters must be in alphabet'.format(self.__class__.__name__)
   for n in range(2):
    for c in spruchWalzenStellungen:
     out += self._encodeLetter(c)
   for walze, ringstellung in zip(self.walzen, spruchWalzenStellungen):
    walze.ringstellung = ringstellung
   if self.notify is not None:
    self.notify('{}.encode/spruchWalzenStellungen: {} => {}'.format(self.__class__.__name__, spruchWalzenStellungen, out[:len(spruchWalzenStellungen)]))
  for c in spruch.upper():
   if c == ' ':
    c = self.blank
   if len(c) == 1:
    out += self._encodeLetter(c)
  if self.notify is not None:
   self.notify('{}.encode: {} => {}'.format(self.__class__.__name__, spruch, out))
  for walze, ringstellung in zip(self.walzen, self.tagesWalzenStellungen):
   walze.ringstellung = ringstellung
  return out

 def encodeMatrix(self, msgLen : int) -> List[List[str]]:
  """Runs forward through the enigma using all characters of the alphabet

:param msgLen: length of messages
:returns: list of encoded messages
  """
  ecList = list()
  for nc, c in enumerate(self.enigma.alphabet):
   ecList.append(list())
   for cs in self.encode(msgLen * c):
    ecList[-1].append(self.enigma.alphabet.index(cs))
  return ecList

 def decode(self, encodedSpruch : str, useSpruchWalzenStellungen : bool = False) -> str:
  """Runs backward through the enigma
     If useSpruchWalzenStellungen, 
     - the spruchWalzenStellung is expected twice at the beginning
     - the spruch is then decoded using the spruchWalzenStellungen
     otherwise the spruch is decoded using the tagesWalzenStellungen

:param encodedSpruch: message to be decoded
:param useSpruchWalzenStellungen: see above
:returns: decoded spruch
  """
  for walze, ringstellung in zip(self.walzen, self.tagesWalzenStellungen):
   walze.ringstellung = ringstellung
  if useSpruchWalzenStellungen:
   spruchWalzenStellungen = str()
   ls = len(self.tagesWalzenStellungen)
   for c in encodedSpruch[:2*ls]:
    spruchWalzenStellungen += self._encodeLetter(c)
   assert spruchWalzenStellungen[:ls] == spruchWalzenStellungen[ls:], '{}.decode: Inconsistent Spruchschlüssel {}'.format(self.__class__.__name__, spruchWalzenStellungen)
   if self.notify is not None:
    self.notify('{}.decode/spruchWalzenStellungen: {} => {}'.format(self.__class__.__name__, encodedSpruch[:ls], spruchWalzenStellungen[:ls]))
   for walze, ringstellung in zip(self.walzen, spruchWalzenStellungen[:ls]):
    walze.ringstellung = ringstellung
   encodedSpruch = encodedSpruch[2*ls:]
  out = str()
  for c in encodedSpruch:
   out += self._encodeLetter(c)
  for walze, ringstellung in zip(self.walzen, self.tagesWalzenStellungen):
   walze.ringstellung = ringstellung
  return out
     
 def _encodeLetter(self, c : str) -> str:
  """Encodes a single character and steps the first Walze
  
:param c: single character
:returns: encoded character
  """
  assert len(c) == 1, '{}.encodeLetter {}: len({}) != 1'.format(self.__class__.__name__, self.name, c)
  assert c in self.enigma.alphabet, '{}.encodeLetter: letter ({}) not in alphabet'.format(self.__class__.__name__, c)
  self.walzen[0].step()
  return self.firstComponent.encode(c, forward = True)
  
 def chain(self) -> List[MzEnigma.Component]:
  """Creates a chain of visited components

:returns: chain list
  """
  chainList = self.firstComponent.chain(forward = True)
  return chainList
  
 def debugEncode(self, c : str ) -> str:
  """Shows the transformation of a character after each component
 
:param c: single character
:return: text built up from the characters after each component
  """
  assert len(c) == 1, '{}.debugEncode: len({}) != 1'.format(self.__class__.__name__, c)
  assert c in self.enigma.alphabet, '{}.debugEncode: Character {} out of range'.format(self.__class__.__name__, c)
  for walze, ringstellung in zip(self.walzen, self.tagesWalzenStellungen):
   walze.ringstellung = ringstellung
  output = ''
  actC = c
  for component, forward in self.chain():
   actC = component.encode(actC, forward, componentOnly = True)
   output += actC
  return output
   
 def frequencyDict(self, spruch : str, decode : bool = True) -> Dict[int, Set[Tuple[str, Set[str]]]]:
  """Creates a frequency dictionary of a message
 
:param spruch: message to be analysed (required)
:param decode: use decoced message instead of the original message
:return: Dict[frequency, Set[Tuple[char, Tuple[occurrency]]
  """
  if decode:
   spruch = self.decode(spruch)
  assert len(spruch) > 0
  c2sDict = dict()
  for n, sc in enumerate(spruch):
   if sc not in c2sDict:
    c2sDict[sc] = set()
   c2sDict[sc].add(n)
  l2csDict = dict()
  for c, nSet in c2sDict.items():
   l = len(nSet)
   if l not in l2csDict:
    l2csDict[l] = set()
   l2csDict[l].add((c, tuple(sorted(nSet))))
  return l2csDict
  
 @property
 def alphabet(self) -> str:
  """
  :getter: Returns the alphabet of the engine
  :setter: None
  """
  return self.enigma.alphabet

 def __eq__(self, tagesschluessel : Tagesschluessel) -> bool:
  return self.enigma == tagesschluessel.enigma \
     and self.tagesWalzenStellungen == tagesschluessel.tagesWalzenStellungen \
     and self.umkehrwalze == tagesschluessel.umkehrwalze \
     and self.walzen == tagesschluessel.walzen \
     and self.steckerbrett == tagesschluessel.steckerbrett \
     and self.zusatzwalze == tagesschluessel.zusatzwalze

 def __repr__(self) -> str:
  content = 'class: {}\nmodel: {}\nalphabet: {}'.format(self.__class__.__name__, self.enigma.model, self.alphabet)
  for walze, ringstellung in zip(self.walzen, self.tagesWalzenStellungen):
   content += '\nWalze {}, Stellung: {}, wiring: {}, notches: {}'.format(walze.name, ringstellung, walze.wiring, walze.notches)
  content += '\nUmkehrwalze: {}, wiring: {}'.format(self.umkehrwalze.name, self.umkehrwalze.wiring)
  if self.steckerbrett:
   content += '\nSteckerbrett {}, wiring: {}'.format(self.steckerbrett.name, self.steckerbrett.wiring)
  if self.zusatzwalze:
   content += '\nZusatzwalze: {}, wiring: {}'.format(self.zusatzwalze.name, self.zusatzwalze.wiring)
  return content

