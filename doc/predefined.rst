.. _crytomuseum: https://www.cryptomuseum.com/crypto/enigma/tree.htm

Predefined Components and Engines
*******************************************************

See `crytomuseum`_ for details ...

Steckerbrett Components
==================================

.. code-block:: python

  MARK_1 = Steckerbrett.Mark_1() # random wiring
  MARK_2 = Steckerbrett.Mark_2() # random wiring
  MARK_3 = Steckerbrett.Mark_3(nConnections = 10) # random wiring
  UnconnectedSteckerbrett = Steckerbrett('Unconnected', stdAlphabet)
  
Predefined Engines
==================================

1924 Commercial Enigma A, B Mark 1
-------------------------------------------------------------

.. code-block:: python

  I_A = Walze(name = 'I_A', wiring = 'DMTWSILRUYQNKFEJCAZBPGXOHV', notches = 'Y') 
  II_A = Walze(name = 'II_A', wiring = 'HQZGPJTMOBLNCIFDYAWVEUSRKX', notches = 'Y') 
  III_A = Walze(name = 'III_A', wiring = 'UQNTLSZFMREHDPXKIBVYGJCWOA', notches = 'Y') 
  UKW_D = Umkehrwalze(name = 'UKW_D', wiring = 'IMETCGFRAYSQBZXWLHKDVUPOJN') 
  Enigma_A = Enigma(model = 'Enigma A', walzen = [I_A, II_A, III_A], umkehrwalzen = [UKW_D], numberOfWalzen = 2)

1925 Commercial Enigma A-133
-------------------------------------------------------------

.. code-block:: python

  I_SGS = Walze(name = 'I_SGS', wiring = 'PSBGÖXQJDHOÄUCFRTEZVÅINLYMKA', notches = 'Ä', alphabet = sgsAlphabet)
  II_SGS = Walze(name = 'II_SGS', wiring = 'CHNSYÖADMOTRZXBÄIGÅEKQUPFLVJ', notches = 'Ä', alphabet = sgsAlphabet)
  III_SGS = Walze(name = 'III_SGS', wiring = 'ÅVQIAÄXRJBÖZSPCFYUNTHDOMEKGL', notches = 'Ä', alphabet = sgsAlphabet)
  UKW_SGS = Umkehrwalze(name = 'UKW_SGS', wiring = 'LDGBÄNCPSKJAVFZHXUIÅRMQÖOTEY', alphabet = sgsAlphabet)
  Enigma_SGS = Enigma(model = 'Enigma SGS', walzen = [I_SGS, II_SGS, III_SGS], umkehrwalzen = [UKW_SGS], numberOfWalzen = 2)

1926 Reichswehr Enigma D, K, Commercial Enigma A26 and A28
-------------------------------------------------------------

.. code-block:: python

  I_D = Walze(name = 'I_D', wiring = 'LPGSZMHAEOQKVXRFYBUTNICJDW', notches = 'Y')
  II_D = Walze(name = 'II_D', wiring = 'SLVGBTFXJQOHEWIRZYAMKPCNDU', notches = 'E')
  III_D = Walze(name = 'III_D', wiring = 'CJGDPSHKTURAWZXFMYNQOBVLIE', notches = 'N')
  Enigma_D = Enigma(model = 'Enigma D', walzen = [I_D, II_D, III_D], umkehrwalzen = [UKW_D], numberOfWalzen = 3)

1929 Reichswehr Enigma I, 1940 Kriegsmarine Enigma M3, 1941 U-Boot Enigma M4
-------------------------------------------------------------------------------------------------------------

.. code-block:: python

  I = Walze(name = 'I', wiring = 'EKMFLGDQVZNTOWYHXUSPAIBRCJ', notches = 'Q')
  II = Walze(name = 'II', wiring = 'AJDKSIRUXBLHWTMCQGZNPYFVOE', notches = 'E')
  III = Walze(name = 'III', wiring = 'BDFHJLCPRTXVZNYEIWGAKMUSQO', notches = 'V')
  IV = Walze(name = 'IV', wiring = 'ESOVPZJAYQUIRHXLNFTGKDCMWB', notches = 'J')
  V = Walze(name = 'V', wiring = 'VZBRGITYUPSDNHLXAWMJQOFECK', notches = 'Z')
  VI = Walze(name = 'VI', wiring = 'JPGVOUMFYQBENHZRDKASXLICTW', notches = 'ZM')
  VII = Walze(name = 'VII', wiring = 'NZJHGRCXMYSWBOUFAIVLPEKQDT', notches = 'ZM')
  VIII = Walze(name = 'VIII', wiring = 'FKQHTLXOCBJSPDZRAMEWNIUYGV', notches = 'ZM')
  UKW_A = Umkehrwalze(name = 'UKW-A', wiring = 'EJMZALYXVBWFCRQUONTSPIKHGD')	 	 	 
  UKW_B = Umkehrwalze(name = 'UKW-B', wiring = 'YRUHQSLDPXNGOKMIEBFZCWVJAT')	 	 	 
  UKW_C = Umkehrwalze(name = 'UKW-C', wiring = 'FVPJIAOYEDRZXWGCTKUQSBNMHL')
  UKW_ThinB = Umkehrwalze(name = 'UKW-ThinB',	wiring = 'ENKQAUYWJICOPBLMDXZVFTHRGS') 
  UKW_ThinC = Umkehrwalze(name = 'UKW-ThinC',	wiring = 'RDOBJNTKVEHMLFCWZAXGYIPSUQ')
  Beta = Zusatzwalze(name = 'Beta', wiring = 'LEYJVCNIXWPBQMDRTAKZGFUHOS') 	 	 
  Gamma = Zusatzwalze(name = 'Gamma', wiring = 'FSOKANUERHMBTIYCWLQPZXVGJD') 	 
  Enigma_I = Enigma(model = 'Enigma I', walzen = [I, II, III, IV, V], umkehrwalzen = [UKW_A, UKW_B, UKW_C], steckerbrett = MARK_3, numberOfWalzen = 3)
  Enigma_M3 = Enigma(model = 'Enigma M3', walzen = [I, II, III, IV, V, VI, VII, VIII], 
                             umkehrwalzen = [UKW_A, UKW_B, UKW_C], steckerbrett = MARK_3, numberOfWalzen = 3)
  Enigma_M4 = Enigma(model = 'Enigma M4', walzen = [I, II, III, IV, V, VI, VII, VIII], umkehrwalzen = [UKW_ThinB, UKW_ThinC], 
                             steckerbrett = MARK_3, zusatzwalzen = [Beta, Gamma],  numberOfWalzen = 4)

