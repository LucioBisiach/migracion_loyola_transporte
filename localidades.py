#!/usr/bin/python


import sys
import xmlrpclib
import ssl

import csv
import json
import requests


username = ' ' #user
pwd = ' ' #password
dbname = ' '


gcontext = ssl._create_unverified_context()

# Get de uid
sock_common = xmlrpclib.ServerProxy('http://localhost:8069/xmlrpc/common',context=gcontext)
uid = sock_common.login(dbname, username, pwd)

#replace loalhost with the address of the server
sock = xmlrpclib.ServerProxy('http://localhost:8069/xmlrpc/object',context=gcontext)
print uid

res = requests.get("https://infra.datos.gob.ar/catalog/modernizacion/dataset/7/distribution/7.5/download/localidades.json")
json_localidades_arg = res.json()
# print(json_localidades_arg['localidades'])

for localidad in json_localidades_arg['localidades']:
    country_id = sock.execute(dbname,uid,pwd,'res.country','search',[('name','=','Argentina')])
    provincia = localidad['provincia']

    state_id = sock.execute(dbname,uid,pwd,'res.country.state','search',[('name','=',provincia['nombre']),('country_id','=','Argentina')])

    url_googlemaps = 'https://www.google.com.ar/maps/place/' + localidad['nombre'] + ',' + provincia['nombre']

    vals ={
            'name': localidad['nombre'],
            'state_id': state_id[0],
            'url_googlemaps': url_googlemaps,
            'country_id': country_id[0]
        }

    return_id = sock.execute(dbname,uid,pwd,'places.tms','search',[('name','=',localidad['nombre'])])
    print(return_id)

    if not return_id:
        # return_id = sock.execute(dbname,uid,pwd,'places.tms','create',vals)
        print(return_id)
    else:
        return_id = sock.execute(dbname,uid,pwd,'places.tms','unlink',return_id)
        # return_id = sock.execute(dbname,uid,pwd,'places.tms','write',return_id,vals)

        print(return_id)



#print("Localidades JSON")
# print(json_localidades_arg)

# Claves de nuestro diccionario
#print("Claves de nuestro json")
#print(json_localidades_arg.keys())

#print("Localidades")
#print(json_localidades_arg['localidades-censales'])

#Localidades censales
#qty_localidades = len(json_localidades_arg['localidades-censales'])
#print("Cantidad localidades")
#print(qty_localidades)

# for localidad in json_localidades_arg['localidades-censales']:
#     country_id = sock.execute(dbname,uid,pwd,'res.country','search',[('name','=','Argentina')])
#     provincia = localidad['provincia']

#     state_id = sock.execute(dbname,uid,pwd,'res.country.state','search',[('name','=',provincia['nombre']),('country_id','=','Argentina')])

#     url_googlemaps = 'https://www.google.com.ar/maps/place/' + localidad['nombre'] + ',' + provincia['nombre']

#     vals ={
#             'name': localidad['nombre'],
#             'state_id': state_id[0],
#             'url_googlemaps': url_googlemaps,
#             'country_id': country_id[0]
#         }

#     return_id = sock.execute(dbname,uid,pwd,'places.tms','search',[('name','=',localidad['nombre'])])
#     print(return_id)

#     if not return_id:
#         return_id = sock.execute(dbname,uid,pwd,'places.tms','create',vals)
#         print(return_id)
#     else:
#         return_id = sock.execute(dbname,uid,pwd,'places.tms','write',return_id,vals)
#         print(return_id)



