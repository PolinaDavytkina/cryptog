# -*- coding: utf-8

import random, math

# ПОСТОЯННЫЕ
alph = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
d_alph = "яюэьыъщшчцхфутсрпонмлкйизжедгвба"

def change_line(pr): #функция преобразующая строку.
  pr = pr.replace(" ", "") #убираем пробелы
  pr = pr.lower() #делаем все буквы строчными
  while pr.find(",") != -1: #заменяем все запятые на "зпт"
    str1 = pr[:pr.find(",")]
    str2 = pr[pr.find(",")+1:]
    pr = str1 + "зпт" + str2

  while pr.find(".") != -1: #заменяем все точки на тчк
    str1 = pr[:pr.find(".")]
    str2 = pr[pr.find(".")+1:]
    pr = str1 + "тчк" + str2
  return pr


# ШИФР АТБАШ
def cryp_atb(pr): #функция шифрования
  i = 0
  cryp_text = ""
  n = len(pr)
  for i in range(n): 
    symb = alph[31 - alph.find(pr[i])] # высчитываем символ
    cryp_text = cryp_text + symb
  return cryp_text

def dec_atb(pr): #функция расшифровки 
  pr = pr.replace(" ", "") # убираем пробелы в тексте, который нужно расшифровать
  pr.lower() #делаем все буквы маленькими
  decryp_text = ""
  n = len(pr) 
  i = 0
  for i in range(n): 
    symb = d_alph[31 - d_alph.find(pr[i])] # высчитываем символ
    decryp_text = decryp_text + symb 
  return (decryp_text)

# КОНЕЦ ШИФР АТБАШ


# ШИФР ЦЕЗАРЯ
def cryp_c(pr, k): #функция шифрования
  i = 0
  cryp_text = ""
  n = len(pr)
  for i in range(n): 
    symb = alph[(alph.find(pr[i]) + k) % 32] # ищем нужный символ
    cryp_text = cryp_text + symb
  return cryp_text

def dec_c(pr,k): #функция расшифровки
  pr = pr.replace(" ", "")
  pr = pr.lower()
  i=0
  n = len(pr)
  decryp_text = ""
  for i in range(n): 
    symb = alph[(alph.find(pr[i]) - k + 32) % 32] #ищем нужный символ
    # print(symb)
    decryp_text = decryp_text + symb

  return decryp_text

# КОНЕЦ ШИФР ЦЕЗАРЯ

# ШИФР БЕЛАЗО
def cryp_bel(pr, key): #функция шифрования
    cryp_text = ""
    for position, symb in enumerate(pr):
          k = alph.index(key[position % len(key)]) # ищем с какой позиции начинается
          index = (alph.index(symb) + k) % len(alph) # ищем нужный символ
          cryp_text += alph[index] 
    return cryp_text


def dec_bel(pr, key): #функция расшифровки
    decryp_text = ""
    for position, symb in enumerate(pr):
          k = alph.index(key[position % len(key)]) # ищем с какой позиции начинается
          index = (alph.index(symb) - k) % len(alph) # ищем нужный символ
          decryp_text += alph[index] 
    print(decryp_text)
    return decryp_text
# КОНЕЦ ШИФРА БЕЛАЗО

# ШИФР ТРИТЕМИЙ

def cryp_try(pr): #функция шифрования
    cryp_text = ""
    for position, symb in enumerate(pr):
          k = position
          index = (alph.index(symb) + k) % len(alph) #ищем нужный символ
          cryp_text += alph[index] 
    return cryp_text

def dec_try(pr): #функция расшифровки
    decryp_text = ""
    for position, symb in enumerate(pr):
          k = position
          index = (alph.index(symb) - k) % len(alph) #ищем нужный символ
          decryp_text += alph[index] 
    return decryp_text

# КОНЕЦ ШИФР ТРИТЕМИЙ

# КВАДРАТ ПОЛИБИЯ

def cryp_qp(pr): # функция шифрования
  i = 0


  matr= [["а","б","в","г","д","е"], #матрица для удобства шифрования
       ["ё","ж","з","и","й","к"],
       ["л","м","н","о","п","р"],
       ["с","т","у","ф","х","ц"],
       ["ч","ш","щ","ъ","ы","ь"],
       ["э","ю","я", "-","-","-"]]
  
  cryp_text = ""
  n = len(pr)
  for i in range(n): 
    for j in range (6):
      for k in range (6):
        if pr[i] == matr[j][k]: # ищем букву в матрице
          cryp_text = cryp_text + str(j+1)+ str(k+1) # индексы буквы записываем 

  return cryp_text

