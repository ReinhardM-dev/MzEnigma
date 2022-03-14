
from typing import Optional, Callable, Dict, List, Tuple, Set
import pytest

import itertools
import re
import random
import string
import MzEnigma

defaultMsg = 'DIEENIGMAISTEINEROTORSCHLUESSELMASCHINEDIEIMZWEITENWELTKRIEGZURVERSCHLUESSELUNGDESNACHRICHTENVERKEHRSDERWEHRMACHTVERWENDETWURDEXAUCHPOLIZEIGEHEIMDIENSTEDIPLOMATISCHEDIENSTESDSSREICHSPOSTUNDREICHSBAHNSETZTENSIEZURGEHEIMENKOMMUNIKATIONEINXTROTZMANNIGFALTIGERVORUNDWAEHRENDDESKRIEGESEINGEFUEHRTERVERBESSERUNGENDERVERSCHLUESSELUNGSQUALITAETGELANGESDENALLIIERTENMITHOHEMPERSONELLENUNDMASCHINELLENAUFWANDDIEDEUTSCHENFUNKSPRUECHENAHEZUKONTINUIERLICHZUENTZIFFERNX'
defaultCrib = 'DIEENIGMAISTEINEROTORSCHLUESSELMASCHINE'

def printFrequencyDict(enigmaSetting : MzEnigma.Tagesschluessel, spruchScoring : MzEnigma.SpruchScoring, actMsg : str) -> None:
 frequencyDict = enigmaSetting.frequencyDict(actMsg)
 for freq in sorted(frequencyDict.keys(), reverse = True):
  msg = ' {} : '.format(freq)
  for c2l in frequencyDict[freq]:
   msg += c2l[0]
  print(msg)
 print(' score = {}'.format(round(spruchScoring.ngramScore(actMsg, 1, validChars = enigmaSetting.alphabet), 3)))

def compareSteckerbrett(phase2EnigmaSetting : MzEnigma.Tagesschluessel, expectedEnigmaSetting : MzEnigma.Tagesschluessel) -> str:
  validResultWiring = ''
  for p2C, eC in zip(phase2EnigmaSetting.steckerbrett.wiring, expectedEnigmaSetting.steckerbrett.wiring):
   if p2C == eC:
    validResultWiring += eC
   else:
    validResultWiring += '.'
  return validResultWiring

def runTuringAttack(enigma : MzEnigma.enigma, name : str, msg : Optional[str] = None, crib : Optional[str] = None, notify : Optional[Callable[[str], None]] = None):
 assert enigma.steckerbrett is not None
 if crib is None:
  crib = msg
 print('Starting engine {}'.format(name))
 if enigma.zusatzwalzen is not None:
  zusatzwalze = enigma.zusatzwalzen[0]
 else:
  zusatzwalze = None
  
 enigmaSetting = MzEnigma.Tagesschluessel(enigma, 
                                                            umkehrwalze = enigma.umkehrwalzen[0], 
                                                            walzen = enigma.walzen[:enigma.numberOfWalzen], 
                                                            tagesWalzenStellungen = 'RHM', 
                                                            steckerbrett = MzEnigma.Steckerbrett('Mark 3', 'ARDCEFTIHXPSVQOKNBLGUMYJWZ'), 
                                                            zusatzwalze = zusatzwalze, 
                                                            notify = None)
 # RVDEAHEJX
 sRange = MzEnigma.TagesschluesselRange(enigma, 
  walzenList = enigmaSetting.walzen, 
  tagesWalzenStellungenList = [enigmaSetting.tagesWalzenStellungen], 
  umkehrwalzenList = [enigmaSetting.umkehrwalze], 
  zusatzwalzenList = [enigmaSetting.zusatzwalze], 
  spruchScoring = None, 
  notify = None) 
 sRange.notify = notify
 eMsg = enigmaSetting.encode(msg)
 steckerbrettWiring = enigmaSetting.steckerbrett.wiringToDict(False)
 print('text = {}'.format(msg))
 print('crib = {}'.format(crib))
 print('encryptedText = {}'.format(eMsg))
 validCandidates = sRange.turingAttack(encodedSpruch = eMsg, crib = crib, startingPosition = msg.find(crib))
 for tagesschluessel, tws2wiringList in validCandidates:
  print('-----------------\n{}'.format(tagesschluessel))
  for tws, wirings in tws2wiringList:
   print(' tws = {} ++++++++++++++++++++++++'.format(tws))
   for wiring in wirings:
    difference = 'none'
    for src, tgt in steckerbrettWiring.items():
     if src not in wiring:
      difference = 'missing key'
     else:
      assert wiring[src] != tgt, 'improper key {} found ({} expected)'.format(wiring[src], tgt)
    print(' + {}: {}'.format(difference, wiring))

