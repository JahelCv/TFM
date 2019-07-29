# -*- coding: utf-8 -*-
import requests
import time
urlroot = "http://34.77.125.204:80/"
urlmod = "http://34.77.125.204:80/ModoSimulador/"
urlglu = "http://34.77.125.204:80/Glucosa/"
urlpara = "http://34.77.125.204:80/ParaHilo/"
urldats = "http://34.77.125.204:80/DatosSimulacion/"
urlarranca = "http://34.77.125.204:80/ArrancaHilo/"
urlpausa = "http://34.77.125.204:80/PausaHilo/"
urldespausa = "http://34.77.125.204:80/DespausaHilo/"

#urlroot = "http://localhost:80/"
#urlmod = "http://localhost:80/ModoSimulador/"
#urlglu = "http://localhost:80/Glucosa/"
#urlpara = "http://localhost:80/ParaHilo/"
#urldats = "http://localhost:80/DatosSimulacion/"
#urlarranca = "http://localhost:80/ArrancaHilo/"
#urlpausa = "http://localhost:80/PausaHilo/"
#urldespausa = "http://localhost:80/DespausaHilo/"

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
#r = requests.get(urlglu)
#print "Glucosa antes de modificarla: " + r.content
#
###### MODO ANTES DE MODIFICAR ##
#r = requests.get(urlmod)
#print "Modo antes de modificarlo: " + r.content
#
#r = requests.get(urlarranca)
#print "Arranco hilo: " + r.content
#
#time.sleep(5)
#
############ Pone datos para hacer deporte ############
#r = requests.put(urldats, json={'bolus' : 0, 'cho' : 0, 
#                'ejercicio' : True, 'exercise' : [0,50,60]})
#if r.ok:
#    print "Envio datos de simulacion: " + str(r.json())
#else:
#    print "No ok"
#
#time.sleep(5)
#
############# PAUSO ####################################
#r = requests.get(urlpausa)
#print "Pausa: " + r.content
#
#time.sleep(10)
#
############# DESPAUSO #################################
#r = requests.get(urldespausa)
#print "Despausa: " + r.content
#
#time.sleep(5)
#
############# GET Glucosa ###############################
#r = requests.get(urlglu)
#print "Glucosa: " + r.content
#
# ########### Pone datos para tomarse un zumo ############
#r = requests.put(urldats, json={'bolus' : 2.107, 'cho' : 60, 
#                'ejercicio' : True, 'exercise' : [0,50,60]})
#if r.ok:
#    print "Envio datos de simulacion: " + str(r.json())
#else:
#    print "No ok"
#    
#time.sleep(300)

r = requests.get(urlpara)
print 'Hilo detenido ' + r.content

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