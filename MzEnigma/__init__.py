__description__ = \
"""
An Enigma simulator

Versions:
 0.0.1      first version
"""
__author__ = "Reinhard Maerz"
__date__ = "2021-08-28"
__version__ = "1.2.1"

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

__all__ = [
 'Umkehrwalze', 'Steckerbrett', 'Zusatzwalze', 'Walze', 
 'stdAlphabet', 'sgsAlphabet'
]

from .component import Umkehrwalze, Steckerbrett, Zusatzwalze, Walze
from .component import stdAlphabet, sgsAlphabet

############# Components ############# 

# 1924 Commercial Enigma A, B Mark 1
I_A = Walze(name = 'I_A', wiring = 'DMTWSILRUYQNKFEJCAZBPGXOHV', notches = 'Y')
II_A = Walze(name = 'II_A', wiring = 'HQZGPJTMOBLNCIFDYAWVEUSRKX', notches = 'Y')
III_A = Walze(name = 'III_A', wiring = 'UQNTLSZFMREHDPXKIBVYGJCWOA', notches = 'Y')

# 1925 Commercial Enigma A-133
I_SGS = Walze(name = 'I_SGS', wiring = 'PSBGÖXQJDHOÄUCFRTEZVÅINLYMKA', notches = 'Ä', alphabet = sgsAlphabet)
II_SGS = Walze(name = 'II_SGS', wiring = 'CHNSYÖADMOTRZXBÄIGÅEKQUPFLVJ', notches = 'Ä', alphabet = sgsAlphabet)
III_SGS = Walze(name = 'III_SGS', wiring = 'ÅVQIAÄXRJBÖZSPCFYUNTHDOMEKGL', notches = 'Ä', alphabet = sgsAlphabet)
UKW_SGS = Umkehrwalze(name = 'UKW_SGS', wiring = 'LDGBÄNCPSKJAVFZHXUIÅRMQÖOTEY', alphabet = sgsAlphabet)

# 1926 Enigma D, K, Commercial Enigma A26 and A28
I_D = Walze(name = 'I_D', wiring = 'LPGSZMHAEOQKVXRFYBUTNICJDW', notches = 'Y')
II_D = Walze(name = 'II_D', wiring = 'SLVGBTFXJQOHEWIRZYAMKPCNDU', notches = 'E')
III_D = Walze(name = 'III_D', wiring = 'CJGDPSHKTURAWZXFMYNQOBVLIE', notches = 'N')
UKW_D = Umkehrwalze(name = 'UKW_D', wiring = 'IMETCGFRAYSQBZXWLHKDVUPOJN')

# 1927, Enigma MI
I = Walze(name = 'I', wiring = 'EKMFLGDQVZNTOWYHXUSPAIBRCJ', notches = 'Q')
II = Walze(name = 'II', wiring = 'AJDKSIRUXBLHWTMCQGZNPYFVOE', notches = 'E')
III = Walze(name = 'III', wiring = 'BDFHJLCPRTXVZNYEIWGAKMUSQO', notches = 'V')
IV = Walze(name = 'IV', wiring = 'ESOVPZJAYQUIRHXLNFTGKDCMWB', notches = 'J')
V = Walze(name = 'V', wiring = 'VZBRGITYUPSDNHLXAWMJQOFECK', notches = 'Z')
UKWA = Umkehrwalze(name = 'UKW-A', wiring = 'EJMZALYXVBWFCRQUONTSPIKHGD')	 	 	 
UKWB = Umkehrwalze(name = 'UKW-B', wiring = 'YRUHQSLDPXNGOKMIEBFZCWVJAT')	 	 	 
UKWC = Umkehrwalze(name = 'UKW-C', wiring = 'FVPJIAOYEDRZXWGCTKUQSBNMHL')

