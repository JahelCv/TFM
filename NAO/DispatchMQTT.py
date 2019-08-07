# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt

class DispatchMQTT(object):
    def __init__(self, ac):
        self.acNAO = ac
        
        broker_address="iot.eclipse.org"
        self.mqttclient = mqtt.Client("NaoClient", clean_session=True) #create new instance
        self.mqttclient.on_message=self.callbackReceived
        
        # Conecta a broker e inicia servicio
        self.mqttclient.connect(broker_address) #connect to broker
        self.mqttclient.loop_start() #start the loop
        
        # Suscribimos
        self.mqttclient.subscribe("nao/decir")
        self.mqttclient.subscribe("nao/exacpalabra")
        self.mqttclient.subscribe("nao/hilos")
        self.mqttclient.subscribe("nao/leds")
        self.mqttclient.subscribe("nao/mover")
    
    def callbackReceived(self, client, userdata, message):
        if message.topic == "nao/decir":
            print("Recibo en nao/decir: ", str(message.payload.decode("utf-8")))
            if self.acNAO.getThreadBlock():
                pass
            else:
                self.acNAO.decirFrase(str(message.payload.decode("utf-8")))
        
        elif message.topic == "nao/exacpalabra":
            print("Recibo en nao/exacpalabra: ", str(message.payload.decode("utf-8")))
            print(" #### TODO!! ####")
        
        elif message.topic == "nao/hilos":
            print("Recibo en nao/hilos: ", str(message.payload.decode("utf-8")))
            print(" #### TODO!! ####")
        
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