# -*- coding: utf-8 -*-
cidades = ['Aveiro', 'Braga', 'Porto', 'Lisboa']
habitantes = [55291, 181894, 237584, 547631]
for i in range(len(cidades)):
    cidade = cidades[i]
    populacao = habitantes[i]
    print ("{0} tem {1} habitantes".format(cidade, populacao))
