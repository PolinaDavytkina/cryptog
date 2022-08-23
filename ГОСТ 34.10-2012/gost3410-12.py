

from os import urandom

from codecs import getdecoder
from codecs import getencoder
from sys import version_info

from pygost.utils import hexdec, hexenc, long2bytes, bytes2long
from pygost import gost34112012512



def modinvert(a, n):
    """ Modular multiplicative inverse
    :returns: inverse number. -1 if it does not exist
    Realization is taken from:
    https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
    """
    if a < 0:
        # k^-1 = p - (-k)^-1 mod p
        return n - modinvert(-a, n)
    t, newt = 0, 1
    r, newr = n, a
    while newr != 0:
        quotinent = r // newr
        t, newt = newt, t - quotinent * newt
        r, newr = newr, r - quotinent * newr
    if r > 1:
        return -1
    if t < 0:
        t = t + n
    return t


MODE2SIZE = {
    2001: 32,
    2012: 64,
}


class GOST3410Curve(object):
    """ GOST 34.10 validated curve
 >>> curve = CURVES["id-GostR3410-2001-TestParamSet"]
 >>> prv = prv_unmarshal(urandom(32))
 >>> signature = sign(curve, prv, GOST341194(data).digest())
 >>> pub = public_key(curve, prv)
 >>> verify(curve, pub, GOST341194(data).digest(), signature)
 True
    :param long p: characteristic of the underlying prime field
    :param long q: elliptic curve subgroup order
    :param long a, b: coefficients of the equation of the elliptic curve in
                      the canonical form
    :param long x, y: the coordinate of the point P (generator of the
                      subgroup of order q) of the elliptic curve in
                      the canonical form
    :param long e, d: coefficients of the equation of the elliptic curve in
                      the twisted Edwards form
    """
    def __init__(self, p, q, a, b, x, y, e=None, d=None):
        self.p = p
        self.q = q
        self.a = a
        self.b = b
        self.x = x
        self.y = y
        self.e = e
        self.d = d
        r1 = self.y * self.y % self.p
        r2 = ((self.x * self.x + self.a) * self.x + self.b) % self.p
        if r1 != self.pos(r2):
             raiseValueError("Invalid parameters")
        self._st = None

    def pos(self, v):
        """Make positive number
        """
        if v < 0:
            return v + self.p
        return v

    def _add(self, p1x, p1y, p2x, p2y): #находим точки на эллиптической кривой
        if p1x == p2x and p1y == p2y:
            t = ((3 * p1x * p1x + self.a) * modinvert(2 * p1y, self.p)) % self.p
        else:
            tx = self.pos(p2x - p1x) % self.p
            ty = self.pos(p2y - p1y) % self.p
            t = (ty * modinvert(tx, self.p)) % self.p
        tx = self.pos(t * t - p1x - p2x) % self.p
        ty = self.pos(t * (p1x - tx) - p1y) % self.p
        return tx, ty

    def exp(self, degree, x=None, y=None): #находим точки на эллиптической кривой
        x = x or self.x
        y = y or self.y
        tx = x
        ty = y
        if degree == 0:
            raise ValueError("Bad degree value")
        degree -= 1
        while degree != 0:
            if degree & 1 == 1:
                tx, ty = self._add(tx, ty, x, y)
            degree = degree >> 1
            x, y = self._add(x, y, x, y)
        return tx, ty

    def st(self):
        """Compute s/t parameters for twisted Edwards curve points conversion
        """
        if self.e  == None or self.d  == None:
            raiseValueError("non twisted Edwards curve")
        if self._st  != None:
            return self._st
        self._st = (
            self.pos(self.e - self.d) * modinvert(4, self.p) % self.p,
            (self.e + self.d) * modinvert(6, self.p) % self.p,
        )
        return self._st


