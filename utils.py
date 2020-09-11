import csv


def toFloat(data, field):
    if '%' in data[field]:
        data[field] = float(data[field].replace('%', '')) / 100
    else:
        data[field] = float(data[field].replace(',', '.'))


def saveToCsv(filename, dict_data):
    try:
        csv_columns = dict_data[0].keys()
        with open(filename, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in dict_data:
                data['destinatario'] = ';'.join(
                    [data['destinatario'][key] for key in data['destinatario']])
                toFloat(data, 'importe_neto_gravado')
                toFloat(data, 'iva_21')
                toFloat(data, 'iva_10_5')
                toFloat(data, 'importe_otros_tributos')
                toFloat(data, 'importe_total')
                writer.writerow(data)
    except IOError:
        print("I/O error")
