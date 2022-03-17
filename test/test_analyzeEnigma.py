
from typing import Optional, Callable, Dict, List, Tuple, Set
import pytest

import itertools
import os, os.path
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
                                                            tagesWalzenStellungen = ''.join(random.sample(enigma.alphabet, enigma.numberOfWalzen)), 
                                                            steckerbrett = MzEnigma.Steckerbrett('Mark 3', 'ARDCEFTIHXPSVQOKNBLGUMYJWZ'), 
                                                            zusatzwalze = zusatzwalze, 
                                                            notify = None)
 # RVDEAHEJX
 sRange = MzEnigma.TagesschluesselRange(enigma, 
  walzenList = [enigmaSetting.walzen], 
  tagesWalzenStellungenList = [enigmaSetting.tagesWalzenStellungen], 
  umkehrwalzenList = [enigmaSetting.umkehrwalze], 
  zusatzwalzenList = [enigmaSetting.zusatzwalze], 
  spruchScoring = None, 
  notify = None) 
 sRange.notify = notify
 print(enigmaSetting)
 eMsg = enigmaSetting.encode(msg)
 steckerbrettWiring = enigmaSetting.steckerbrett.wiringToDict(False)
 print('text = {}'.format(msg))
 print('crib = {}'.format(crib))
 print('encryptedText = {}'.format(eMsg))
 validCandidates = sRange.turingAttack(encodedSpruch = eMsg, crib = crib, startingPosition = msg.find(crib))
 for tagesschluessel, tws2wiringList in validCandidates:
  print('-----------------\n{}'.format(tagesschluessel))
  for tws, wirings in tws2wiringList:
   print(' - tws = {} ++++++++++++++++++++++++'.format(tws))
   for wiring in wirings:
    missingKeys = list()
    improperKeys = list()
    difference = 'correct'
    for src, tgt in steckerbrettWiring.items():
     if src not in wiring and difference == 'correct':
      missingKeys.append(src)
      difference = 'missing keys'
     elif src in wiring and wiring[src] != tgt:
      improperKeys.append(src)
      difference = 'improper keys'
    if difference == 'missing keys':
     print('  + {}: {}'.format(difference, sorted(missingKeys)))
    elif difference == 'correct':
     print('  + {}'.format(difference))
    elif difference == 'improper keys' and notify:
     print('  + {}: {}'.format(difference, sorted(improperKeys)))

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
 enigmaSetting = MzEnigma.Tagesschluessel(enigma, notify = None)
 print(enigmaSetting)
 spruchScoring = MzEnigma.SpruchScoring('german', normalize = True, logarithmic = False) 
 eMsg = enigmaSetting.encode(msg)
 print('text = {}'.format(msg))
 print('encryptedText = {}'.format(eMsg))
 print('frequencyDict:')
 printFrequencyDict(enigmaSetting, spruchScoring, msg)
 sRange = MzEnigma.TagesschluesselRange(enigma, 
  walzenList = [enigmaSetting.walzen], 
  tagesWalzenStellungenList = None, 
  umkehrwalzenList = [enigmaSetting.umkehrwalze], 
  zusatzwalzenList = [enigmaSetting.zusatzwalze], 
  spruchScoring = spruchScoring, 
  notify = None) 
 sRange.notify = notify
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

def runRejewskiAttack(enigma : MzEnigma.Enigma, name : str, usePickleFile : bool = True, notify : Optional[Callable[[str], None]] = None):
 assert enigma.steckerbrett is None
 print('Starting engine {}'.format(name))
 enigmaSetting = MzEnigma.Tagesschluessel(enigma, 
   walzen = enigma.walzen[:enigma.numberOfWalzen], 
   umkehrwalze = enigma.umkehrwalzen[0], notify = None)
 print(enigmaSetting)
 msg = ''.join(random.sample(enigma.alphabet, enigma.numberOfWalzen))
 eMsg = enigmaSetting.encode(msg +  msg)
 print('spruchschluessel = {}'.format(msg))
 print('encryptedText = {}'.format(eMsg))
 sRange = MzEnigma.TagesschluesselRange(enigma, 
  walzenList = [enigmaSetting.walzen], 
  tagesWalzenStellungenList = None, 
  umkehrwalzenList = [enigmaSetting.umkehrwalze], 
  zusatzwalzenList = [enigmaSetting.zusatzwalze], 
  spruchScoring = None, 
  notify = None) 
 sRange.notify = notify
 pickleFile = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'rejewskiCatalog.pickle')
 if usePickleFile and os.path.exists(pickleFile):
  catalog = sRange.loadRejewskiCatalog(pickleFile)
 else:
  if os.path.exists(pickleFile):
   os.remove(pickleFile)
  catalog = sRange.createRejewskiCatalog(pickleFile)
 validCandidates = sRange.rejewskiAttack(catalog, eMsg)
 print('Computation finished, {} candidates found'.format(len(validCandidates)))
 for setting, spruchschluessel in validCandidates:
  found = list()
  if setting == enigmaSetting:
   found.append('setting correct')
  if spruchschluessel == msg:
   found.append('spruchschluessel correct')
  found = ', '.join(found)
  if len(found) == 0:
   found = 'improper'
  print('tagesWalzenStellungen = {}, spruchschluessel = {} -> {} '.format(setting.tagesWalzenStellungen, spruchschluessel, found))

def test_rejewskiAttack(pytestconfig):
 pattern = pytestconfig.getoption('component')
 if pattern:
  print('\n--- test_rejewskiAttack ---\n')
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
 print('plaintext = {}'.format(msg))
 if False:
  # crib = 'NIGMAISTEINEROTORSCHLUESSELMASCHINEDIE'
  crib = msg[:12]
  enigma = MzEnigma.Enigma_D
  name = 'Enigma_D'
  runRejewskiAttack(enigma, name, notify = None)
 elif False:
  # crib = 'NIGMAISTEINEROTORSCHLUESSELMASCHINEDIE'
  crib = msg[:12]
  enigma = MzEnigma.Enigma_M3
  name = 'Enigma_M3'
  runTuringAttack(enigma, name, msg, crib = crib, notify = None)
 else:
  phase2Method = 'Mz'
  enigma = MzEnigma.Enigma_M3
  name = 'Enigma_M3'
  runGilloglyAttack(enigma, name, msg, phase2Method = phase2Method, notify = print)