CURVES = {
    "id-tc26-gost-3410-12-512-paramSetA": GOST3410Curve(
        p=bytes2long(hexdec("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFDC7")),
        q=bytes2long(hexdec("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF27E69532F48D89116FF22B8D4E0560609B4B38ABFAD2B85DCACDB1411F10B275")),
        a=bytes2long(hexdec("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFDC4")),
        b=bytes2long(hexdec("E8C2505DEDFC86DDC1BD0B2B6667F1DA34B82574761CB0E879BD081CFD0B6265EE3CB090F30D27614CB4574010DA90DD862EF9D4EBEE4761503190785A71C760")),
        x=bytes2long(hexdec("00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003")),
        y=bytes2long(hexdec("7503CFE87A836AE3A61B8816E25450E6CE5E1C93ACF1ABC1778064FDCBEFA921DF1626BE4FD036E93D75E6A50E3A41E98028FE5FC235F5B889A589CB5215F2A4")),
    ),
    "id-tc26-gost-3410-12-512-paramSetB": GOST3410Curve(
        p=bytes2long(hexdec("8000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000006F")),
        q=bytes2long(hexdec("800000000000000000000000000000000000000000000000000000000000000149A1EC142565A545ACFDB77BD9D40CFA8B996712101BEA0EC6346C54374F25BD")),
        a=bytes2long(hexdec("8000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000006C")),
        b=bytes2long(hexdec("687D1B459DC841457E3E06CF6F5E2517B97C7D614AF138BCBF85DC806C4B289F3E965D2DB1416D217F8B276FAD1AB69C50F78BEE1FA3106EFB8CCBC7C5140116")),
        x=bytes2long(hexdec("00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002")),
        y=bytes2long(hexdec("1A8F7EDA389B094C2C071E3647A8940F3C123B697578C213BE6DD9E6C8EC7335DCB228FD1EDF4A39152CBCAAF8C0398828041055F94CEEEC7E21340780FE41BD")),
    ),
    "id-tc26-gost-3410-2012-512-paramSetC": GOST3410Curve(
        p=bytes2long(hexdec("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFDC7")),
        q=bytes2long(hexdec("3FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFC98CDBA46506AB004C33A9FF5147502CC8EDA9E7A769A12694623CEF47F023ED")),
        a=bytes2long(hexdec("DC9203E514A721875485A529D2C722FB187BC8980EB866644DE41C68E143064546E861C0E2C9EDD92ADE71F46FCF50FF2AD97F951FDA9F2A2EB6546F39689BD3")),
        b=bytes2long(hexdec("B4C4EE28CEBC6C2C8AC12952CF37F16AC7EFB6A9F69F4B57FFDA2E4F0DE5ADE038CBC2FFF719D2C18DE0284B8BFEF3B52B8CC7A5F5BF0A3C8D2319A5312557E1")),
        x=bytes2long(hexdec("E2E31EDFC23DE7BDEBE241CE593EF5DE2295B7A9CBAEF021D385F7074CEA043AA27272A7AE602BF2A7B9033DB9ED3610C6FB85487EAE97AAC5BC7928C1950148")),
        y=bytes2long(hexdec("F5CE40D95B5EB899ABBCCFF5911CB8577939804D6527378B8C108C3D2090FF9BE18E2D33E3021ED2EF32D85822423B6304F726AA854BAE07D0396E9A9ADDC40F")),
        e=0x01,
        d=bytes2long(hexdec("9E4F5D8C017D8D9F13A5CF3CDF5BFE4DAB402D54198E31EBDE28A0621050439CA6B39E0A515C06B304E2CE43E79E369E91A0CFC2BC2A22B4CA302DBB33EE7550")),
    ),
}
CURVES["id-GostR3410-2001-CryptoPro-XchA-ParamSet"] = CURVES["id-GostR3410-2001-CryptoPro-A-ParamSet"]
CURVES["id-GostR3410-2001-CryptoPro-XchB-ParamSet"] = CURVES["id-GostR3410-2001-CryptoPro-C-ParamSet"]
CURVES["id-tc26-gost-3410-2012-256-paramSetB"] = CURVES["id-GostR3410-2001-CryptoPro-A-ParamSet"]
CURVES["id-tc26-gost-3410-2012-256-paramSetC"] = CURVES["id-GostR3410-2001-CryptoPro-B-ParamSet"]
CURVES["id-tc26-gost-3410-2012-256-paramSetD"] = CURVES["id-GostR3410-2001-CryptoPro-C-ParamSet"]
DEFAULT_CURVE = CURVES["id-GostR3410-2001-CryptoPro-A-ParamSet"]


