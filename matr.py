# -*- coding: utf-8

import numpy as p
import math
from numpy import linalg as inverse

alphabet = "0абвгдеёжзийклмнопрстуфхцчшщъыьэюя"

def inverse_matr(matrix): # Проверка матрицы на обратимость
  try:
    in_matr = inverse.inv(matrix) # вычисляем обратную матрицу
  except p.linalg.LinAlgError: 
    in_matr = "Ошибка, матрица необратима" # обрабатываем ошибку, если обратной матрицы не сушествует
  return in_matr

def cryp_matr(pr, matrkey): #функция шифрования
  n = len(pr)
  k = math.ceil(n / 5) 
  i = 0
  
  s = n % 5
  if s != 0:
    pr = pr + (5 - s) * "0"
  
  text = pr
  cryp_text = ""

  for i in range(k):
    matr = p.matrix([[alphabet.find(text[0])], [alphabet.find(text[1])], [alphabet.find(text[2])], [alphabet.find(text[3])], [alphabet.find(text[4])]])
    text = text[5:]
    matrcryp = p.dot(matrkey, matr)
    # print (matrcryp)

    s1 = str(matrcryp[0][0]) 
    s1 = s1 [s1.find("[") + 1:s1.find("]") + 1]
    s1 = s1 [s1.find("[") + 1:s1.find("]")]

    s2 = str(matrcryp[1][0]) 
    s2 = s2 [s2.find("[") + 1:s2.find("]") + 1]
    s2 = s2 [s2.find("[") + 1:s2.find("]")]

    s3 = str(matrcryp[2][0]) 
    s3 = s3 [s3.find("[") + 1:s3.find("]") + 1]
    s3 = s3 [s3.find("[") + 1:s3.find("]")]

    s4 = str(matrcryp[3][0]) 
    s4 = s4 [s4.find("[") + 1:s4.find("]") + 1]
    s4 = s4 [s4.find("[") + 1:s4.find("]")]

    s5 = str(matrcryp[4][0]) 
    s5 = s5 [s5.find("[") + 1:s5.find("]") + 1]
    s5 = s5 [s5.find("[") + 1:s5.find("]")]

    cryp_text = cryp_text + s1 + " " + s2 + " " + s3 + " " + s4 + " " + s5 + " " 
    
  return cryp_text

def dec_matr(pr, matrkey): #функция расшифровки
  decryp_text = ""
  pr = pr.split()
  i = 0
  n = math.ceil(len(pr) / 5)
  s = len(pr) % 5
  pr_1 = []
  if s != 0:
    for i in range(s):
      pr.append(0)
  i = 0

  for i in range(n):
    matr = p.matrix([[float(pr[0])], [float(pr[1])], [float(pr[2])], [float(pr[3])], [float(pr[4])]])
    # matr = p.matrix([[pr[0]], [pr[1]], [pr[2]], [pr[3]], [pr[4]]])
    k = len(pr)
    j = 0
    pr_1 = []
    for j in range(k - 5):
      pr_1.append(pr[j+5])
    pr = pr_1
    matrdec = p.dot(matrkey, matr)
    a = 0
    for a in range(5):
      if a == 1 or a ==2:
        decryp_text += alphabet[int(matrdec[a][0])+1]
      else:
        decryp_text += alphabet[int(matrdec[a][0])]
  return decryp_text

# proverb = "Леопард не может изменить своих пятен."
# proverb = " Людмила Петрушевская. Будильник. Жил, да был будильник. У него были усы, шляпа и сердце. И он решил жениться. Он решил жениться, когда стукнет без пятнадцати девять. Ровно в восемь он сделал предложение графину с водой. Графин с водой согласился немедленно, но в пятнадцать минут девятого его унесли и выдали замуж за водопроводный кран. Дело было сделано, и графин вернулся на стол к будильнику уже замужней дамой. Было двадцать минут девятого. Времени оставалось мало. Будильник тогда сделал предложение очкам. Очки были старые и неоднократно выходили замуж за уши. Очки подумали пять минут и согласились, но в этот момент их опять выдали замуж за уши. Было уже восемь часов двадцать пять минут. Тогда будильник быстро сделал предложение книге. Книга тут же согласилась, и будильник стал ждать, когда же стукнет без пятнадцати девять. Сердце его очень громко колотилось. Тут его взяли и накрыли подушкой, потому что детей уложили спать. И без пятнадцати девять будильник неожиданно для себя женился на подушке."
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

  
# matrkey_c = p.matrix([[9.86, 3.52, 12.61, 8.00, 4.48], [5.78, 2.18, -1, 1, 1], [3, 1, 1, 1, 1], [2, 1, 1, 4, 1], [2, -1, 1, 1, 5]])
matrkey_c = p.matrix([[4, 1, 1, 2, 1], [1, 2, -1, 1, 1], [3, 1, 1, 1, 1], [2, 1, 1, 4, 1], [2, -1, 1, 1, 5]]) # матрица шифрования
# matrkey_c = p.matrix([[ 1, 2], [2, 4]])
print("Матрица шифрования:")
print(matrkey_c)
matrkey_d = inverse_matr(matrkey_c) # проверяем матрицу на обратимость и сразу же вычисляем обратную матрицу
cryp_text = cryp_matr(proverb, matrkey_c) # шифруем текст
print(cryp_text)
print("Матрица расшифровки:")
print(matrkey_d)
decryp_text = dec_matr(cryp_text, matrkey_d) # расшифровываем текст
print(decryp_text)
