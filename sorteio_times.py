import random

nomes = ['Gel', 'Daniel', 'Lirio', 'Felipe', 'Gabriel', 'Gustavo',
         'Bertolini', 'Guirra', 'Leornardo', 'Fernando']
times = ['Barcelona', 'Real Madrid', 'Borussia Dortmund', 'Bayer Munique',
         'Chelsea', 'PSG', 'Atl Madrid', 'Manchester City', 'Manchester United',
         'Juventus', 'Tottenham', 'Liverpool']
for i, x in enumerate(nomes):
    choice = random.choice(times)
    print "{} joga com o time {}".format(x, choice)
    times.remove(choice)
