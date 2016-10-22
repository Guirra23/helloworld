# -*- coding: utf-8 -*-
import random
nomes = []
qtd = int(input("Digite o número de jogadores: "))
cont = 1
while cont <= qtd:
    n = [str(x) for x in input("Digite o nome do player : ").split()]
    nomes.append(n)
    cont = cont + 1
times = ['Barcelona', 'Real Madrid', 'Borussia Dortmund', 'Bayern Munique',
         'Chelsea', 'PSG', 'Atl Madrid', 'Manchester City', 'Manchester United',
         'Juventus', 'Tottenham', 'Liverpool']
for i, x in enumerate(nomes):
    choice = random.choice(times)
    print "{} joga com o time {}".format(x, choice)
    times.remove(choice)
