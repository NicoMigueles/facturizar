#!/usr/bin/env python

import sys
import json
import utils
import factura

from drive import updateFacturasFromDrive


def main():
    updateFacturasFromDrive()
    facturas = factura.parseFolder('facturas')

    print((f'\nTransformando {len(facturas)} facturas.'))
    with open('out/all.json', 'w') as outfile:
        json.dump(facturas, outfile)
    print('Generated all.json')
    utils.saveToCsv('out/facturas.csv', facturas)
    print('Generated facturas.csv')


if __name__ == '__main__':
    main()