def dec_qp(pr): # функция расшифровки
  pr = pr.replace(" ", "")

  i=0
  

  matr= [["а","б","в","г","д","е"], #матрица для удобства расшифровки
       ["ё","ж","з","и","й","к"],
       ["л","м","н","о","п","р"],
       ["с","т","у","ф","х","ц"],
       ["ч","ш","щ","ъ","ы","ь"],
       ["э","ю","я", "-","-","-"]]
  
  decryp_text = ""

  n = len(pr)
  for i in range(0, n - 1, 2): # читаем строку с шагом 2
    j = int(pr[i]) 
    k = int(pr[i+1])
    decryp_text = decryp_text + matr [j-1][k-1] # по найденым индексам записываем букву

  return decryp_text
# КОНЕЦ КВАДРАТ ПОЛИБИЯ

# ШИФР ВИЖЕНЕРА

def cryp_vig(pr, key): #функция шифрования
    cryp_text = ""
    for position, symb in enumerate(pr):
          k = alph.index(key[position])
          index = (alph.index(symb) + k) % len(alph) #ищем нужный символ
          cryp_text+= alph[index] 
    return cryp_text


def dec_vig(pr, key): #функция расшифровки
    decryp_text = ""
    for position, symb in enumerate(pr):
          k = alph.index(key[position])
          index = (alph.index(symb) - k) % len(alph) #ищем нужный символ
          decryp_text += alph[index] 
    return decryp_text


# КОНЕЦ ШИФР ВИЖЕНЕРА

# ВЕРТИКАЛЬНАЯ ПЕРЕСТАНОВКА
def cryp_ver(pr,k): #функция шифрования
  i = 0 
  n_k = len(k) # смотрим длинну ключевого слова
  if len(pr) % n_k != 0:  # считаем количество строк
    n = len(pr)//n_k + 1 
  else: 
    n = len(pr)//n_k
  text = pr
  matr = []
  for i in range(n): # разделяем текст на строки
    if i % 2 != 0:
      str1 = text [:n_k]
      matr.append(str1[::-1]) #записываем строку в обратном порядке, так как при шивровании текст записывается "змейкой"
      text = text [n_k:]
    else:
      matr.append(text [:n_k])
      text = text [n_k:]

  i = 0
  n = len(matr[1])
  m = len(matr)
  if len(matr[m-1]) != n: # последнюю строку дозаполняем прочерками для удобства обработки
    matr[m-1] = matr[m-1] + "-" * (n - len(matr[m-1]))
  column = []

  # print (matr, n, m)
  for i in range(n): #заполняем столбцы
    word = ""
    for j in range(m):
      word = word + matr[j][i]
    column.append(word)
  # print (column)

  k2 = list(k)
  j = 0
  for i in alph: #инденсируем буквы ключа
    if k.find(i) != -1:
      k2[k.find(i)] = j
      # print(k2, j)
      j += 1
  # print(k2)
  result = ''
  for i in k2: #переставляем столбцы
    result = result + column[int(i)]
  return result

def dec_ver(pr,k):  #функция расшифровки
  k2 = list(k)
  j = 0
  for i in alph: # индексируем ключ
    if k.find(i) != -1:
      k2[k.find(i)] = j
      j += 1

  k_symb = len(pr) / len(k) #смотрим сколько целых столбцов у нас есть
  k_symb_b = len(pr) % len(k) #смотрим сколько неполных столбцов
  column=[]
  pr2 = pr
  while pr2 != "": # разделяем на столбцы
    column.append(pr2[0:k_symb])
    pr2=pr2[k_symb:]

  column2 = []
  n_k2 =len (k2)
  for i in range(n_k2): #переставляем столбцы
    column2.append(column[int(k2[i])])
  matr = []
  n = len(column2[1])
  m = len(column2)

  for i in range(n): #собираем текст
    word = ""
    for j in range(m):
      if i % 2 == 0:
        word = word + str(column2[j][i])
      else:
        word = word + str(column2[len(k) - 1- j][i])
    matr.append(word)

  result = ""
  n_matr = len(matr)
  for i in range(n_matr):
    result = result + str(matr[i])
  
  if result.find("-")!=-1:
    index = result.find("-")
    result = result[:index]
  return result
