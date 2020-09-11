import os
import pdf
import utils


def getByFieldName(l, field):
    # Returns the value when the field name presides the value.
    # Example: [..., 'Fecha de Emisión:', '04/09/2020', ...]
    # Returns '04/09/2020'
    return l[l.index(field)+1].strip()


def renameDuplicates(l):
    response = []
    for i in l:
        if i in response:
            # Ya existe
            response.append(f'{i} ')
        else:
            response.append(i)
    return response


def getItems(l):
    first_index = l.index('Alicuota\nIVA')
    index = first_index
    items = []
    protected = False
    last = False
    while(l[index+1] != 'Otros Tributos'):
        item = []
        if protected:
            iterations = range(6)
            try:
                if len(items) and float(l[index + 1].replace(',', '.')) == items[0]['subtotal-iva']:
                    index += len(items)
                    last = True
            except:
                pass
        else:
            iterations = range(7)

        for i in iterations:
            index += 1
            if not last:
                if i == 1:
                    if ' ' in l[index]:
                        item.append(l[index].split(' ')[0])
                        item.append(l[index].split(' ')[1])
                    else:
                        print('No tiene espacio en el nombre wtf', l[index])

                elif i == 6:
                    try:
                        utils.toFloat(l, index)
                        item.append(l[index])
                    except:
                        protected = True
                        index -= 1
                        continue
                else:
                    item.append(l[index])
            else:
                if i == 0:
                    if ' ' in l[index]:
                        item.append(l[index].split(' ')[0])
                        item.append(l[index].split(' ')[1])
                    else:
                        print('No tiene espacio en el nombre wtf', l[index])

                elif i == 5:
                    index += 1
                    item.insert(0, l[index])
                else:
                    item.append(l[index])

        nombre = item[0]
        if '\n' in item[0]:
            nombres = []
            for potencial in item[0].split('\n'):
                if 'O/C' in potencial:
                    continue
                nombres.append(potencial)

            if len(nombres) == 1:
                nombre = nombres[0]
            else:
                nombre = ' '.join(nombres)

        if len(item) == 8:
            subtotal_iva = item[7]
        else:
            utils.toFloat(item, 5)
            utils.toFloat(item, 6)

            subtotal_iva = item[5] * (item[6] + 1.00)

        items.append({
            'producto': nombre,
            'cantidad': item[1],
            'unidad': item[2],
            'precio-unit': item[3],
            'bonif-porc': item[4],
            'subtotal': item[5],
            'iva': item[6],
            'subtotal-iva': subtotal_iva,
        })
    return items


def toFactura(raw_output):
    raw_list = renameDuplicates(raw_output.split('\n\n'))
    tipo_factura = raw_list[1].split('\n')[1]
    razon_social = getByFieldName(raw_list, 'Razón Social:')
    cond_frente_al_iva = getByFieldName(raw_list, 'Condición frente al IVA:')
    punto_venta = getByFieldName(raw_list, 'Punto de Venta:')
    num_comp = getByFieldName(raw_list, 'Comp. Nro:')
    destinatario_razon_social = getByFieldName(
        raw_list, 'Apellido y Nombre / Razón Social:')

    destinatario_domicilio = getByFieldName(
        raw_list, 'Domicilio Comercial: ')

    if destinatario_razon_social == 'Condición frente al IVA:':
        destinatario_razon_social = ' '.join(getByFieldName(
            raw_list, 'Domicilio Comercial: ').split('\n')[:2])
    if '\n' in destinatario_domicilio:
        destinatario_domicilio = destinatario_domicilio.split('\n')[-1]

    destinatario_condicion = getByFieldName(
        raw_list, 'Condición frente al IVA: ')
    destinatario_cuit = getByFieldName(raw_list, 'CUIT:')
    destinatario_condicion_de_venta = getByFieldName(
        raw_list, 'Condición de venta:')
    items = getItems(raw_list)

    importe_total = getByFieldName(raw_list, 'Importe Total: $')
    totales = getByFieldName(raw_list,
                             'Importe Neto Gravado: $\nIVA 27%: $\nIVA 21%: $\nIVA 10.5%: $\nIVA 5%: $\nIVA 2.5%: $\nIVA 0%: $\nImporte Otros Tributos: $').split('\n')

    importe_neto_gravado = totales[0]
    #iva_27 = totales[1]
    iva_21 = totales[2]
    iva_10_5 = totales[3]
    #iva_5 = totales[4]
    #iva_2_5 = totales[5]
    #iva_0 = totales[6]
    importe_otros_tributos = totales[7]

    return {
        'factura': tipo_factura,
        'razon-social': razon_social,
        'condicion': cond_frente_al_iva,
        'punto-venta': punto_venta,
        'num-comp': num_comp,
        'num-factura': f'{punto_venta}-{num_comp}',
        'destinatario': {
            'razon-social': destinatario_razon_social,
            'cuit': destinatario_cuit,
            'condicion-iva': destinatario_condicion,
            'domicilio': destinatario_domicilio,
            'condicion-venta': destinatario_condicion_de_venta,
        },
        'items': items,
        'importe_neto_gravado': importe_neto_gravado,
        'iva_21': iva_21,
        'iva_10_5': iva_10_5,
        'importe_otros_tributos': importe_otros_tributos,
        'importe_total': importe_total,

    }


def parseFactura(path):
    return toFactura(pdf.toString(path))


def parseFolder(path):
    return [parseFactura(f'{path}/{pdf}') for pdf in os.listdir(path) if '.pdf' in pdf]
