import re
import copy

# Постоянные переменные
alph = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
r1_length = 19
r2_length = 22
r3_length = 23
key_one = ""
r1 = []
r2 = []
r3 = []

def bin_enc(pr): #преобразуем строку в биты
    result = bin(int.from_bytes(pr.encode(encoding='utf-8'), 'big'))[2:]
    return result

def bin_dec(pr): # преобразуем биты в строку
    pr = int(pr, 2)
    result = pr.to_bytes((pr.bit_length() + 7) // 8, 'big').decode(encoding='utf-8')
    return result 

def set_key(key): #записываем ключ в постоянные переменные
    key_one = key
    loading_registers(key) # вызываем функцию для заполнения регистров


def loading_registers(key): # функция заполнения регистров
	i = 0
	while(i < r1_length): 
		r1.insert(i, int(key[i])) 
		i = i + 1
	j = 0
	p = r1_length
	while(j < r2_length): 
		r2.insert(j,int(key[p])) 
		p = p + 1
		j = j + 1
	k = r2_length + r1_length
	r = 0
	while(r < r3_length): 
		r3.insert(r,int(key[k])) 
		k = k + 1
		r = r + 1

def get_majority(x,y,z): # функция F из методички, иначе говоря определяем число для сравнения с битом синхронизации
	if(x + y + z > 1):
		return 1
	else:
		return 0

def get_keystream(length): # функция изменения регистров
	r1_temp = copy.deepcopy(r1)
	r2_temp = copy.deepcopy(r2)
	r3_temp = copy.deepcopy(r3)
	keystream = []
	i = 0
	while i < length:
		majority = get_majority(r1_temp[8], r2_temp[10], r3_temp[10]) # вычисляем мажор
		if r1_temp[8] == majority: # если бит синхронизации совпадает с мажором, то меняем регистр
			new = r1_temp[13] ^ r1_temp[16] ^ r1_temp[17] ^ r1_temp[18]
			r1_temp_two = copy.deepcopy(r1_temp)
			j = 1
			while(j < len(r1_temp)):
				r1_temp[j] = r1_temp_two[j-1]
				j = j + 1
			r1_temp[0] = new

		if r2_temp[10] == majority: # если бит синхронизации совпадает с мажором, то меняем регистр
			new_one = r2_temp[20] ^ r2_temp[21]
			r2_temp_two = copy.deepcopy(r2_temp)
			k = 1
			while(k < len(r2_temp)):
				r2_temp[k] = r2_temp_two[k-1]
				k = k + 1
			r2_temp[0] = new_one

		if r3_temp[10] == majority: # если бит синхронизации совпадает с мажором, то меняем регистр
			new_two = r3_temp[7] ^ r3_temp[20] ^ r3_temp[21] ^ r3_temp[22]
			r3_temp_two = copy.deepcopy(r3_temp)
			m = 1
			while(m < len(r3_temp)):
				r3_temp[m] = r3_temp_two[m-1]
				m = m + 1
			r3_temp[0] = new_two

		keystream.insert(i, r1_temp[18] ^ r2_temp[21] ^ r3_temp[22])
		i = i + 1
	return keystream

def cryp_a5_1(pr):
    cryp_text = ""
    binary = bin_enc(pr) 
    keystream = get_keystream(len(binary))
    i = 0
    while(i < len(binary)):
        cryp_text = cryp_text + str(int(binary[i]) ^ keystream[i]) 
        i = i + 1
    return cryp_text

def dec_a5_1(pr):
    decryp_text = ""
    binary = []
    keystream = get_keystream(len(pr))
    i = 0
    while(i < len(pr)):
        binary.insert(i,int(pr[i]))
        decryp_text = decryp_text + str(binary[i] ^ keystream[i])
        i = i + 1
    return bin_dec(decryp_text)



# proverb = input("Введите текст для шифрования: ")
proverb = "В"
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



key = str(input("Введите 64-битный ключ: "))
print(key)
set_key(key)
cryp_text = cryp_a5_1(proverb)
print("Зашифровано(A5/1)")
print(cryp_text)
decryp_text = dec_a5_1(cryp_text)
print("Расшифрованно(A5/1)")
print(decryp_text)

# Ключ: 0101001000011010110001110001100100101001000000110111111010110111
