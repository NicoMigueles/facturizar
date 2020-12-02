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

    # Formatear de factura al formato necesario para una venta
    cpy_facturas = facturas.copy()
    ventas = []
    for f in cpy_facturas:
        f['dest_rz'] = f['destinatario']['razon-social']
        f['dest_cuit'] = f['destinatario']['cuit']
        f['dest_dir'] = f['destinatario']['domicilio']
        f.pop('destinatario')
        f.pop('items')
        ventas.append(f)

    utils.saveToCsv('out/tmp.csv', ventas)
    utils.cleanCsv('out/tmp.csv', 'out/ventas.csv')
    print('Generated ventas.csv')

    excel2020 = []
    cpy2_facturas = facturas.copy()
    for f in cpy2_facturas:
        f['cliente'] = f['dest_rz'].replace(
            'SOCIEDAD ANONIMA COMERCIAL INMOBILIARIA Y FINANCIERA', 'SACIYF').replace(
            'SOCIEDAD ANONIMA COMERCIAL', 'SAC').replace(
            '-', '').replace(
            'S A', 'SA')
        f['zona'] = utils.obtenerZona(f['dest_dir'])
        f['cuit'] = f['dest_cuit']
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
        f.pop('dest_rz')
        f.pop('dest_cuit')
        f.pop('dest_dir')
        f.pop('num-factura')
        f.pop('importe_otros_tributos')
        excel2020.append(f)

    utils.saveToCsv('out/excelFormat.csv', excel2020)

    utils.saveToCsv('out/facturas.csv', facturas)
    print('Generated facturas.csv')
    utils.cleanCsv('out/facturas.csv', 'out/ventas.csv')


if __name__ == '__main__':
    main()
