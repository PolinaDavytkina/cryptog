# -*- coding: utf-8
import sys
from math import ceil
from pygost.gost3412 import GOST3412Kuznechik
from pygost.utils import hexdec, hexenc
from os import urandom

def Linv(blk): # линейное преобразование
    for _ in range(16):
        t = blk[0]
        for i in range(15):
            blk[i] = blk[i + 1]
            t ^= GF[blk[i]][LC[i]]
        blk[15] = t
    return blk

def strxor(a, b): # Эта функция будет обрабатывать только самую короткую длину обеих строк, игнорируя оставшуюся.

    mlen = min(len(a), len(b))
    a, b, xor = bytearray(a), bytearray(b), bytearray(mlen)
    for i in xrange(mlen):
        xor[i] = a[i] ^ b[i]
    return bytes(xor)

def lp(blk):
    return L([PI[v] for v in blk])

class GOST3412Kuznechik(object): # класс шифрования
    """GOST 34.12-2015 128-bit block cipher Кузнечик (Kuznechik)
    """
    def __init__(self, key):
        """
        :param key: encryption/decryption key
        :type key: bytes, 32 bytes
        Key scheduling (roundkeys precomputation) is performed here.
        """
        kr0 = bytearray(key[:16]) # разделяем ключ пополам
        kr1 = bytearray(key[16:]) # разделяем ключ пополам
        self.ks = [kr0, kr1]
        for i in range(4):
            for j in range(8):
                k = lp(bytearray(strxor(C[8 * i + j], kr0)))
                kr0, kr1 = [strxor(k, kr1), kr0]
            self.ks.append(kr0)
            self.ks.append(kr1)

    def encrypt(self, blk): # функция шифрования по кузнечику
        blk = bytearray(blk)
        for i in range(9):
            blk = lp(bytearray(strxor(self.ks[i], blk)))
        return bytes(strxor(self.ks[9], blk))

    def decrypt(self, blk): # функция расшифровки по кузнечику
        blk = bytearray(blk)
        for i in range(9, 0, -1):
            blk = [PIinv[v] for v in Linv(bytearray(strxor(self.ks[i], blk)))]
        return bytes(strxor(self.ks[0], blk))

flatten = lambda l: [item for sublist in l for item in sublist]

def to_chunks(lst, n = 8): # делим на куски по 8 бит
    lst += bytes([0]) * (ceil(len(lst) / n) * n - len(lst))
    return [lst[i:i + n] for i in range(0, len(lst), n)]


key = None

def set_key(_key):
    global key
    key = hexdec(_key)

def encrypt_kuz(data : bytearray):
    global key
    ciph = GOST3412Kuznechik(key) # задаем переменную класса шифрования кузнечика
    return bytearray(flatten([ciph.encrypt(chunk) for chunk in to_chunks(data, 16)])) # шифруем, вызывая функции из класса

def decrypt_kuz(data : bytearray):
    global key
    ciph = GOST3412Kuznechik(key) # задаем переменную класса шифрования кузнечика
    return bytearray(flatten([ciph.decrypt(chunk) for chunk in to_chunks(data, 16)])) # расшифровываем, вызывая функции из класса


def main():
    key = hexenc(urandom(32)) #Генерация 32битного ключа
    set_key(key)
    pr = "Леопард не может изменить своих пятен."
    # pr = " Людмила Петрушевская. Будильник. Жил, да был будильник. У него были усы, шляпа и сердце. И он решил жениться. Он решил жениться, когда стукнет без пятнадцати девять. Ровно в восемь он сделал предложение графину с водой. Графин с водой согласился немедленно, но в пятнадцать минут девятого его унесли и выдали замуж за водопроводный кран. Дело было сделано, и графин вернулся на стол к будильнику уже замужней дамой. Было двадцать минут девятого. Времени оставалось мало. Будильник тогда сделал предложение очкам. Очки были старые и неоднократно выходили замуж за уши. Очки подумали пять минут и согласились, но в этот момент их опять выдали замуж за уши. Было уже восемь часов двадцать пять минут. Тогда будильник быстро сделал предложение книге. Книга тут же согласилась, и будильник стал ждать, когда же стукнет без пятнадцати девять. Сердце его очень громко колотилось. Тут его взяли и накрыли подушкой, потому что детей уложили спать. И без пятнадцати девять будильник неожиданно для себя женился на подушке."
    # pr = input("Введите текст: ")
    data = pr.encode('utf-8')
    print(' '.join([str(e) for e in encrypt_kuz(data)]))
    cryp_text = ' '.join([str(e) for e in encrypt_kuz(data)])

    data = bytes(int(s) for s in cryp_text.split(' '))
    print(decrypt_kuz(data).decode('utf-8'))

if __name__ == "__main__":
    main()

