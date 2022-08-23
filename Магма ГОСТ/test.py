
from pygost.gost3412 import GOST3412Kuznechik
from pygost.gost3412 import GOST3412Magma
from pygost.utils import hexdec, hexenc


key = hexdec("ffeeddccbbaa99887766554433221100f0f1f2f3f4f5f6f7f8f9fafbfcfdfeff")
plaintext = hexdec("fedcba9876543210")
ciphertext = hexdec("4ee901e5c2d8ca3d")

ciph = GOST3412Magma(key)
print("Ключ:           ", hexenc(key))
print("Обычный текст:    ", hexenc(plaintext))
print("Зашифрованный текст:", hexenc(ciph.encrypt(plaintext)))
print("Зашифрованный текст для проверки:      ", hexenc(ciphertext))
print()
