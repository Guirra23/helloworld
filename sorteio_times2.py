# -*- coding: utf-8 -*-
import random


nomes = []
validate = False

while validate is False:
    qtd = int(input("Digite o número de jogadores: "))
    if qtd >= 2 and qtd <= 12:
        validate = True
    continue
    print "Você deve inserir a qtd de jogadores com no mínimo 2 e no máximo 12"

for i in range(qtd):
    n = raw_input("Digite o nome do player : ")
    nomes.append(n)

times = ['Barcelona', 'Real Madrid', 'Borussia Dortmund', 'Bayern Munique',
         'Chelsea', 'PSG', 'Atl Madrid', 'Manchester City', 'Manchester United',
         'Juventus', 'Tottenham', 'Liverpool']

for i, x in enumerate(nomes):
    choice = random.choice(times)
    print ("{} joga com o time {}".format(x, choice))
    times.remove(choice)