def public_key(curve, prv): # Формируем публичный ключ, изходя из секретного
    """ Generate public key from the private one
 :param GOST3410Curve curve: curve to use
 :param long prv: private key
 :returns: public key's parts, X and Y
 :rtype: (long, long)
    """
    return curve.exp(prv)


def sign(curve, prv, digest, rand=None, mode=2001): # Вычисление цифровой подписи
    size = MODE2SIZE[mode]
    q = curve.q
    e = bytes2long(digest) % q
    if e == 0:
        e = 1
    while True:
        if rand is None:
            rand = urandom(size)
        elif len(rand) != size:
             raiseValueError("rand length != %d" % size) #обработка ошибки
        k = bytes2long(rand) % q
        if k == 0:
            continue
        r, _ = curve.exp(k) # вычисляем координату, вторая координата не нужна
        r %= q
        if r == 0:
            continue
        d = prv * r
        k *= e
        s = (d + k) % q
        if s == 0:
            continue
        break
    return long2bytes(s, size) + long2bytes(r, size)


def verify(curve, pub, digest, signature, mode=2012): #проверка подлинности подписи
    """ Verify provided digest with the signature
 :param GOST3410Curve curve: curve to use
 :type pub: (long, long)
 :param digest: digest needed to check
 :type digest: bytes, 32 or 64 bytes
 :param signature: signature to verify with
 :type signature: bytes, 64 or 128 bytes
 :rtype: bool
    """
    size = MODE2SIZE[mode]
    if len(signature) != size * 2:
         print("Invalid signature length")
    q = curve.q
    p = curve.p
    s = bytes2long(signature[:size])
    r = bytes2long(signature[size:])
    if r <= 0 or r >= q or s <= 0 or s >= q:
        return False
    e = bytes2long(digest) % q
    if e == 0:
        e = 1
    v = modinvert(e, q)
    z1 = s * v % q
    z2 = q - r * v % q
    p1x, p1y = curve.exp(z1)
    q1x, q1y = curve.exp(z2, pub[0], pub[1])
    lm = q1x - p1x
    if lm < 0:
        lm += p
    lm = modinvert(lm, p)
    z1 = q1y - p1y
    lm = lm * z1 % p
    lm = lm * lm % p
    lm = lm - p1x - q1x
    lm = lm % p
    if lm < 0:
        lm += p
    lm %= q
    return lm == r


def prv_unmarshal(prv): # Преобразуем ключ в строку байт
    """Unmarshal private key
 :param bytes prv: serialized private key
 :rtype: long
    """
    return bytes2long(prv[::-1])


def pub_marshal(pub, mode=2012): # Для корректной работы с байтами ключа
    size = MODE2SIZE[mode]
    return (long2bytes(pub[1], size) + long2bytes(pub[0], size))


def pub_unmarshal(pub, mode=2012): # Для корректной работы с байтами ключа
    size = MODE2SIZE[mode]
    pub = pub[::-1]
    return (bytes2long(pub[size:]), bytes2long(pub[:size]))


curve = CURVES["id-tc26-gost-3410-12-512-paramSetA"]

pr = input("Введите текст для шифрования:")
data = pr.encode('utf-8')
key = urandom(64)

prv_raw = key
prv = prv_unmarshal(prv_raw)
pub = public_key(curve, prv)
# print(pub)
print("Открытый ключ:", hexenc(pub_marshal(pub)))
dgst = gost34112012512.new(data).digest()  #хэширование данных, к сожалению этой функции нет в открытом доступе.
signature = sign(curve, prv, dgst)
print("Подпись:", hexenc(signature))

b = verify(curve, pub, dgst, signature)
if b is True:
    print('Подпись прошла проверку')
else:
    print('Подпись не прошла проверку')