def test_turingAttack(pytestconfig):
 global defaultMsg, defaultCrib
 msg = pytest.helpers.message(pytestconfig)
 if not msg:
  msg = defaultMsg
  crib = defaultCrib
 else:
  crib = None 
  
 pattern = pytestconfig.getoption('component')
 if pattern:
  print('\n--- test_turingAttack ---\n')
  for name, enigma in vars(MzEnigma).items():
   if isinstance(enigma, MzEnigma.Enigma) and re.fullmatch(pattern, name) and enigma.steckerbrett is not None:
    runTuringAttack(enigma, name, msg, crib, 
                           notify = pytest.helpers.notify(pytestconfig))
  
def runGilloglyAttack(enigma : MzEnigma.Enigma, name : str, msg : str, phase2Method : str = 'Mz', notify : Optional[Callable[[str], None]] = None):
 assert enigma.steckerbrett is not None
 print('Starting engine {}'.format(name))
 enigmaSetting = MzEnigma.Tagesschluessel(enigma, notify = notify)
 spruchScoring = MzEnigma.SpruchScoring('german', normalize = True, logarithmic = False) 
 eMsg = enigmaSetting.encode(msg)
 print('text = {}'.format(msg))
 print('encryptedText = {}'.format(eMsg))
 print('frequencyDict:')
 printFrequencyDict(enigmaSetting, spruchScoring, msg)
 sRange = MzEnigma.TagesschluesselRange(enigma, 
  walzenList = enigmaSetting.walzen, 
  tagesWalzenStellungenList = None, 
  umkehrwalzenList = [enigmaSetting.umkehrwalze], 
  zusatzwalzenList = [enigmaSetting.zusatzwalze], 
  spruchScoring = spruchScoring, 
  notify = notify) 
 phase1EnigmaSetting = sRange.gilloglyAttackPhase1(eMsg)
 phase1Msg = 'phase 1 analysis of settings - Umkehrwalze, Walzen, Zusatzwalze, and Tageswalzenstellungen -'
 if phase1EnigmaSetting != enigmaSetting:
  print('{} of {} failed'.format(phase1Msg, name))
  print('{}\nexpected = \n{}'.format(name, enigmaSetting))
  print('{}\nderived = \n{}'.format(name, phase1EnigmaSetting))
  return
 print('{} succeeded'.format(phase1Msg))
 print('frequencyDict after phase 1:')
 printFrequencyDict(phase1EnigmaSetting, spruchScoring, phase1EnigmaSetting.decode(eMsg))
 if phase2Method == 'Mz':
  phase2EnigmaSetting = sRange.mzAttackPhase2(phase1EnigmaSetting, encodedSpruch = eMsg)
 else:
  phase2EnigmaSetting = sRange.gilloglyAttackPhase2(phase1EnigmaSetting, encodedSpruch = eMsg, noImprovement = 10, cycles = 1000,  useSimulatedAnnealing = False)
 phase2Msg = 'phase 1 analysis of settings - Steckerbrett -'
 if phase2EnigmaSetting.steckerbrett == enigmaSetting.steckerbrett:
  print('{} of {} succeeded'.format(phase2Msg, name))
  return
 print('{} not succeeded, steckerbrett comparison = {}'.format(phase2Msg, compareSteckerbrett(phase2EnigmaSetting, enigmaSetting)))
 if phase2Method == 'Mz':
  print(' ... trying fixes')
  phase2EnigmaSettingNew = sRange.exchangePhase2(phase2EnigmaSetting, encodedSpruch = eMsg)
  print('{} still not succeeded, steckerbrett comparison = {}'.format(phase2Msg, compareSteckerbrett(phase2EnigmaSettingNew, enigmaSetting)))
  if phase2EnigmaSettingNew.steckerbrett == enigmaSetting.steckerbrett:
   print('{} of {} succeeded with fixes'.format(phase2Msg, name))
   return
  decodedMsg = phase2EnigmaSettingNew.decode(eMsg)
 else:
  decodedMsg = phase2EnigmaSetting.decode(eMsg)
 print('Message:\n{} (expected) \n{} (got)'.format(msg, decodedMsg))