1942 Enigma T (Tirpitz)
-------------------------------------------------------------

.. code-block:: python

  I_T 	= Walze(name = 'I_T', wiring = 'KPTYUELOCVGRFQDANJMBSWHZXI', notches = 'WZEKQ')
  II_T 	= Walze(name = 'II_T', wiring = 'UPHZLWEQMTDJXCAKSOIGVBYFNR', notches = 'WZFLR')
  III_T 	= Walze(name = 'III_T', wiring = 'QUDLYRFEKONVZAXWHMGPJBSICT', notches = 'WZEKQ')
  IV_T 	= Walze(name = 'IV_T', wiring = 'CIWTBKXNRESPFLYDAGVHQUOJZM', notches = 'WZFLR')
  V_T 	= Walze(name = 'V_T', wiring = 'UAXGISNJBVERDYLFZWTPCKOHMQ', notches = 'YCFKR')
  VI_T 	= Walze(name = 'VI_T', wiring = 'XFUZGALVHCNYSEWQTDMRBKPIOJ', notches = 'XEIMQ')
  VII_T 	= Walze(name = 'VII_T', wiring = 'BJVFTXPLNAYOZIKWGDQERUCHSM', notches = 'YCFKR')
  VIII_T 	= Walze(name = 'VIII_T', wiring = 'YMTPNZHWKODAJXELUQVGCBISFR', notches = 'XEIMQ')
  UKW_T = Umkehrwalze(name = 'UKW_T',	wiring = 'GEKPBTAUMOCNILJDXZYFHWVQSR') 
  Enigma_T = Enigma(model = 'Enigma Tirpitz', walzen = [I_T, II_T, III_T, IV_T, V_T, VI_T, VII_T, VIII_T], 
                           umkehrwalzen = [UKW_T], numberOfWalzen = 3)
                           
1931 G31 Abwehr Enigma
-------------------------------------------------------------

.. code-block:: python

  I_G312 = Walze(name = 'I_G312', wiring = 'DMTWSILRUYQNKFEJCAZBPGXOHV', notches = 'SUVWZABCEFGIKLOPQ')
  II_G312 = Walze(name = 'II_G312', wiring = 'HQZGPJTMOBLNCIFDYAWVEUSRKX', notches = 'STVYZACDFGHKMNQ')
  III_G312 = Walze(name = 'III_G312', wiring = 'UQNTLSZFMREHDPXKIBVYGJCWOA', notches = 'UWXAEFHKMNR')
  UKW_G312 = Umkehrwalze(name = 'UKW_G312', wiring = 'RULQMZJSYGOCETKWDAHNBXPVIF')
  Enigma_G312 = Enigma(model = 'Enigma G-312', walzen = [I_G312, II_G312, III_G312], 
                           umkehrwalzen = [UKW_G312], numberOfWalzen = 3)

1945 Norway Enigma (Norenigma)
-------------------------------------------------------------

.. code-block:: python

  I_N = Walze(name = 'I_N', wiring = 'WTOKASUYVRBXJHQCPZEFMDINLG', notches = 'Q')
  II_N = Walze(name = 'II_N', wiring = 'GJLPUBSWEMCTQVHXAOFZDRKYNI', notches = 'E')
  III_N = Walze(name = 'III_N', wiring = 'JWFMHNBPUSDYTIXVZGRQLAOEKC', notches = 'V')
  IV_N = Walze(name = 'IV_N', wiring = 'FGZJMVXEPBWSHQTLIUDYKCNRAO', notches = 'J')
  V_N = Walze(name = 'V_N', wiring = 'HEJXQOTZBVFDASCILWPGYNMURK', notches = 'Z')
  UKW_N = Umkehrwalze(name = 'UKW_N', wiring = 'MOWJYPUXNDSRAIBFVLKZGQCHET')
  Enigma_N = Enigma(model = 'Norenigma', walzen = [I_N, II_N, III_N, IV_N, V_N], 
                           umkehrwalzen = [UKW_N], numberOfWalzen = 3)

