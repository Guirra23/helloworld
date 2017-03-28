import csv
creader = csv.reader(open('csv_teste.csv'))
cwriter = csv.writer(open('csv_teste2.csv', 'w'))

for cline in creader:
    new_line = [val for col, val in enumerate(cline) if col not in (2, 3)]
    cwriter.writerow(new_line)
