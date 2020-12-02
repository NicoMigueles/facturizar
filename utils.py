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
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(
                csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in dict_data:
                if 'destinatario' in data.keys():
                    data['destinatario'] = ';'.join(
                        [data['destinatario'][key] for key in data['destinatario']])

                if data == '\n':
                    continue
                writer.writerow(data)
    except IOError:
        print("I/O error")


def obtenerZona(dir):
    if 'Misiones' in dir:
        return "M"
    if 'Capital Federal' in dir:
        return "C"
    if 'Buenos Aires' in dir:
        return "BA"

    print(f'No se pudo reconocer automaticamente la zona de {dir}.')
    return input("Ingrese zona manualmente: ").upper()
