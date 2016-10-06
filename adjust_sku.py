import csv


def package_name(package_name):
    if package_name == 'Clarosync 10GB Semanal':
        return 'Clarosync 50GB Semanal'
    if package_name == 'Clarosync 10GB Mensal':
        return 'Clarosync 50GB Mensal'
    if package_name == 'Clarosync 30GB':
        return 'Clarosync 100GB Mensal'
    if package_name == 'Clarosync 100GB':
        return 'Clarosync 1TB Mensal'
    if package_name == 'Clarosync 10GB':
        return 'Clarosync 50GB Mensal'

    return None


def create_array(file_path):
    with open(file_path, 'rb') as f:
        reader = csv.reader(f, delimiter=',')
        x = []
        for row in reader:
            x.append(row)
        return x


file_path = "/home/guirra/Downloads/sku.csv"
file = open("/home/guirra/Downloads/sku2.csv", 'w')
with open(file_path, 'rb') as f:
    reader = csv.reader(f, delimiter=',')
    temp = create_array(file_path)
    for line in reader:
        pack_name = package_name(line[1])
        if not pack_name:
            continue
        for row in temp:
            if row[4] == line[4] and row[1] == pack_name:
                if line[0] > row[0]:
                    file.write('{},{}'.format(row[2], line[2]))
                else:
                    file.write('{},{}'.format(line[2], row[2]))
                file.write('\n')
    file.close()
