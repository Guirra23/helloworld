# -*- coding: utf-8 -*-
pyg = 'ay'
original = raw_input('Enter a word:')

# Testa se ao menos uma string foi digitada
if len(original) > 0 and original.isalpha():
    # Variável recebe a palavra digitada e converte em minúsculas
    word = original.lower()
    # Variavel recebe a primeira string da variavel 'word'
    first = word[0]
    # Variável faz junção das variáveis anteriores
    new_word = word + first + pyg
    # Variável recebe a mesma porém a partir da segunda string
    new_word = new_word[1:len(new_word)]

    print original
    print new_word
else:
    print 'empty'
