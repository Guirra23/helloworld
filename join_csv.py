import csv


def convert_csv_in_array(filename):
    with open(filename, 'rb') as f:
        reader = csv.reader(f, delimiter=',')
        x = dict([row for row in reader])
    f.close()

    return x


sync_file = '/home/guirra/titans/sync_actives/report_with_lcid_cid_telcelmx.csv'
partner_file = '/home/guirra/titans/sync_actives/telcelmx_tcm_paid_until.csv'
complete_report = '/home/guirra/titans/sync_actives/report_sync_actives_telcelmx.csv'

lcid = convert_csv_in_array(partner_file)

with open(sync_file, 'rb') as f:
    reader = csv.reader(f, delimiter=',')
    with open(complete_report, 'w') as rep:
        report = csv.writer(rep)
        for i, row in enumerate(reader, 1):
            try:
                report.writerow(row + [lcid.get(row[2])])
            except ValueError:
                report.writerow(row)
        print(i)
    rep.close()
f.close()
