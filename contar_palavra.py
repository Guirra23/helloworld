# -*- coding: utf-8 -*-
import string

arq = open('texto.doc')
texto = arq.read()
texto = texto.lower()

for c in string.punctuation:
    texto = texto.replace(c, '')
texto = texto.split()

dic = {}
for p in texto:
    if p not in dic:
        dic[p] = 1
    else:
        dic[p] += 1

print ('A palavra universo aparece %s vezes' % dic['universo'])
arq.close()