# КОНЕЦ ВЕРТИКАЛЬНАЯ ПЕРЕСТАНОВКА

# БЛОКНОТ ШЕННОНА
def cryp_sh(pr, key): #функция шифрования
  cryp_text = ""
  for m, k in zip(pr, range(len(key))):
    cryp_text = cryp_text + alph[(alph.find(m)+int(key[k]))%32] #ищем нужный символ
  return cryp_text

def dec_sh(pr,key): #функция расшифровки
  decryp_text = ""
  for m, k in zip(pr, range(len(key))):
    decryp_text = decryp_text + alph[(alph.find(m)-int(key[k]))%32] #ищем нужный символ
  return decryp_text
# КОНЕЦ БЛОКНОТ ШЕННОНА


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
   
def is_coprime(e, f):  # проверка на взаимную простоту
  check = 1
  while check!=0: 
    if(math.gcd(e, f) == 1):
      check = 0
      print('Числа ', e, 'и', f, ' взаимно простые')
    else:
      print('Числа ', e, 'и', f, ' НЕ взаимно простые')
      e = int(input('Введите новое значение параметра Е: '))
  return (e)        

def cryp_rsa(pr, n, e): #функция шифрования
  cryp_text = []
  for i in pr:
    cryp_text.append((alph.find(i) ** e) % n)
  return cryp_text

def dec_rsa(pr, n, e, f): #функция расшифровки
  n_pr = len(pr)
  decryp_text = ""
  for i in range(100000):
    if i * e % f == 1:
        d = i
        break
  for i in range(n_pr):
    # print((int(pr[i]) ** d) % n)
    decryp_text = decryp_text + alph[(int(pr[i]) ** d) % n]
  return decryp_text
# КОНЕЦ ШИФРА RSA

# ШИФР ELGAMAL
def is_coprime(k, f):
  check = 1
  while check!=0: 
    if(math.gcd(k, f) == 1):
      check = 0
    else:
      k = random.randint(1,100)
  return (k)     

def cryp_elm(pr,p, g, y,f): #функция шифрования
  n = len(pr)
  cryp_text = ""
  for i in range(n):
    k = random.randint(1,100)
    k = is_coprime(k,f)
    a = (g ** k) % p
    b = (y ** k) *alph.find(pr[i]) % p
    print(a, b)
    cryp_text = cryp_text + str(a) + str(b)

  return cryp_text


def dec_elm(pr): #функция расшифровки
  decryp_text = ""

  return decryp_text
# КОНЕЦ ШИФРА ELGAMAL

# ОБМЕН КЛЮЧАМИ ПО АЛГОРИТМУ DIFFIE-HELLMAN
def exchange_key(n, a):
  key_a = random.randint(2, n-1) # генерируем Секретный ключ первого пользователя
  key_b = random.randint(2, n-1) # генерируем Секретный ключ второго пользователя
  print("Секретный ключ первого пользователя", key_a)
  print("Секретный ключ второго пользователя", key_b)
  y_a = (a ** key_a) % n # вычисляем открытый ключ 1-ого пользователя
  y_b = (a ** key_b) % n # вычисляем открытый ключ 2-ого пользователя
  key_ab = (y_b ** key_a) % n # вычисляем общий ключ для 1-ого пользователя
  key_ba = (y_a ** key_b) % n # вычисляем общий ключ для 2-ого пользователя
  if key_ab == key_ba:
    print("Обмен ключами работает, общие секретные ключи совтадают")
    print(key_ab, "=", key_ba)
  else:
    print("Какая-то ошибка;(")
# КОНЕЦ ОБМЕНА КЛЮЧАМИ DIFFIE-HELLMAN

# ТЕЛО ПРОГРАММЫ

proverb = input("Введите текст:\n")
# proverb = "Леопард не может изменить своих пятен."
# proverb = "абвгдежзийклмнопрстуфхцчшщъыьэюя"

