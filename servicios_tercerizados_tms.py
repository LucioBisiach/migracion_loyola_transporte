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

services = sock.execute(dbname,uid,pwd,'service.services','search', [('name', '!=', ''), ('outsourced_service','=',True)])

for service in services:
    service_data = sock.execute(dbname,uid,pwd,'service.services','read',service,['id', 'name', 'label_service','date_start','date_stop','customer','provider','n_ref'])

    # Clientes
    for customer in service_data[0]['customer']:
        if type(customer) == int:
            id_customer = customer

    # Proveedores
    if service_data[0]['provider'] != False:
        for supplier in service_data[0]['provider']:
            if type(supplier) == int:
                id_supplier = supplier
    


    vals_service_tms = {
        'id': service_data[0]['id'],
        'name': service_data[0]['name'],
        'label_service': service_data[0]['label_service'],
        'date_start': service_data[0]['date_start'],
        'date_stop': service_data[0]['date_stop'],
        'n_ref': service_data[0]['n_ref'], 
        'customer': id_customer,
        'supplier': id_supplier,
        'outsourced_service': True,
    }

    return_service_data_tms = sock.execute(dbname,uid,pwd,'services.tms','search',[('name','=',service_data[0]['name'])])
    print(return_service_data_tms)

    if not return_service_data_tms:
        return_service_data_tms = sock.execute(dbname,uid,pwd,'services.tms','create',vals_service_tms) 
        print("Se creo el servicio: ")
        print(service_data[0]['name'])
        print(return_service_data_tms)
    else:
        return_service_data_tms = sock.execute(dbname,uid,pwd,'services.tms','write',return_service_data_tms,vals_service_tms) 
        print("Se actualizo el servicio: ")
        print(service_data[0]['name'])