def test_gilloglyAttack(pytestconfig):
 msg = pytest.helpers.message(pytestconfig)
 if not msg:
  msg = defaultMsg
 pattern = pytestconfig.getoption('component')
 phase2Method = 'Mz'
 if pattern:
  print('\n--- test_gilloglyAttack ---\n')
  for name, enigma in vars(MzEnigma).items():
   if isinstance(enigma, MzEnigma.Enigma) and re.fullmatch(pattern, name) and enigma.steckerbrett is not None:
    runGilloglyAttack(enigma, name, msg, 
                           phase2Method = phase2Method,  
                           notify = pytest.helpers.notify(pytestconfig))

def runRejewskiAttack(enigma : MzEnigma.Enigma, name : str, notify : Optional[Callable[[str], None]] = None):
 assert enigma.steckerbrett is None
 print('Starting engine {}'.format(name))
 enigmaSetting = MzEnigma.Tagesschluessel(enigma, notify = notify)
 msg = itertools.permutations(enigma.alphabet, len(enigma.numberOfWalzenStellungen()))
 eMsg = enigmaSetting.encode(msg +  msg)
 print('encryptedText = {}'.format(eMsg))
 sRange = MzEnigma.TagesschluesselRange(enigma, 
  walzenList = enigmaSetting.walzen, 
  tagesWalzenStellungenList = None, 
  umkehrwalzenList = [enigmaSetting.umkehrwalze], 
  zusatzwalzenList = [enigmaSetting.zusatzwalze], 
  spruchScoring = None, 
  notify = notify) 
 catalog = sRange.createRejewskiCatalog()
 validCandidates = sRange.rejewskiAttack(catalog, eMsg)
 assert enigmaSetting in validCandidates
 assert validCandidates[enigmaSetting] == msg

def test_rejewskiAttack(pytestconfig):
 pattern = pytestconfig.getoption('component')
 if pattern:
  print('\n--- test_gilloglyAttack ---\n')
  for name, enigma in vars(MzEnigma).items():
   if isinstance(enigma, MzEnigma.Enigma) and re.fullmatch(pattern, name) and enigma.steckerbrett is None:
    runRejewskiAttack(enigma, name, notify = pytest.helpers.notify(pytestconfig))
                            
if __name__ == "__main__":
 import difflib
 match = difflib.SequenceMatcher(None,'abcd','yycy')
 matchResult = list(match.find_longest_match(0, 4, 0, 4))
 # msg = 'DIEENIGMAISTEINEROTORSCHLUESSELMASCHINEDIEIMZWEITENWELTKRIEGZURVERSCHLUESSELUNGDESNACHRICHTENVERKEHRSDERWEHRMACHTVERWENDETWURDEXAUCHPOLIZEIGEHEIMDIENSTEDIPLOMATISCHEDIENSTESDSSREICHSPOSTUNDREICHSBAHNSETZTENSIEZURGEHEIMENKOMMUNIKATIONEINXTROTZMANNIGFALTIGERVORUNDWAEHRENDDESKRIEGESEINGEFUEHRTERVERBESSERUNGENDERVERSCHLUESSELUNGSQUALITAETGELANGESDENALLIIERTENMITHOHEMPERSONELLENUNDMASCHINELLENAUFWANDDIEDEUTSCHENFUNKSPRUECHENAHEZUKONTINUIERLICHZUENTZIFFERNX'
 # msg = 'DIEENIGMAISTEINEROTORSCHLUESSELMASCHINE'
 msg = "OBERKOMMANDODERWEHRMACHTOBERKOMMANDODERWEHRMACHTOBERKOMMANDODERWEHRMACHT"
 #          'XLNFCBYXCWGAOWURKQJDUBNRQWWXVIKIMPLYQAGFCVUEUZCINVQYSAWLIFEXAAKSPETAJXIY'
 enigma = MzEnigma.Enigma_M3
 name = 'Enigma_M3'
 print('plaintext = {}'.format(msg))
 if True:
  # crib = 'NIGMAISTEINEROTORSCHLUESSELMASCHINEDIE'
  crib = msg[:12]
  runTuringAttack(enigma, name, msg, crib = crib, notify = None)
 else:
  phase2Method = 'Mz'
  runGilloglyAttack(enigma, name, msg, phase2Method = phase2Method, notify = None)
 if False:
  oldScore = 0
  for l in range(3, len(actMsg)):
   msg = ''.join(random.choices(string.ascii_uppercase, k=l))
   T = spruchScoring.setSATemperature(msg)
   score = spruchScoring.newNgramScore(msg, oldScore)
   if score > oldScore:
    print('{}, {}, {} -> {}'.format(l, T, oldScore, score))
    oldScore = score