print ("Выберете шифр, которым хотели бы зашифровать: \n ШИФРЫ ОДНОЗНАЧНОЙ ЗАМЕНЫ \n 1 - АТБАШ \n 2 - Шифр Цезаря \n 3 - Квадрат Полибия")
print("ШИФРЫ МНОГОЗНАЧНОЙ ЗАМЕНЫ \n 4 - Шифр Белазо \n 5 - Шифр Тритемия \n 6 - Шифр Виженера ") 
print("ШИФРЫ БЛОЧНОЙ ЗАМЕНЫ \n 7 - Шифр Плейфера \n 8 - Матричный шифр ")
print( "ШИФР ПЕРСТАНОВКИ \n 9 - Шифр Вертикальной Перестановки \n ШИФР ГАММИРОВАНИЯ \n 10- Одноразовый блокнот Шеннона \n ПОТОЧНЫЙ ШИФР \n 11 - А5/1 ")
print( " КОМБИНАЦИОННЫЙ ШИФР \n 12 - Кузнечик \n АССИМЕТРИЧНЫЕ ШИФРЫ(ГЕНЕРАЦИЯ ЦИФРОВОЙ ПОДПИСИ) \n 13 - RSA \n 14 - Elgamal \n 15 - Обмен ключами по алгоритму Diffie-Hellman")
code_ср = input()


# АТБАШ
if code_ср == "1": # проверяем, какой шифр вызвал пользователь
  proverb = change_line(proverb) # вызываем функцию, которая преобразует строку
  cryp_text = cryp_atb(proverb) # вызываем функцию шифрования
  print("Зашифровано(АТБАШ)")
  print(cryp_text)
  decryp_text = dec_atb(cryp_text) # вызываем функцию расшифровки
  print("Расшифрованно(АТБАШ)")
  print(decryp_text)

# Цезарь
elif code_ср == "2": # проверяем, какой шифр вызвал пользователь
  proverb = change_line(proverb) # вызываем функцию, которая преобразует строку
  print("Введите ключ для шифрования")
  key = input()
  key = int(key) #преобразуем введеный ключ в целочисленный формат
  cryp_text = cryp_c(proverb, key) # вызываем функцию шифрования
  print("Зашифровано(Цезарь)")
  print(cryp_text)
  print("Введите ключ для расшифровки")
  key = input()
  key = int(key) #преобразуем введеный ключ в целочисленный формат
  decryp_text = dec_c(cryp_text, key) # вызываем функцию расшифровки
  print("Расшифрованно(Цезарь)")
  print(decryp_text)

# Белазо
elif code_ср == "4": # проверяем, какой шифр вызвал пользователь
  proverb = change_line(proverb) # вызываем функцию, которая преобразует строку
  print("Введите ключ для шифрования")
  key = input() # вводим ключ для шифрования
  cryp_text = cryp_bel(proverb, key) # вызываем функцию шифрования
  print("Зашифровано(Белазо)")
  print(cryp_text)
  print("Введите ключ для расшифровки")
  key = input() # вводим ключ для расшифровки
  decryp_text = dec_bel(cryp_text, key) # вызываем функцию расшифровки
  print("Расшифрованно(Белазо)")
  print(decryp_text)

# Квадрат Полибия
elif code_ср == "3": # проверяем, какой шифр вызвал пользователь
  proverb = change_line(proverb) # вызываем функцию, которая преобразует строку
  cryp_text = cryp_qp(proverb) # вызываем функцию шифрования
  print("Зашифровано(Квадрат Полибия)")
  print(cryp_text)
  decryp_text = dec_qp(cryp_text)
  print("Расшифрованно(Квадрат Полибия)") # вызываем функцию расшифровки
  print(decryp_text)

# Шифр Тритемия
elif code_ср == "5": # проверяем, какой шифр вызвал пользователь
  proverb = change_line(proverb) # вызываем функцию, которая преобразует строку

  cryp_text = cryp_try(proverb) # вызываем функцию шифрования
  print("Зашифровано(Шифр Тритемия)")
  print(cryp_text)

  decryp_text = dec_try(cryp_text) # вызываем функцию расшифровки
  print("Расшифрованно(Шифр Тритемия)")
  print(decryp_text)

