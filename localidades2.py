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

localidades = sock.execute(dbname,uid,pwd,'places.tms','search',[('name','!=','')])

for localidad in localidades:
    localidad_data = sock.execute(dbname,uid,pwd,'places.tms','read',localidad,['id', 'name'])
    # print(localidad_data[0]['name'])

    return_localidad_data = sock.execute(dbname,uid,pwd,'places.tms','search',[('name','!=','')])
    # print(return_localidad_data)
    if return_localidad_data:
        return_localidad_data = sock.execute(dbname,uid,pwd,'places.tms','unlink',return_localidad_data)
    else:
        print("No hay nada que borrar")