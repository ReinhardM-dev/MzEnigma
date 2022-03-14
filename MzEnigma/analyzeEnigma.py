from __future__ import annotations
from typing import Optional, Callable, Dict, List, Tuple, Set

import copy
import random
import itertools
import hashlib
import pdb
from pprint import pprint

import numpy
import networkx

import MzEnigma

class TagesschluesselRange(object):
 """Represents the Tagesschluessel of an Enigma
 
:param enigma: model of the Enigma (required)
:param umkehrwalzenList: 'Umkehrwalze' (if undefined, randomly selected)
:param walzenList: List of type 'Walze' (if undefined, randomly selecte(if undefined, randomly selected)
:param tagesWalzenStellungenList: List of Tageswalzenstellungen (if undefined, all) 
:param zusatzwalzenList: 'Zusatzwalze' (if undefined, randomly selected)
:param blank: replacement character for a blank
:param notify: notification function (e.g. print)
  """
 def __init__(self,
  enigma : Optional[MzEnigma.Enigma] = None,  
  umkehrwalzenList : Optional[List[MzEnigma.Umkehrwalze]] = None, 
  walzenList : Optional[List[MzEnigma.Walze]] = None,
  tagesWalzenStellungenList : Optional[List[str]] = None,
  zusatzwalzenList : Optional[List[MzEnigma.Zusatzwalze]] = None, 
  spruchScoring : Optional[MzEnigma.SpruchScoring] = None, 
  blank : str = '',  
  notify : Optional[Callable[[str], None]] = None) -> None:
  self.notify = notify
  assert enigma, '{}: Enigma required'.format(self.__class__.__name__)
  self.enigma = enigma
  self.blank = blank
  alphabet = self.enigma.alphabet
  if enigma.steckerbrett:
   self.steckerbrett = copy.deepcopy(enigma.steckerbrett)
   self.steckerbrett.notify = self.notify
  else:
   self.steckerbrett = None
  assert walzenList is not None and len(walzenList) > 0, '{}: WalzenRange is required'.format(self.__class__.__name__)
  self.walzenList = list()
  for _walze in walzenList:
   walze = copy.deepcopy(_walze)
   walze.notify = self.notify
   self.walzenList.append(walze)
  if tagesWalzenStellungenList:
   for tagesWalzenStellungen in tagesWalzenStellungenList:
    assert len(tagesWalzenStellungen) == enigma.numberOfWalzen, '{}: Walzenstellung, number of characters must match the number of walzen'.format(self.__class__.__name__)
    assert all(v in alphabet for v in tagesWalzenStellungen), '{}: Walzenstellung, all characters must be in alphabet'.format(self.__class__.__name__)
  else:
   tagesWalzenStellungenList = list(itertools.product(self.enigma.alphabet, repeat = self.enigma.numberOfWalzen))
  self.tagesWalzenStellungenList = copy.deepcopy(tagesWalzenStellungenList )
  self.zusatzwalzenList = list()
  if enigma.zusatzwalzen is not None:
   assert zusatzwalzenList is not None, '{}: zusatzwalzenList is required'.format(self.__class__.__name__)
   for _walze in zusatzwalzenList:
    walze = copy.deepcopy(_walze)
    walze.notify = self.notify
    self.zusatzwalzenList.append(walze)
  assert umkehrwalzenList is not None, '{}: umkehrwalzenList is required'.format(self.__class__.__name__)
  self.umkehrwalzenList = list()
  for _walze in umkehrwalzenList:
   walze = copy.deepcopy(_walze)
   walze.notify = self.notify
   self.umkehrwalzenList.append(walze)
  self.spruchScoring = spruchScoring 
 
 @classmethod
 def rejewskiAttack(cls, catalog : Dict[MzEnigma.Tagesschluessel, List[List[str]]], encodedSpruchSchluessel : str) -> Dict[MzEnigma.Tagesschluessel, str]:
  """Find candidate spruchschluessels for an encrypted SpruchwalzenStellung

:returns: dict of tagesschluessel with the unencoded spruchSchluessel
  """
  assert len(catalog) > 0, '{}.rejewskiAttack: empty catalog detected'.format(cls.__class__.__name__)  
  firstKey, firstItem = catalog.items()[0]
  assert isinstance(firstKey, MzEnigma.Tagesschluesse), '{}.rejewskiAttack: improper catalog key, MzEnigma.Tagesschluessel espected'.format(cls.__class__.__name__)
  assert isinstance(firstItem, list), '{}.rejewskiAttack: improper catalog item, list espected'.format(cls.__class__.__name__)  
  assert 2 * len(firstItem) == len(encodedSpruchSchluessel), '{}.rejewskiAttack: number of positions in catalog item ({}) != number of positions in spruchschluessel ({})'.format(cls.__class__.__name__, len(firstItem), len(encodedSpruchSchluessel) // 2)  
  assert isinstance(firstItem[0], list), '{}.rejewskiAttack: improper catalog item.item, list espected'.format(cls.__class__.__name__)  
  alphabet = firstKey.alphabet
  assert len(firstItem[0]) == len(alphabet), '{}.rejewskiAttack: number of positions in catalog item.item({}) != number of characters ({})'.format(cls.__class__.__name__, len(firstItem[0]), len(alphabet))  
  
  encodedPosKeys = list()
  for first, second in zip(encodedSpruchSchluessel[len(firstItem):], encodedSpruchSchluessel[:len(firstItem)]):
   encodedPosKeys.append(first+second)
   
  validCandidates = dict()
  for tagesschluessel, listOfDoublets in catalog:
   unencodedPosKeys = list()
   for pos, doublets in enumerate(listOfDoublets):
    if encodedPosKeys[pos] not in doublets:
     break
    unencodedPosKeys.append(alphabet[doublets.index(encodedPosKeys[pos])])
   if len(unencodedPosKeys) > 0:
    validCandidates[tagesschluessel] = ''.join(unencodedPosKeys)
   
  return validCandidates

 def createRejewskiCatalog(self) -> Dict[MzEnigma.Tagesschluessel, List[List[str]]]:
  """Build up a catalog of spruchschluessels  

:returns: a list of doublets for every tagesschluessel
  """
  assert self.enigma.steckerbrett is None, '{}.createRejewskiCatalog: engines with steckerbrett are not supported'.format(self.__class__.__name__)
  gTagesschluessel = MzEnigma.Tagesschluessel(enigma = self.enigma, steckerbrett = self.steckerbrett, blank = self.blank, notify = self.notify)
  rejewskiDict = dict()
  for umkehrwalze in self.umkehrwalzenList:
   for walzen in itertools.permutations(self.walzenList, self.enigma.numberOfWalzen):
    for tagesWalzenStellungenTuple in self.tagesWalzenStellungenList:
     tagesWalzenStellungen = ''.join(tagesWalzenStellungenTuple)
     if len(self.zusatzwalzenList) > 0:
      for zusatzwalze in self.zusatzwalzenList:
       tagesschluessel = MzEnigma.Tagesschluessel.changeWalzen(
                                  gTagesschluessel, walzen = walzen, tagesWalzenStellungen = tagesWalzenStellungen, umkehrwalze = umkehrwalze, zusatzwalze = zusatzwalze)
       rejewskiDict[tagesschluessel] = tagesschluessel.findDoublets(first = 0, second = self.enigma.numberOfWalzen, all = True)
     else:
      tagesschluessel = MzEnigma.Tagesschluessel.changeWalzen( 
                                 gTagesschluessel, walzen = walzen, tagesWalzenStellungen = tagesWalzenStellungen, umkehrwalze = umkehrwalze)
      rejewskiDict[tagesschluessel] = tagesschluessel.findDoublets(first = 0, second = self.enigma.numberOfWalzen, all = True)
  return rejewskiDict

 def turingAttack(self, encodedSpruch : str = '', crib : str = '', startingPosition : int = 0) -> List[Tuple[MzEnigma.Tagesschluessel, List[Tuple[str, str]]]]:
  """Turing attack to derive settings for Umkehrwalze, Walzen, Zusatzwalze, Tageswalzenstellungen and several settings of the Steckerbrett
An engine with Steckerbrett is required.

:param encodedSpruch: encoded message to be attacked (required)
:param crib: unencoded crib to be found in the message (required) 
:param startingPosition: starting position of the crib in the message
:return: List[Tuple[Tagesschluessel, List[Tuple[Walzenstellungen, Steckerbrett.wiring]]]]
  """
  def connectBus(id : int, v : str) -> bool:
   '''Heart of the turing bomb - the bus is restricted to the ONE active line with a character
   
   :param id: bus to be used
   :param v: input value
   :return: boolean indicating success
   '''
   nonlocal graph, ecList, buses
   if buses[id] is None:
    buses[id] = v
    vID = self.enigma.alphabet.index(v)
    for tgtID in graph.neighbors(id):
     for _, posDict in graph[id][tgtID].items():
      pos = posDict['pos']
      tgtV = ecList[vID][pos]
      # if self.notify:
      #  self.notify('{}.turingAttack: id = {}, v = {} -> pos = {} -> tgtID = {}, tgtV = {}'.format(self.__class__.__name__, id, v, pos, tgtID, tgtV))
      if not connectBus(tgtID, tgtV):
       return False
    return True
   else:
    return buses[id] == v
   
  def getValidWalzenStellungen(tagesschluessel : MzEnigma.Tagesschluessel) -> List[Tuple[str, List[Dict[str, str]]]]: 
   nonlocal ecList, buses, firstBus, spruchLen, graph
   if self.notify:
    self.notify('{}.turingAttack: \n{}'.format(self.__class__.__name__, tagesschluessel))
   oldTagesWalzenStellungen = tagesschluessel.tagesWalzenStellungen
   candidateSteckerbrettList = list()
   for tagesWalzenStellungenID, tagesWalzenStellungenTuple in enumerate(self.tagesWalzenStellungenList):
    knownWirings = list()
    tagesschluessel.tagesWalzenStellungen = ''.join(tagesWalzenStellungenTuple)
    if self.notify:
     self.notify('{}.turingAttack: examining tagesWalzenStellungen = {} ({} of {})'.format(self.__class__.__name__, tagesschluessel.tagesWalzenStellungen, tagesWalzenStellungenID,  len(self.tagesWalzenStellungenList)))
    ecList = list()
    for nc, c in enumerate(self.enigma.alphabet):
     ecList.append(list())
     for cs in tagesschluessel.encode(spruchLen * c):
      ecList[-1].append(cs)
    
    for v in self.enigma.alphabet:
     if self.notify:
       self.notify('{}.turingAttack: examining {}'.format(self.__class__.__name__, v))
     buses = len(self.enigma.alphabet) * [ None ]
     if connectBus(firstBus, v):
      knownWiring = dict()
      for n, id in enumerate(buses):
       if id is not None:
        knownWiring[self.enigma.alphabet[n]] = id
      keys = list(knownWiring.keys())
      for key in keys:
       value = knownWiring[key]
       if value not in keys:
        knownWiring[value] = key
      knownWirings.append(knownWiring)
      if self.notify:
       self.notify('{}.turingAttack: wiring {} found'.format(self.__class__.__name__, knownWiring))
     candidateSteckerbrettList.append((tagesschluessel.tagesWalzenStellungen, knownWirings))
   tagesschluessel.tagesWalzenStellungen = oldTagesWalzenStellungen
   return candidateSteckerbrettList

  assert self.enigma.steckerbrett is not None, '{}.turingAttack: engines without steckerbrett are not supported'.format(self.__class__.__name__)
  posList = MzEnigma.Enigma.validCribPositions(encodedSpruch, crib)
  assert startingPosition in posList, '{}.turingAttack: {} is not a valid starting position, use in {}'.format(self.__class__.__name__, startingPosition, posList)
  encodedSpruch = encodedSpruch[startingPosition:]
  ecList = list()
  buses = list()
  
  # We need to use a MultiGraph, since the menu may contain duplicate edges (with different positions) 
  graph = networkx.MultiGraph()

  for pos, cc in enumerate(crib):
   icc = self.enigma.alphabet.index(cc)
   iec = self.enigma.alphabet.index(encodedSpruch[pos])
   graph.add_edge(icc, iec, pos = pos)
  firstBus = sorted(graph.adjacency(), key = lambda item: len(item[1]), reverse = True)[0][0]
 
  spruchLen = len(crib)
  encodedSpruch = encodedSpruch[:spruchLen]
  
  gTagesschluessel = MzEnigma.Tagesschluessel(enigma = self.enigma, 
                                                                 steckerbrett = copy.deepcopy(MzEnigma.UnconnectedSteckerbrett), 
                                                                 tagesWalzenStellungen = self.enigma.numberOfWalzen * 'A', 
                                                                 blank = self.blank, notify = None)
  validCandidates = list()
  for umkehrwalze in self.umkehrwalzenList:
   for walzen in itertools.permutations(self.walzenList, self.enigma.numberOfWalzen):
    if len(self.zusatzwalzenList) > 0:
     for zusatzwalze in self.zusatzwalzenList:
      tagesschluessel = MzEnigma.Tagesschluessel.changeWalzen(
                                 gTagesschluessel, walzen = walzen, tagesWalzenStellungen = gTagesschluessel.tagesWalzenStellungen, 
                                 umkehrwalze = umkehrwalze, zusatzwalze = zusatzwalze)
      candidateSteckerbrettList = getValidWalzenStellungen(tagesschluessel)
      if len(candidateSteckerbrettList) > 0:
       validCandidates.append((copy.deepcopy(tagesschluessel), candidateSteckerbrettList))
    else:
     tagesschluessel = MzEnigma.Tagesschluessel.changeWalzen( 
                                gTagesschluessel, walzen = walzen, tagesWalzenStellungen = gTagesschluessel.tagesWalzenStellungen, umkehrwalze = umkehrwalze)
     candidateSteckerbrettList = getValidWalzenStellungen(tagesschluessel)
     if len(candidateSteckerbrettList) > 0:
      validCandidates.append((copy.deepcopy(tagesschluessel), candidateSteckerbrettList))
  return validCandidates
  
 def gilloglyAttackPhase1(self, encodedSpruch : str) -> MzEnigma.Tagesschluessel:
  """Brute force attack to derive settings for Umkehrwalze, Walzen, Zusatzwalze, and Tageswalzenstellungen
 
:param encodedSpruch: message to be attacked (required)
:return: Tagesschlüssel
  """
  def doScoring():
   nonlocal encodedSpruch, bestScore, tagesschluessel, bestTagesschluessel, lastDecryptedSpruch
   decryptedSpruch = tagesschluessel.decode(encodedSpruch)
   actScore = MzEnigma.SpruchScoring.indexOfCoincidence(decryptedSpruch)
   decryptedSpruchMD5 = hashlib.md5(str(decryptedSpruch).encode("utf-8")).hexdigest()
   if self.notify:
    self.notify('{}.gilloglyAttackPhase1: score = {}(best: {})\n md5 = {}\n{}\n'.format(
      self.__class__.__name__, actScore, bestScore, decryptedSpruchMD5, tagesschluessel))
   lastDecryptedSpruch = decryptedSpruch
   if actScore > bestScore:
    bestScore = actScore
    bestTagesschluessel = copy.deepcopy(tagesschluessel)
   
  lastDecryptedSpruch = ''
  gTagesschluessel = MzEnigma.Tagesschluessel(enigma = self.enigma, steckerbrett = self.steckerbrett, blank = self.blank, notify = self.notify)
  bestTagesschluessel = None
  bestScore = 0
  for umkehrwalze in self.umkehrwalzenList:
   for walzen in itertools.permutations(self.walzenList, self.enigma.numberOfWalzen):
    for tagesWalzenStellungenTuple in self.tagesWalzenStellungenList:
     tagesWalzenStellungen = ''.join(tagesWalzenStellungenTuple)
     if len(self.zusatzwalzenList) > 0:
      for zusatzwalze in self.zusatzwalzenList:
       tagesschluessel = MzEnigma.Tagesschluessel.changeWalzen(
                                  gTagesschluessel, walzen = walzen, tagesWalzenStellungen = tagesWalzenStellungen, umkehrwalze = umkehrwalze, zusatzwalze = zusatzwalze)
       doScoring()
     else:
      tagesschluessel = MzEnigma.Tagesschluessel.changeWalzen( 
                                 gTagesschluessel, walzen = walzen, tagesWalzenStellungen = tagesWalzenStellungen, umkehrwalze = umkehrwalze)
      doScoring()
  return bestTagesschluessel

 def shotgunPhase2(self, 
   phase1Tagesschluessel : MzEnigma.Tagesschluessel, encodedSpruch : str = '', noImprovement : int = 10) -> MzEnigma.Tagesschluessel:
  """Shotgun hill climbing or simulated annealing attack to derive settings for Steckerbrett
 
:param phase1Tagesschluessel: tagesschluessel with correct settings for Umkehrwalze, Walzen, Zusatzwalze, and Tageswalzenstellungen(required)
:param encodedSpruch: encrypted message to be attacked (required)
:param noImprovement: stop condition after *noImprovement* number of attempts in a cycle
:return: Tagesschlüssel
  """
  def fillWired(tagesschluessel):
   wired = set()
   unwired = set()
   for n, c in enumerate(tagesschluessel.alphabet):
    if tagesschluessel.steckerbrett.wiring[n] != c:
     wired.add(c)
    else:
     unwired.add(c)
   return wired, unwired

  assert self.spruchScoring is not None, '{}.shotgunPhase2: self.spruchScoring is required'.format(self.__class__.__name__)
  assert phase1Tagesschluessel.steckerbrett is not None, '{}.gilloglyAttackPhase2: steckerbrett is required'.format(self.__class__.__name__)
  wired,  unwired = fillWired(phase1Tagesschluessel)
  if len(wired) <= 2:
   return phase1Tagesschluessel
  assert len(unwired) > 2, '{}.shotgunPhase2: steckerbrett with > 0 unconnected pins required'.format(self.__class__.__name__)
  tagesschluessel = copy.deepcopy(phase1Tagesschluessel)

  notImproved = 0
  bestScore = 0
  while notImproved < noImprovement:
   actScore = self.spruchScoring.newNgramScore(tagesschluessel.decode(encodedSpruch), bestScore, tagesschluessel.alphabet)
   if actScore >= bestScore:
    if actScore > bestScore:
     notImproved = -1
    bestScore = actScore
    bestWired = copy.deepcopy(wired)
    bestUnwired = copy.deepcopy(unwired)
    bestWiring = tagesschluessel.steckerbrett.wiring
    if self.notify:
     self.notify('{}.shotgunPhase2: bestScore = {}\n{}\n'.format(
      self.__class__.__name__, bestScore, tagesschluessel))
   else:
    tagesschluessel.steckerbrett.wiring = bestWiring
    wired = copy.deepcopy(bestWired)
    unwired = copy.deepcopy(bestUnwired)
   notImproved += 1
   unconnectSrc = random.choice(list(wired))
   connectSrc = random.choice(list(unwired))
   unwired.remove(connectSrc)
   unwired.add(unconnectSrc)
   connectTgt = random.choice(list(unwired))
   tagesschluessel.steckerbrett.clearMark3Setting(unconnectSrc)
   tagesschluessel.steckerbrett.addMark3Setting(connectSrc, connectTgt)
   wired,  unwired = fillWired(tagesschluessel)
  return tagesschluessel

 def exchangePhase2(self, 
   phase1Tagesschluessel : MzEnigma.Tagesschluessel, encodedSpruch : str = '', cycles : int = 5) -> MzEnigma.Tagesschluessel:
  """Hill climbing based on exchange of x-connected ports of a steckerbrett
 
:param phase1Tagesschluessel: tagesschluessel with correct settings for Umkehrwalze, Walzen, Zusatzwalze, and Tageswalzenstellungen(required)
:param encodedSpruch: encrypted message to be attacked (required)
:param cycles: number of exchange cycles
:return: Tagesschlüssel
  """
  assert self.spruchScoring is not None, '{}.exchangePhase2: self.spruchScoring is required'.format(self.__class__.__name__)
  assert phase1Tagesschluessel.steckerbrett is not None, '{}.gilloglyAttackPhase2: steckerbrett is required'.format(self.__class__.__name__)
  tagesschluessel = copy.deepcopy(phase1Tagesschluessel)
  wired = set()
  for n, c in enumerate(tagesschluessel.alphabet):
   if tagesschluessel.steckerbrett.wiring[n] != c:
    wired.add(c)
  if len(wired) <= 2:
   return phase1Tagesschluessel
  bestWiring = tagesschluessel.steckerbrett.wiring
  bestScore = self.spruchScoring.ngramScore(tagesschluessel.decode(encodedSpruch), validChars = tagesschluessel.alphabet)
  for cycle in range(cycles):
   frequencyDict = tagesschluessel.frequencyDict(encodedSpruch, decode = True)
   for freq in sorted(frequencyDict.keys(), reverse = True):
    for c1, _ in frequencyDict[freq]:
     if c1 in wired:
      c1Index = tagesschluessel.steckerbrett.wiring.index(c1)
      if c1 != tagesschluessel.alphabet[c1Index]: 
       for c2 in wired:
        c2Index = tagesschluessel.steckerbrett.wiring.index(c2)
        if c2 != c1 and c2 != tagesschluessel.alphabet[c2Index]:
         actWiring = tagesschluessel.steckerbrett.wiring
         tagesschluessel.steckerbrett.exchangeMark3Setting(c1, c2)
         actScore = self.spruchScoring.ngramScore(tagesschluessel.decode(encodedSpruch), validChars = tagesschluessel.alphabet)
         if actScore > bestScore:
          bestScore = actScore
          bestWiring = tagesschluessel.steckerbrett.wiring
          if self.notify:
           self.notify('{}.exchangePhase2: cycle {}, exchanging {} <-> {}, score = {}'.format(self.__class__.__name__, cycle + 1, c1, c2, bestScore))
        tagesschluessel.steckerbrett.wiring = actWiring
   tagesschluessel.steckerbrett.wiring = bestWiring
  tagesschluessel.steckerbrett.wiring = bestWiring
  return tagesschluessel

 def gilloglyAttackPhase2(self, 
   phase1Tagesschluessel : MzEnigma.Tagesschluessel, encodedSpruch : str = '', 
      noImprovement : int = 10, cycles : int = 1000,  useSimulatedAnnealing : bool = False) -> MzEnigma.Tagesschluessel:
  """Shotgun hill climbing or simulated annealing attack to derive settings for Steckerbrett
 
:param phase1Tagesschluessel: tagesschluessel with correct settings for Umkehrwalze, Walzen, Zusatzwalze, and Tageswalzenstellungen(required)
:param encodedSpruch: encrypted message to be attacked (required)
:param noImprovement: stop condition after *noImprovement* number of attempts in a cycle
:param cycles: number of cycles with a random steckerbrett configuration
:param useSimulatedAnnealing: use simulated annealing instead of conventional hill climbing
:return: Tagesschlüssel
  """

  if useSimulatedAnnealing:
   self.spruchScoring.setSATemperature(encodedSpruch)
  else:
   self.spruchScoring.setSATemperature('')
  bestScore = 0
  tagesschluessel = copy.deepcopy(phase1Tagesschluessel)
  bestWiring = tagesschluessel.steckerbrett.wiring
  
  for cycle in range(cycles):
   tagesschluessel = self.shotgunPhase2(self, tagesschluessel, encodedSpruch,  noImprovement)
   actScore = self.spruchScoring.newNgramScore(tagesschluessel.decode(encodedSpruch), bestScore, tagesschluessel.alphabet)
   if actScore > bestScore:
    bestScore = actScore
    bestWiring = tagesschluessel.steckerbrett.wiring
   newSteckerbrett = MzEnigma.Steckerbrett.Mark_3(alphabet = tagesschluessel.alphabet)
   tagesschluessel.steckerbrett.wiring = newSteckerbrett.wiring
  tagesschluessel.steckerbrett.wiring = bestWiring
  return tagesschluessel

 def mzAttackPhase2(self, phase1Tagesschluessel : MzEnigma.Tagesschluessel, encodedSpruch : str = '') -> MzEnigma.Tagesschluessel:
  """Systematic hill climbing attack to derive settings for Steckerbrett
 
:param phase1Tagesschluessel: tagesschluessel with correct settings for Umkehrwalze, Walzen, Zusatzwalze, and Tageswalzenstellungen(required)
:param encodedSpruch: encrypted message to be attacked (required)
:return: Tagesschlüssel
  """
  assert self.spruchScoring is not None, '{}.mzAttackPhase2: self.spruchScoring is required'.format(self.__class__.__name__)
  assert phase1Tagesschluessel.steckerbrett is not None, '{}.mzAttackPhase2: steckerbrett is required'.format(self.__class__.__name__)
  tagesschluessel = copy.deepcopy(phase1Tagesschluessel)
  nConnections = 0
  for n, c in enumerate(tagesschluessel.alphabet):
   if tagesschluessel.steckerbrett.wiring[n] != c:
    nConnections += 1
  nConnections = nConnections // 2
  assert nConnections > 0, '{}.mzAttackPhase2: at least one connection in steckerbrett required'.format(self.__class__.__name__)
  tagesschluessel.steckerbrett.wiring = tagesschluessel.alphabet
  monograms = sorted(self.spruchScoring.ngramDict[1].items(), key = lambda c2s: c2s[1], reverse = False)
  assert len(monograms) > 2*nConnections, '{}.mzAttackPhase2: len(monograms) = {} > 2*nConnections = {}'.format(self.__class__.__name__, len(monograms), 2*nConnections)
  initialScore = self.spruchScoring.ngramScore(tagesschluessel.decode(encodedSpruch), 1, validChars = tagesschluessel.alphabet)
  unwired = list(tagesschluessel.alphabet)
  self.spruchScoring.numberOfChars = 1
  connectedChars = ''
  connection = 0
  while connection < nConnections and len(unwired) > 1:
   connectTgt = monograms.pop()[0]
   connectedChars += connectTgt
   if connectTgt not in unwired:
    continue
   maxScore = 0
   maxN = -1
   wiring = tagesschluessel.steckerbrett.wiring
   for n, connectSrc in enumerate(unwired):
    tagesschluessel.steckerbrett.wiring = wiring
    if connectSrc != connectTgt:
     tagesschluessel.steckerbrett.addMark3Setting(connectSrc, connectTgt)
    decodedSpruch = tagesschluessel.decode(encodedSpruch)
    if True:
     actScore = self.spruchScoring.ngramScore(decodedSpruch, 1, validChars = connectedChars)
    else:
     actScore = MzEnigma.SpruchScoring.indexOfCoincidence(decodedSpruch)
    if actScore > maxScore:
     maxScore = actScore
     maxN = n
   tagesschluessel.steckerbrett.wiring = wiring
   connectSrc = unwired[maxN]
   unwired.pop(unwired.index(connectSrc))
   if self.notify:
    self.notify('{}.mzAttackPhase2: connecting {} -> {}, diffScore = {}'.format(self.__class__.__name__, connectSrc, connectTgt, maxScore))
   if connectSrc != connectTgt:
    tagesschluessel.steckerbrett.addMark3Setting(connectSrc, connectTgt)
    unwired.pop(unwired.index(connectTgt))
    connection += 1
  if self.notify:
   finalScore = self.spruchScoring.ngramScore(tagesschluessel.decode(encodedSpruch), 1, validChars = tagesschluessel.alphabet)
   self.notify('{}.mzAttackPhase2: score {} -> {}'.format(self.__class__.__name__, initialScore, finalScore))
  return tagesschluessel