# Шифр Виженера
elif code_ср == "6": # проверяем, какой шифр вызвал пользователь
  proverb = change_line(proverb) # вызываем функцию, которая преобразует строку
  n = len(proverb)
  print("Введите ключ для шифрования")
  key = input() # вводим ключ для шифрования
  key += proverb[:n-1] 
  cryp_text = cryp_vig(proverb, key) # вызываем функцию шифрования
  print("Зашифровано(Шифр Виженера)")
  print(cryp_text)
  n = len(proverb)
  print("Введите ключ для шифрования")
  key = input() # вводим ключ для расшифровки
  key += proverb[:n-1] 
  decryp_text = dec_vig(cryp_text, key) # вызываем функцию расшифровки
  print("Расшифрованно(Шифр Виженера)")
  print(decryp_text)

# Шифр Вертикальной Перестановки
elif code_ср == "9": # проверяем, какой шифр вызвал пользователь
  proverb = change_line(proverb) # вызываем функцию, которая преобразует строку
  print("Введите ключ для шифрования")
  key = input()  # вводим ключ для шифрования
  cryp_text = cryp_ver(proverb, key) # вызываем функцию шифрования
  print("Зашифровано(Шифр Вертикальной Перестановки)")
  cryp = cryp_text.replace("-", "")
  print(cryp)
  print("Введите ключ для расшифровки")
  key = input() # вводим ключ для расшифровки
  decryp_text = dec_ver(cryp_text, key) # вызываем функцию расшифровки
  print("Расшифрованно(Шифр Вертикальной Перестановки)")
  print(decryp_text)

# Одноразовый блокнот Шеннона
elif code_ср == "10": # проверяем, какой шифр вызвал пользователь
  proverb = change_line(proverb) # вызываем функцию, которая преобразует строку

  print("Генерируем ключ для шифрования")
  key=[random.randint(1,32) for i in range(len(proverb))] #генеринуем ключ
  print(key)
  cryp_text = cryp_sh(proverb, key) # вызываем функцию шифрования
  print("Зашифровано(Одноразовый блокнот Шеннона)")
  print(cryp_text)
  decryp_text = dec_sh(cryp_text, key) # вызываем функцию расшифровки
  print("Расшифрованно(Одноразовый блокнот Шеннона)")
  print(decryp_text)

# RSA
elif code_ср == "13": # проверяем, какой шифр вызвал пользователь
  proverb = change_line(proverb) # вызываем функцию, которая преобразует строку

  p = int(input("Введите значение параметра P(простое число):"))
  p = prime_num(p) # проверяем параметр р на простоту
  q = int(input("Введите значение параметра Q(простое число):"))
  q = prime_num(q) # проверяем параметр q на простоту
  n=p*q
  f = (p-1)*(q-1)
  print("Введите значение параметра E, взаимно простое", f, ": ")
  e = int(input())
  e = int(is_coprime(e, f)) # проверяем является ли е взаимно простое f


  cryp_text = cryp_rsa(proverb, n, e) # вызываем функцию шифрования
  print("Зашифровано(RSA)")
  print(cryp_text)
  decryp_text = dec_rsa(cryp_text, n, e, f) # вызываем функцию расшифровки
  print("Расшифрованно(RSA)")
  print(decryp_text)

# Elgamal
elif code_ср == "14": # проверяем, какой шифр вызвал пользователь
  proverb = change_line(proverb) # вызываем функцию, которая преобразует строку
  p = int(input("Введите р > 32:"))
  g = random.randint(1,p)
  x = random.randint(1,p)
  y = (g ** x) % p
  print("Открытые ключи p =", p, " g =", g, " y =", y)
  f = p - 1


  cryp_text = cryp_elm(proverb,p,g,y,f)
  print("Зашифровано(Elgamal)")
  print(cryp_text)
  decryp_text = dec_elm(cryp_text) 
  print("Расшифрованно(Elgamal)")
  print(decryp_text)


# Обмен ключами по алгоритму Diffie-Hellman
elif code_ср == "15": # проверяем, какой шифр вызвал пользователь
  print("Введите a и n , удовлетворяюшие условию 1 < a < n \n Введите а")
  a = int(input()) 
  print("Введите n")
  n = int(input())

  if (a > 1) and (a < n):
    exchange_key(n, a)
  else: 
    print("Некорректно введены данные")


else:
    print("Ошибка проверите корректность введенных данных")