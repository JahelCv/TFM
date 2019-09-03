# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
from DatosCompartidos import DatosCompartidos

class DispatchMQTT(object):
    def __init__(self, ac, dc):
        self.acNAO = ac
        self.datos = dc
        
        broker_address="34.76.240.69"
        self.mqttclient = mqtt.Client() #create new instance
        
        # Conecta a broker e inicia servicio
        self.mqttclient.username_pw_set("nao","nao")
        self.mqttclient.on_message = self.callbackReceived
        self.mqttclient.connect(broker_address) #connect to broker
        self.mqttclient.loop_start() #start the loop
        
        # Suscribimos
        self.mqttclient.subscribe("nao/decir")
        self.mqttclient.subscribe("nao/exacpalabra")
        self.mqttclient.subscribe("hilos")
        self.mqttclient.subscribe("nao/leds")
        self.mqttclient.subscribe("nao/mover")
        
    def publicaInterfazHilosMQTT(self, msg):
#        print "Antes de hacer un publish"
        self.mqttclient.publish("hilos",msg)
#        print "Despues de hacer un publish"
        
    def publicaVentanaEscenarioMQTT(self, msg):
        print "DispatchMQTT # publicaVentanaEscenarioMQTT: Publico -> " + str(msg)
        self.mqttclient.publish("interfaz/ventanaescenario",msg)
    
    def callbackReceived(self, client, userdata, message):
        print 'DispatchMQTT # callbackReceived(): '
        if message.topic == "nao/decir":
            print("Recibo en nao/decir: ", str(message.payload.decode("utf-8")))
            if self.acNAO.getThreadBlock():
                pass
            else:
                self.acNAO.decirFrase(str(message.payload.decode("utf-8")))
        
        elif message.topic == "nao/exacpalabra":
            print("Recibo en nao/exacpalabra: ", str(message.payload.decode("utf-8")))
            fmsg = float(str(message.payload.decode("utf-8")))
            if fmsg >= 0.1 and fmsg <= 0.9:
                self.datos.modifyData("EXACPALABRA", fmsg)
        
        elif message.topic == "hilos":
            print("Recibo en hilos: ", str(message.payload.decode("utf-8")))
            mensaje = str(message.payload.decode("utf-8"))
            lmensaje = mensaje.split(',')
            if lmensaje[1] == "PARADO":
                print("Paro hilo id: " + lmensaje[0])
                self.datos.pararHiloExcluyente(lmensaje[0])
            elif lmensaje[1] == "CORRIENDO":
                print("Arranco hilo id: " + lmensaje[0])
                self.datos.arrancarHiloExcluyente(lmensaje[0])
            elif lmensaje[1] == "PAUSADO":
                print("Pauso hilo id: " + lmensaje[0])
                self.datos.pausarHiloExcluyente(lmensaje[0])
        
        # En este topic viene en formato verde,on
        # siendo el primer componente rojo, azul o verde
        # siendo el segundo componente on o off
        elif message.topic == "nao/leds":
            mensaje = str(message.payload.decode("utf-8"))
            print("Recibo en nao/leds: ", str(message.payload.decode("utf-8")))
            lmensaje = mensaje.split(',')
            # Miramos si on/off
            if lmensaje[1] == "on":
                flag = True
            else:
                flag = False
            #Miramos que leds
            if lmensaje[0] == "verde":
                self.acNAO.setLedsOjosGreen(flag)
            elif lmensaje[0] == "rojo":
                self.acNAO.setLedsOjosRed(flag)
            elif lmensaje[0] == "azul":
                self.acNAO.setLedsOjosBlue(flag)
                
        elif message.topic == "nao/mover":
            print("Recibo en nao/mover: ", str(message.payload.decode("utf-8")))
            if str(message.payload.decode("utf-8")) == "Pincharse":
                self.acNAO.accionPinchate()
            elif str(message.payload.decode("utf-8")) == "Sentarse":
                self.acNAO.accionSentarse()
            elif str(message.payload.decode("utf-8")) == "Parada":
                self.acNAO.posicionParada()
            elif str(message.payload.decode("utf-8")) == "Comer":
                self.acNAO.accionComer()
            elif str(message.payload.decode("utf-8")) == "MedirGlucosa":
                self.acNAO.accionMedirGlucosa()
            elif str(message.payload.decode("utf-8")) == "Correr":
                self.acNAO.accionCorrer()
                
    def pararMQTT(self):
        self.mqttclient.loop_stop()
        
    def setDatosCompartidos(self, d):
        self.datos = d
        
    def setAccionesNAO(self, ac):
        self.acNAO = ac