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

documents = sock.execute(dbname,uid,pwd,'service.documents','search', [('name', '!=', '')])


for document in documents:
    document_data = sock.execute(dbname,uid,pwd,'service.documents','read',document,['id', 'name', 'n_ref','ref_services','url_document','comentario'])
    # Docuymentos con url
    if document_data[0]['url_document']:

        services = sock.execute(dbname,uid,pwd,'services.tms','search', [('n_ref', '=', document_data[0]['n_ref'])])
        print("servicio ", services[0])

        vals_document_link = {
            'id': document_data[0]['id'],
            'name': document_data[0]['name'],
            'n_ref': document_data[0]['n_ref'],
            'url_googlemaps': document_data[0]['url_document'],
            'ref_services': services[0],
        }

        return_document_with_link = sock.execute(dbname,uid,pwd,'document.services.tms','search',[('url_googlemaps','=',document_data[0]['url_document'])])

        if not return_document_with_link:
            return_document_with_link = sock.execute(dbname,uid,pwd,'document.services.tms','create',vals_document_link)
            print("Se creo")
        else:
            return_document_with_link = sock.execute(dbname,uid,pwd,'document.services.tms','write',return_document_with_link,vals_document_link)
            print("Se actualizo")

    # Docuymentos sin url
    # else:

    #     services = sock.execute(dbname,uid,pwd,'services.tms','search', [('n_ref', '=', document_data[0]['n_ref'])])
    #     print("servicio ", services[0])

    #     vals_document_without_link = {
    #         'id': document_data[0]['id'],
    #         'name': document_data[0]['name'],
    #         'n_ref': document_data[0]['n_ref'],
    #         'url_googlemaps': '',
    #         'ref_services': services[0],

    #     }
    #     return_document_withou_link = sock.execute(dbname,uid,pwd,'document.services.tms','search',[('id','=',document_data[0]['id'])])

    #     if not return_document_withou_link:
    #         return_document_withou_link = sock.execute(dbname,uid,pwd,'document.services.tms','create',vals_document_without_link)
    #         print("Se creo documento sin link de google")
    #     else:
    #         return_document_withou_link = sock.execute(dbname,uid,pwd,'document.services.tms','write',return_document_withou_link,vals_document_without_link)
    #         print("Se actualizo documento sin link de google")