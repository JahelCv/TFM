# -*- coding: utf-8 -*-
import requests
import time
urlroot = "http://34.77.125.204:80/"
urlmod = "http://34.77.125.204:80/ModoSimulador/"
urlglu = "http://34.77.125.204:80/Glucosa/"
urlpara = "http://34.77.125.204:80/ParaHilo/"
urlarranca = "http://34.77.125.204:80/ArrancaHilo/"

#urlroot = "http://localhost:80/"
#urlmod = "http://localhost:80/ModoSimulador/"
#urlglu = "http://localhost:80/Glucosa/"
#urlpara = "http://localhost:80/ParaHilo/"
#urlarranca = "http://localhost:80/ArrancaHilo/"

###### CONSULTA A ROOT #############
#r = requests.get(urlroot)
#print r.content
#

##### REGISTRA NAOS ###############
#r = requests.get(urlreg)
#idnao = r.content
#print idnao
#
###### LISTA NAOS ##################
#r = requests.get(urllista)
#print r.content

##### GLUCOSA ANTES DE MODIFICAR ##
r = requests.get(urlglu)
print "Glucosa antes de modificarla: " + r.content

##### MODO ANTES DE MODIFICAR ##
r = requests.get(urlmod)
print "Modo antes de modificarlo: " + r.content

r = requests.get(urlarranca)
print "Arranco hilo: " + r.content

time.sleep(10)

r = requests.get(urlpara)
print "Paro hilo: " + r.content

###### MODIFICAR GLUCOSA ###########
#r = requests.put(urlglu, data={'data': 2345})
#print "Que recibe put: " + r.content
#
###### GLUCOSA DESPUES DE MODIFICAR ##
#r = requests.get(urlglu)
#print "Glucosa despues de modificarla: " + r.content



###### MODIFICAR MODO ###########
#r = requests.put(urlmod, data={'data': 3})
#print "Que recibe put: " + r.content
#
###### MODO DESPUES DE MODIFICAR ##
#r = requests.get(urlmod)
#print "Modo despues de modificarlo: " + r.content