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
    with open('out/facturas.json', 'w') as outfile:
        json.dump(facturas, outfile)
    print('Generated facturas.json')

    excel = []
    for f in facturas.copy():
        f['cliente'] = f['destinatario']['razon-social'].replace(
            'SOCIEDAD ANONIMA COMERCIAL INMOBILIARIA Y FINANCIERA', 'SACIYF').replace(
            'SOCIEDAD ANONIMA COMERCIAL', 'SAC').replace(
            '-', '').replace(
            'S A', 'SA')
        f['zona'] = utils.obtenerZona(f['destinatario']['domicilio'])
        f['cuit'] = f['destinatario']['cuit']
        f['numfactura'] = f['num-factura']
        f['importe'] = f['importe_total']
        f['importe_no_grabado'] = f['importe_otros_tributos']
        f['ventas_grabadas'] = f['importe_neto_gravado']
        f['iva105'] = f['iva_10_5']
        f['iva21'] = f['iva_21']
        f.pop('factura')
        f.pop('razon-social')
        f.pop('condicion')
        f.pop('punto-venta')
        f.pop('num-comp')
        f.pop('importe_neto_gravado')
        f.pop('importe_total')
        f.pop('iva_10_5')
        f.pop('iva_21')
        f.pop('destinatario')
        f.pop('items')
        f.pop('num-factura')
        f.pop('importe_otros_tributos')
        excel.append(f)

    utils.saveToCsv('out/excel.csv', excel)
    print('Generated excel.csv')
    # utils.saveToCsv('out/facturas.csv', facturas)
    # print('Generated facturas.csv')
    # utils.cleanCsv('out/facturas.csv', 'out/ventas.csv')


if __name__ == '__main__':
    main()