# 1932, Enigma M3
VI = Walze(name = 'VI', wiring = 'JPGVOUMFYQBENHZRDKASXLICTW', notches = 'ZM')
VII = Walze(name = 'VII', wiring = 'NZJHGRCXMYSWBOUFAIVLPEKQDT', notches = 'ZM')
VIII = Walze(name = 'VIII', wiring = 'FKQHTLXOCBJSPDZRAMEWNIUYGV', notches = 'ZM')

# 1942, Enigma M4
Beta = Zusatzwalze(name = 'Beta', wiring = 'LEYJVCNIXWPBQMDRTAKZGFUHOS') 	 	 
Gamma = Zusatzwalze(name = 'Gamma', wiring = 'FSOKANUERHMBTIYCWLQPZXVGJD') 	 
UKWThinB = Umkehrwalze(name = 'UKW-ThinB',	wiring = 'ENKQAUYWJICOPBLMDXZVFTHRGS') 
UKWThinC = Umkehrwalze(name = 'UKW-ThinC',	wiring = 'RDOBJNTKVEHMLFCWZAXGYIPSUQ')

# 1942 Enigma T (Tirpitz)
I_T 	= Walze(name = 'I_T', wiring = 'KPTYUELOCVGRFQDANJMBSWHZXI', notches = 'WZEKQ')
II_T 	= Walze(name = 'II_T', wiring = 'UPHZLWEQMTDJXCAKSOIGVBYFNR', notches = 'WZFLR')
III_T 	= Walze(name = 'III_T', wiring = 'QUDLYRFEKONVZAXWHMGPJBSICT', notches = 'WZEKQ')
IV_T 	= Walze(name = 'IV_T', wiring = 'CIWTBKXNRESPFLYDAGVHQUOJZM', notches = 'WZFLR')
V_T 	= Walze(name = 'V_T', wiring = 'UAXGISNJBVERDYLFZWTPCKOHMQ', notches = 'YCFKR')
VI_T 	= Walze(name = 'VI_T', wiring = 'XFUZGALVHCNYSEWQTDMRBKPIOJ', notches = 'XEIMQ')
VII_T 	= Walze(name = 'VII_T', wiring = 'BJVFTXPLNAYOZIKWGDQERUCHSM', notches = 'YCFKR')
VIII_T 	= Walze(name = 'VIII_T', wiring = 'YMTPNZHWKODAJXELUQVGCBISFR', notches = 'XEIMQ')

# 1945 G31 Abwehr Enigma
I_G312 = Walze(name = 'I_G312', wiring = 'DMTWSILRUYQNKFEJCAZBPGXOHV', notches = 'SUVWZABCEFGIKLOPQ')
II_G312 = Walze(name = 'II_G312', wiring = 'HQZGPJTMOBLNCIFDYAWVEUSRKX', notches = 'STVYZACDFGHKMNQ')
III_G312 = Walze(name = 'III_G312', wiring = 'UQNTLSZFMREHDPXKIBVYGJCWOA', notches = 'UWXAEFHKMNR')
UKW_G312 = Umkehrwalze(name = 'UKW_G312', wiring = 'RULQMZJSYGOCETKWDAHNBXPVIF')

# 1945 Norway Enigma (Norenigma)
I_N = Walze(name = 'I_N', wiring = 'WTOKASUYVRBXJHQCPZEFMDINLG', notches = 'Q')
II_N = Walze(name = 'II_N', wiring = 'GJLPUBSWEMCTQVHXAOFZDRKYNI', notches = 'E')
III_N = Walze(name = 'III_N', wiring = 'JWFMHNBPUSDYTIXVZGRQLAOEKC', notches = 'V')
IV_N = Walze(name = 'IV_N', wiring = 'FGZJMVXEPBWSHQTLIUDYKCNRAO', notches = 'J')
V_N = Walze(name = 'V_N', wiring = 'HEJXQOTZBVFDASCILWPGYNMURK', notches = 'Z')
UKW_N = Umkehrwalze(name = 'UKW_N', wiring = 'MOWJYPUXNDSRAIBFVLKZGQCHET')


