#!/usr/bin/env python

import sys
import json
import utils
import factura

from drive import updateFacturasFromDrive


def main():
    # updateFacturasFromDrive()
    facturas = factura.parseFolder('facturas')

    print((f'\nTransformando {len(facturas)} facturas.'))
    with open('out/all.json', 'w') as outfile:
        json.dump(facturas, outfile)
    print('Generated all.json')

    # Formatear de factura al formato necesario para una venta
    ventas = []
    for f in facturas:
        f['dest_rz'] = f['destinatario']['razon-social']
        f['dest_cuit'] = f['destinatario']['cuit']
        f['dest_dir'] = f['destinatario']['domicilio']
        f.pop('destinatario')
        f.pop('items')
        ventas.append(f)

    utils.saveToCsv('out/tmp.csv', ventas)
    utils.cleanCsv('out/tmp.csv', 'out/ventas.csv')
    print('Generated ventas.csv')

    utils.saveToCsv('out/facturas.csv', facturas)
    print('Generated facturas.csv')
    utils.cleanCsv('out/facturas.csv', 'out/ventas.csv')


if __name__ == '__main__':
    main()
