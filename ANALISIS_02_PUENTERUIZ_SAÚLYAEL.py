# -*- coding: utf-8 -*-
"""
Created on Sun Oct 10 18:57:42 2021

@author: saulp
"""

"""
Columnas del archivo synergy_logistics_database.csv
register_id	
direction	
origin	
destination	
year	
date	
product	
transport_mode	
company_name	
total_value

"""
import csv

registros = []
with open("synergy_logistics_database.csv", "r") as archivo:
    lector = csv.DictReader(archivo)
    
    for registro in lector:
        registros.append(registro)
        
"""        
Opción 1) Rutas de importación y exportación. Synergy logistics está
considerando la posibilidad de enfocar sus esfuerzos en las 10 rutas más
demandadas. Acorde a los flujos de importación y exportación, ¿cuáles son esas
10 rutas? ¿le conviene implementar esa estrategia? ¿porqué?
"""


def calcularDemandaPorRuta(direction = "both"):
    rutas = []
    demandaXRuta = []
    for registro in registros:
        if registro["direction"] == direction or direction == "both":
            origin = registro["origin"]
            destination = registro["destination"]
            if (origin,destination) not in rutas:
                rutas.append((origin,destination))
                demandaXRuta.append([origin,destination,0])
            else:
                demandaXRuta[rutas.index((origin,destination))][2] += 1
    demandaXRuta.sort(reverse = True, key = lambda x:x[2])
    return demandaXRuta
        

importacionesXRuta = calcularDemandaPorRuta("Imports")
exportacionesXRuta = calcularDemandaPorRuta("Exports")

print("\nOpción 1)")
print("Rutas de importación y exportación.")

print("\n10 rutas con mayor importación.")
print("{:<20} {:<20} {:<20}".format("Origen","Destino","Importacinoes"))
for ruta in importacionesXRuta[:10]:
    print("{:<20} {:<20} {:<20}".format(ruta[0],ruta[1],ruta[2]))
    
print("\n10 rutas con mayor exportación.")
print("{:<20} {:<20} {:<20}".format("Origen","Destino","Exportacinoes"))
for ruta in exportacionesXRuta[:10]:
    print("{:<20} {:<20} {:<20}".format(ruta[0],ruta[1],ruta[2]))
    
print("\n10 rutas con menor importación.")
print("{:<20} {:<20} {:<20}".format("Origen","Destino","Importacinoes"))
for ruta in importacionesXRuta[-10:]:
    print("{:<20} {:<20} {:<20}".format(ruta[0],ruta[1],ruta[2]))
    
print("\n10 rutas con menor exportación.")
print("{:<20} {:<20} {:<20}".format("Origen","Destino","Exportacinoes"))
for ruta in exportacionesXRuta[-10:]:
    print("{:<20} {:<20} {:<20}".format(ruta[0],ruta[1],ruta[2]))

"""
Opción 2) Medio de transporte utilizado. ¿Cuáles son los 3 medios de transporte
más importantes para Synergy logistics considerando el valor de las
importaciones y exportaciones? ¿Cuál es medio de transporte que podrían
reducir?

"""

def calcularValorPorTransporte():
    valorXTransporte = []
    transportes = []

    for registro in registros:
        if registro["transport_mode"] in transportes:
            valorXTransporte[transportes.index(registro["transport_mode"])][1] += float(registro["total_value"])
        else:
            valorXTransporte.append([registro["transport_mode"],float(registro["total_value"])])
            transportes.append(registro["transport_mode"])
    valorXTransporte.sort(reverse = True, key = lambda x:x[1])
        
    return valorXTransporte

valorXTransporte = calcularValorPorTransporte()

print("\nOpción 2)")
print("Medio de transporte utilizado.")
print("{:<15} {:<12}".format("Transporte","Valor Total"))
for transporte in valorXTransporte:
    print("{:<15} {:<12}".format(transporte[0],transporte[1]))

"""
Opción 3) Valor total de importaciones y exportaciones. Si Synergy Logistics
quisiera enfocarse en los países que le generan el 80% del valor de las
exportaciones e importaciones ¿en qué grupo de países debería enfocar sus
esfuerzos?

"""

def calcularPorcentajePorPais():
    valorXPais = []
    paises = []
    valorTotal = 0

    for registro in registros:
        if registro["direction"] == "Exports":
            valorTotal += float(registro["total_value"])
            if registro["origin"] in paises:
                valorXPais[paises.index(registro["origin"])][1] += float(registro["total_value"])
            else:
                valorXPais.append([registro["origin"],float(registro["total_value"])])
                paises.append(registro["origin"])
            
    for i in range(len(valorXPais)):
        valorXPais[i][1] = valorXPais[i][1]/valorTotal*100
    
    valorXPais.sort(reverse = True, key = lambda x:x[1])
    
    return valorXPais

valorXPais = calcularPorcentajePorPais()

print("\nOpción 3)")
print("Valor total de importaciones y exportaciones.")
porcentaje = 0
i = 0
print ("{:<15} {:<10}".format("País", "Porcentaje"))
while porcentaje <= 80:
    porcentaje += valorXPais[i][1]
    print ("{:<15} {:<4}%".format(valorXPais[i][0], round(valorXPais[i][1],3)))
    i += 1