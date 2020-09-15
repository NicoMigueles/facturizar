import csv


def toFloat(data, field):
    if '%' in data[field]:
        data[field] = float(data[field].replace('%', '')) / 100
    else:
        data[field] = float(data[field].replace(',', '.'))


def cleanCsv(input, output):
    # Removes the white spaces in file.
    with open(input) as infile, open(output, 'w') as outfile:
        for line in infile:
            if not line.strip():
                continue  # skip the empty line
            outfile.write(line)  # non-empty line. Write it to output


def saveToCsv(filename, dict_data):
    try:
        csv_columns = dict_data[0].keys()
        with open(filename, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in dict_data:
                if 'destinatario' in data.keys():
                    data['destinatario'] = ';'.join(
                        [data['destinatario'][key] for key in data['destinatario']])
                # No lo convierto para que el excel me lo tome como número. wtf pero si.
                # toFloat(data, 'importe_neto_gravado')
                # toFloat(data, 'iva_21')
                # toFloat(data, 'iva_10_5')
                # toFloat(data, 'importe_otros_tributos')
                # toFloat(data, 'importe_total')
                writer.writerow(data)
    except IOError:
        print("I/O error")
