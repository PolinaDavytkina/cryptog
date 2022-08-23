#!/usr/bin/env python
from pygost.gost3412 import GOST3412Kuznechik
from pygost.utils import hexdec, hexenc


key = hexdec("8899aabbccddeeff0011223344556677fedcba98765432100123456789abcdef")
plaintext = hexdec("1122334455667700ffeeddccbbaa9988")
ciphertext = hexdec("7f679d90bebc24305a468d42b9d4edcd")

ciph = GOST3412Kuznechik(key)
print("Key:           ", hexenc(key))
print("Plain text:    ", hexenc(plaintext))
print("Encrypted text:", hexenc(ciph.encrypt(plaintext)))
print("Expected:      ", hexenc(ciphertext))
print()
