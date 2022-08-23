import random, math

# ПОСТОЯННЫЕ
alph = "абвгдежзийклмнопрстуфхцчшщъыьэюя"


# ШИФР RSA
def prime_num(num): # проверка на простоту
  k = 0
  check = 1
  while check!=0: 
    for i in range(2, num // 2+1):
      if (num % i == 0):
        k = k+1
    if (k <= 0):
      print("Число простое")
      check = 0
    elif(check!=0):
      print("Число не является простым")
      num = int(input('Введите значение параметра P(простое число): '))
      k = 0
  return num     
   
def is_coprime(e, f): # проверка на взаимную простоту
  check = 1
  while check!=0: 
    if(math.gcd(e, f) == 1):
      check = 0
      print('Числа ', e, 'и', f, ' взаимно простые')
    else:
      print('Числа ', e, 'и', f, ' НЕ взаимно простые')
      e = int(input('Введите новое значение параметра Е: '))
  return (e)        

def hash_m(pr,p): # функция вычисления хэша
    h = h0 = 0
    for i in pr:
        h=((h0+alph.find(i))**2)%p
        h0=h
    return h

def cryp_prsa(pr, n, e, f): # функция вычисления цифровой подписи
    i = 0
    while i < n:
        if (i * e) % f == 1:
            d = i
            break
        i += 1
    
    print("Параметр d = ", d)
    s = (pr ** d) % n

    return s

def dec_prsa(s, e): # функция проверки цифровой подписи
  m = (s ** e) % n
  return m
# КОНЕЦ ШИФРА RSA

# proverb = "Леопард не может изменить своих пятен."
proverb = input("Введите текст для шифрования: ")

proverb = proverb.replace(" ", "")
proverb = proverb.lower()
while proverb.find(",") != -1:
    str1 = proverb[:proverb.find(",")]
    str2 = proverb[proverb.find(",")+1:]
    proverb = str1 + "зпт" + str2
while proverb.find(".") != -1:
    str1 = proverb[:proverb.find(".")]
    str2 = proverb[proverb.find(".")+1:]
    proverb = str1 + "тчк" + str2

p = int(input("Введите значение параметра P(простое число):"))
p = prime_num(p)
q = int(input("Введите значение параметра Q(простое число):"))
q = prime_num(q)
n=p*q
f = (p-1)*(q-1)
print("Введите значение параметра E, взаимно простое", f, ": ")
e = int(input())
e = int(is_coprime(e, f))

hash = hash_m(proverb, p) #вычисляем хэш

s = cryp_prsa(hash, n, e, f) #вычисляем цифровую подпись
print("Сообщение: ", proverb)
print("Электронная подпись: ", s)
m = dec_prsa(s, e) # подтверждаем цифровую подпись
if m == hash:
    print("Подтверждение электронной подписи")
    print("Хэш функции равны", m, "=", hash)
else:
    print("Подтверждение электронной подписи")
    print("Хэш функции не равны:",m, "!=", hash)