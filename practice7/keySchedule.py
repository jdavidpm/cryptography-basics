from bitstring import *

arrPC1 = [57, 49, 41, 33, 25, 17,  9,\
	   1, 58, 50, 42, 34, 26, 18,\
	  10,  2, 59, 51, 43, 35, 27,\
	  19, 11,  3, 60, 52, 44, 36,\
	  63, 55, 47, 39, 31, 23, 15,\
	   7, 62, 54, 46, 38, 30, 22,\
	  14,  6, 61, 53, 45, 37, 29,\
	  21, 13,  5, 28, 20, 12,  4]

arrPC2 = [14, 17, 11, 24,  1,  5,\
	   3, 28, 15,  6, 21, 10,\
	  23, 19, 12,  4, 26,  8,\
	  16,  7, 27, 20, 13,  2,\
	  41, 52, 31, 37, 47, 55,\
	  30, 40, 51, 45, 33, 48,\
	  44, 49, 39, 56, 34, 53,\
	  46, 42, 50, 36, 29, 32]

shiftRounds = [1] * 2 + [2] * 6 + [1] + [2] * 6 + [1]
shiftRoundACC = [1, 2, 4, 6, 8, 10, 12, 14, 15, 17, 19, 21, 23, 25, 27, 28]

def bytesFormatted(arrHex):
	return " ".join('0x{0:0{1}X}'.format(n, 2) for n in arrHex)

def permutedChoice(keyInput, PC):
	keyPermuted, j, bit = [0] * 7, 0, 0
	for i in (arrPC2 if PC else arrPC1):
		if (bit == 8): j, bit = j + 1, 0
		row = i >> 3
		column = i % 8
		if (i % 8 == 0): row -= 1
		if ((ord(keyInput[row]) & (128 >> ((column - 1) % 8)))):
			keyPermuted[j] |= (128 >> bit)
		bit += 1

	return keyPermuted

def keyGenerator(keyPermuted, nRound):
	nShifts = shiftRoundACC[nRound - 1]
	C0 = BitArray(bytesFormatted(keyPermuted[:3] + [keyPermuted[3]])) >> 4
	D0 = BitArray(bytesFormatted([keyPermuted[3] & 15] + keyPermuted[4:]))
	CN = ((C0 << nShifts) | (C0 >> (28 - nShifts))) & BitArray('0x0fffffff')
	DN = ((D0 << nShifts) | (D0 >> (28 - nShifts))) & BitArray('0x0fffffff')
	CN.append('0x0000000')
	KEYN = BitArray(hex((CN.int | DN.int)))
	if (KEYN.len < 56):
		KEYN.prepend('0x' + ('0' * ((56  - KEYN.len) // 4)))
	return ([i for i in permutedChoice([chr(int(KEYN.hex[i : i + 2], 16)) for i in range(0, len(KEYN.hex), 2)], 1)][:-1])

def getNKey(keyString, keyNumber):
	return bytesFormatted(keyGenerator(permutedChoice(keyString, 0), keyNumber))
