# -*- coding: utf-8

import sys
from math import ceil
from pygost.gost3412 import GOST3412Magma
from pygost.utils import hexdec, hexenc
from os import urandom

def gost28147_ns2block(ns): # сеть Фейстеля для шифрования

    n1, n2 = ns
    return bytes(bytearray((
        (n2 >> 0) & 255, (n2 >> 8) & 255, (n2 >> 16) & 255, (n2 >> 24) & 255,
        (n1 >> 0) & 255, (n1 >> 8) & 255, (n1 >> 16) & 255, (n1 >> 24) & 255,
    ))) 

def gost28147_encrypt(sbox, key, ns): # поблочное шифрование
    return xcrypt(SEQ_ENCRYPT, sbox, key, ns)


def gost28147_decrypt(sbox, key, ns): #поблочная расшифровка
    return xcrypt(SEQ_DECRYPT, sbox, key, ns)

def gost28147_block2ns(data): # сеть Фейстеля для расшифровки
    data = bytearray(data)
    return (
        data[0] | data[1] << 8 | data[2] << 16 | data[3] << 24,
        data[4] | data[5] << 8 | data[6] << 16 | data[7] << 24,
    )

def xcrypt(seq, sbox, key, ns): #сама функция шифрования/расшифровки
    s = SBOXES[sbox]
    w = bytearray(key)
    x = [
        w[0 + i * 4] |
        w[1 + i * 4] << 8 |
        w[2 + i * 4] << 16 |
        w[3 + i * 4] << 24 for i in range(8)
    ]
    n1, n2 = ns
    for i in seq:
        n1, n2 = _shift11(_K(s, addmod(n1, x[i]))) ^ n2, n1
    return n1, n2

class GOST3412Magma(object): # класс шифрования Магма
    """GOST 34.12-2015 64-bit block cipher Магма (Magma)
    """
    def __init__(self, key): 
        self.key = b"".join(key[i * 4:i * 4 + 4][::-1] for i in range(8))
        self.sbox = data

    def encrypt(self, blk): #шифрование Магма3412, которое базируется на ГОСТ 28147
        return gost28147_ns2block(gost28147_encrypt(
            self.sbox,
            self.key,
            gost28147_block2ns(blk[::-1]),
        ))[::-1]

    def decrypt(self, blk): #расшифровка Магма3412, которое базируется на ГОСТ 28147
        return gost28147_ns2block(gost28147_decrypt(
            self.sbox,
            self.key,
            gost28147_block2ns(blk[::-1]),
        ))[::-1]


flatten = lambda l: [item for sublist in l for item in sublist]

def to_chunks(lst, n = 8):
    lst += bytes([0]) * (ceil(len(lst) / n) * n - len(lst))
    return [lst[i:i + n] for i in range(0, len(lst), n)]


key = None

def set_key(_key):
    global key
    key = hexdec(_key)

def encrypt_magma(data : bytearray):
    global key
    ciph = GOST3412Magma(key) # задаем переменную класса шифрования магма
    return bytearray(flatten([ciph.encrypt(chunk) for chunk in to_chunks(data, 8)])) # шифруем, вызывая функции из класса

def decrypt_magma(data : bytearray):
    global key
    ciph = GOST3412Magma(key) # задаем переменную класса шифрования кузнечика
    return bytearray(flatten([ciph.decrypt(chunk) for chunk in to_chunks(data, 8)])) # расшифровываем, вызывая функции из класса



def main():
    key = hexenc(urandom(32)) #Генерация 32битного ключа
    set_key(key)
    # pr = "Леопард не может изменить своих пятен."
    # pr = " Людмила Петрушевская. Будильник. Жил, да был будильник. У него были усы, шляпа и сердце. И он решил жениться. Он решил жениться, когда стукнет без пятнадцати девять. Ровно в восемь он сделал предложение графину с водой. Графин с водой согласился немедленно, но в пятнадцать минут девятого его унесли и выдали замуж за водопроводный кран. Дело было сделано, и графин вернулся на стол к будильнику уже замужней дамой. Было двадцать минут девятого. Времени оставалось мало. Будильник тогда сделал предложение очкам. Очки были старые и неоднократно выходили замуж за уши. Очки подумали пять минут и согласились, но в этот момент их опять выдали замуж за уши. Было уже восемь часов двадцать пять минут. Тогда будильник быстро сделал предложение книге. Книга тут же согласилась, и будильник стал ждать, когда же стукнет без пятнадцати девять. Сердце его очень громко колотилось. Тут его взяли и накрыли подушкой, потому что детей уложили спать. И без пятнадцати девять будильник неожиданно для себя женился на подушке."
    pr = input("Введите текст: ")
    data = pr.encode('utf-8')
    print(' '.join([str(e) for e in encrypt_magma(data)]))
    cryp_text = ' '.join([str(e) for e in encrypt_magma(data)])

    data = bytes(int(s) for s in cryp_text.split(' '))
    print(decrypt_magma(data).decode('utf-8'))



if __name__ == "__main__":
    main()

