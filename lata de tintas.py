'''Descreva  a metragem quadrada a ser pintada. 1 litro de tinta
cobre 3 metros quadrados e a lata de tinta é vendida em 18 litros, 
que custam R$80,00. Informe ao usuário a quantidade de latas e o 
valor a ser pago. Obs.: Somente são vendidos um número inteiro de latas
'''
m = int(input('Metros a ser pintado: '))
if m % 54 != 0:
 latas = int(m / 54) +1
else:
  latas = m / 54
valor = latas * 80
print ('%d lata(s) a um custo de %.2f' %(latas, valor))