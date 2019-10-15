import math
import random


def hfunc(text, seed=0):  # 
    """
    Хэш-функция one_at_a_time (Jenkins)
    """
    h = 0
    for c in text:
        h += ord(c) + seed
        h += h << 10
        h ^= h >> 6
    h += h << 3
    h ^= h >> 11
    h += h << 15
    return h & 0xffffffff


class Filter1:
    def __init__(self):
        '''
хэшировать ключ полученный в add
хранить значение
acc - хран. ключи
h - новый ключ
складывать acc и h через логическое или |
сравнить логическим и

        '''
        self.acc = 0x00000000
        

    def add(self, text):  # добавитm элемент к множеству
        h = hfunc(text)
        self.acc |= h
        

    def contains(self, text):  # проверяет содержится ли элемент в данном множестве
        h = hfunc(text)

        buff = self.acc & h

        if buff == self.acc:
            return True
        


class Filter2:
    def __init__(self, bits):
        # bits - сколько бит испольщовать на 1 hash
        self.hashes = []
        self.mask = 2**bits-1
        
        
    def add(self, text):
        self.hashes.append(hfunc(text) & self.mask)
        

    def contains(self, text):
        text = hfunc(text) & self.mask
        return text in self.hashes
        
        


class Filter3:
    def __init__(self, size):
        self.bitsarray = [0] * size
        self.size = size
        
    def add(self, text):
        self.bitsarray[hfunc(text)%self.size] = 1

    def contains(self, text):
            return self.bitsarray[hfunc(text)%self.size]  
        


class Filter4:
    def __init__(self, size, number_of_funcs):
        self.array = [0] * size
        self.size = size
        self.number_of_funcs = number_of_funcs 
        

    def add(self, text):
        for i in range(self.number_of_funcs):
            self.array[hfunc(text, seed=i)%self.size] = 1
        

    def contains(self, text):
        for i in range(self.number_of_funcs):
            if not self.array[hfunc(text, seed=i)%self.size]:
                return False
        return True


def test(flt):
    print(type(flt).__name__)
    for email in emails:
        flt.add(email)
    fp, fn = 0, 0
    for email in emails:
        if not flt.contains(email):
            fn += 1
    for email in fake_emails:
        if flt.contains(email) and email not in emails:
            fp += 1
    print("Ложноположительных срабатываний: %.2f%%" % (100 * fp / len(emails)))
    print("Ложноотрицательных срабатываний:", fn)


def shuffle(text):
    lst = list(text)
    random.shuffle(lst)
    return "".join(lst)


random.seed(42)

with open("emails.txt") as f:
    emails = f.read().split("\n")[:10000]

fake_emails = [shuffle(e) for e in emails]


'''hash_ = []
for i in emails:
    hash_.append(hfunc(i)%100)

n = len(set(hash_))
n = (1-1/n)**n
print(1-n)'''


#test(Filter1())
#test(Filter2(10))
#test(Filter3(1000))
test(Filter4(95851, 7))  # теоретическое значение https://hur.st/bloomfilter





































    
    
