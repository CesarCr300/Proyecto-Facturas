from xml.dom import minidom
import os
import pandas

def obtener_lista_archivos(origen):
    return os.listdir(facturasOrigen)

def conseguir_dato_segun_etiqueta(doc, direccionFactura, etiqueta,numero_etiqueta):
    dato = doc.getElementsByTagName(etiqueta)[numero_etiqueta]
    return dato.firstChild.data

facturasOrigen = "facturas"
facturas = obtener_lista_archivos(facturasOrigen)  #listaDeArchivos

listaEmpresas = []
consumoDeEmpresas = []
numeroCompras = []
consumo_por_cliente = {"empresa":listaEmpresas, "monto": consumoDeEmpresas, "cantidad de compras": numeroCompras}
productos = []
kilogramos = []

montoLoop = 0
montoMensual = 0
for factura in facturas:
    direccionFactura = facturasOrigen + "/" + factura
    doc = minidom.parse(direccionFactura)

    '''Conseguir monto total de factura'''
    montoLoop = float(conseguir_dato_segun_etiqueta(doc, direccionFactura,"cbc:PayableAmount",0))

    '''Conseguir nombre del cliente'''
    nombreEmpresa = conseguir_dato_segun_etiqueta(doc, direccionFactura, "cbc:RegistrationName",1)

    for nombre_producto in doc.getElementsByTagName("cbc:Description"):
        productos.append(nombre_producto.firstChild.data)
    
    '''Corroborar si la empresa no ha sido agregada'''
    if nombreEmpresa not in listaEmpresas:
        listaEmpresas.append(nombreEmpresa)
        consumoDeEmpresas.append(montoLoop)
        numeroCompras.append(1)
    else:
        indexMonto = listaEmpresas.index(nombreEmpresa)
        consumoDeEmpresas[indexMonto] += montoLoop
        numeroCompras[indexMonto] += 1

    montoMensual += montoLoop
consumo = pandas.DataFrame(consumo_por_cliente)

consumo.to_csv("ventas/venta_1907_2507.csv")

dt_informe_productos = pandas.DataFrame(index=set(productos),columns=listaEmpresas).fillna(0)

for factura in facturas:
    direccionFactura = facturasOrigen + "/" + factura
    doc = minidom.parse(direccionFactura)
    nombreEmpresa = conseguir_dato_segun_etiqueta(doc, direccionFactura, "cbc:RegistrationName", 1)
    i = 0
    for producto in doc.getElementsByTagName("cbc:Description"):
        nombre_producto = producto.firstChild.data
        kg = conseguir_dato_segun_etiqueta(doc, direccionFactura, "cbc:InvoicedQuantity",i)
        i+=1
        dt_informe_productos.loc[nombre_producto, nombreEmpresa] += float(kg)

dt_informe_productos.to_csv("informes/informe_1907_2507.csv")