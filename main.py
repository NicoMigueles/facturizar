import os
import sys
import factura
import json


def parseFolder(path):
    return [factura.parseFactura(pdf) for pdf in os.listdir(path) if '.pdf' in pdf]


if len(sys.argv) == 2:
    facturas = parseFolder(str(sys.argv[1]))
    with open('out.json', 'w') as outfile:
        json.dump(facturas, outfile)
else:
    print('Usage: facturizar path')
