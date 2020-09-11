# Facturizar

Herramienta para generar información a partir facturas de ventas de una empresa.

Input:

`pdf default generado por la afip`

Output:

```JSON
  {
    "factura": "A",
    "razon-social": "******",
    "condicion": "IVA Responsable Inscripto",
    "punto-venta": "00000",
    "num-comp": "00000000",
    "num-factura": "00000-00000000",
    "destinatario": {
      "razon-social": "******",
      "cuit": "00000000000",
      "condicion-iva": "IVA Responsable Inscripto",
      "domicilio": "******",
      "condicion-venta": "Cuenta Corriente"
    },
    "items": [
      {
        "producto": "Nombre del producto",
        "cantidad": "0,00",
        "unidad": "unidades",
        "precio-unit": "0,00",
        "bonif-porc": "0,00",
        "subtotal": "0,00",
        "iva": "21%",
        "subtotal-iva": "0,00"
      }
    ],
    "importe_neto_gravado": "0,00",
    "iva_21": "0,00",
    "iva_10_5": "0,00",
    "importe_otros_tributos": "0,00",
    "importe_total": "0,00"
  }
```
