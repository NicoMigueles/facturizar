import os
from factura import parseFactura

factura = "27225914376_001_00003_00000101.pdf"
path = "facturas"
facturas = [ f'{path}/{pdf}' for pdf in os.listdir(path) if '.pdf' in pdf and pdf.split('_')[1] == '001']

parseFactura(facturas[1])

