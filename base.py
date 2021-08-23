from xml.dom import minidom
import os
import pandas
def obtener_lista_archivos(origen):
    return os.listdir(facturasOrigen)

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
    directionFactura = facturasOrigen + "/" + factura

    '''Conseguir monto tota de factura'''
    doc = minidom.parse(directionFactura)
    monto = doc.getElementsByTagName("cbc:PayableAmount")[0]
    montoLoop = float(monto.firstChild.data)

    '''Conseguir nombre del cliente'''
    doc = minidom.parse(directionFactura)
    empresa = doc.getElementsByTagName("cbc:RegistrationName")[1]
    nombreEmpresa = (empresa.firstChild.data)

    for nombre_producto in doc.getElementsByTagName("cbc:Description"):
        productos.append(nombre_producto.firstChild.data)
    
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
    directionFactura = facturasOrigen + "/" + factura
    doc = minidom.parse(directionFactura)
    empresa = doc.getElementsByTagName("cbc:RegistrationName")[1]
    nombreEmpresa = (empresa.firstChild.data)
    i = 0
    for producto in doc.getElementsByTagName("cbc:Description"):
        nombre_producto = producto.firstChild.data
        kg = doc.getElementsByTagName("cbc:InvoicedQuantity")[i].firstChild.data
        i+=1
        dt_informe_productos.loc[nombre_producto, nombreEmpresa] += float(kg)

dt_informe_productos.to_csv("informes/informe_1907_2507.csv")