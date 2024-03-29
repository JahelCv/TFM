# -*- encoding: UTF-8 -*-
""" Say 'hello, you' each time a human face is detected

"""

import sys
import time
from requests import exceptions

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

from AccionesNAO import AccionesNAO
from DatosCompartidos import DatosCompartidos
from SimuladorRemoto import SimuladorRemoto
from DispatchMQTT import DispatchMQTT
from Escenario import Escenario
from Interaccion import Interaccion

ip = "andy.local"

# Global variable to store the Server module instance
Server = None

class ServerModule(ALModule):
    def __init__(self, name):
        ALModule.__init__(self, name)
        self.name = name
        # No need for IP and port here because
        # we have our Python broker connected to NAOqi broker

        self.memory = ALProxy("ALMemory")
        self.tts = ALProxy("ALTextToSpeech")
        self.asr = ALProxy("ALSpeechRecognition")        
        self.leds = ALProxy("ALLeds")
        self.postureProxy = ALProxy("ALRobotPosture")
        self.motionProxy = ALProxy("ALMotion")
        self.autmov = ALProxy("ALAutonomousMoves")
        self.aspeech = ALProxy("ALAnimatedSpeech")
        
        # Inicializo clases
        self.ac = AccionesNAO(self.tts, self.asr, self.memory, self.leds, 
                              self.postureProxy, self.motionProxy, self.autmov, 
                              self.aspeech, "Server")    
        #self.ac.setRotateEyes()
        
        # DatosCompartidos tendrá un mejor uso más adelante
        # Se puede fusionar con ThreadManager
        self.dc = DatosCompartidos()
        self.dc.setData("EXACPALABRA",0.4)
        
        try:
            # Crea el que atiende a los subscriptores
            self.dmqtt = DispatchMQTT(self.ac, self.dc)
            
            # Creo conexion con simulador 
            self.simremoto = SimuladorRemoto()
            self.simremoto.arrancaSimuladorRemoto()
            
            # El que interactua de verdad con el usuario
            self.es = Escenario(self.dc, self.ac, self.simremoto, self.dmqtt)
            print 'Creo Escenario'
            self.dc.addHiloExcluyente("ESCENARIO", self.es)
            print 'Anyado ESCENARIO como hilo excluyente'
            self.dmqtt.publicaInterfazHilosMQTT("ESCENARIO,"+self.dc.getEstadoHiloExcluyente("ESCENARIO")+",CALLBACKNO")
            print 'Hago un publish al mqtt del ESCENARIO' 
            
            self.inte = Interaccion(self.dc, self.ac, self.simremoto, self.dmqtt)
            print 'Creo Interaccion'
            self.dc.addHiloExcluyente("INTERACCION", self.inte)
            print 'Anyado INTERACCION como hilo excluyente'
            self.dmqtt.publicaInterfazHilosMQTT("INTERACCION,"+self.dc.getEstadoHiloExcluyente("INTERACCION")+",CALLBACKNO")
            print 'Hago un publish al mqtt del INTERACCION'
            self.ac.setLedsOjosRed(False)
            self.ac.setLedsOjosGreen(True)
            self.ac.setLedsOjosBlue(False)
            self.ac.decirFrase("Módulo arrancado exitosamente.")
        except exceptions.ConnectionError:
            print "MainNAO # Exception!"
            self.asr.pause(True)
            if self.ac.isWaitingWord:
                self.memory.unsubscribeToEvent("WordRecognized", "Server")
                self.asr.unsubscribe("Server")
                self.dmqtt.pararMQTT()
            self.simremoto.paraSimuladorRemoto()
            self.dmqtt.publicaInterfazHilosMQTT("ESCENARIO,PARADO")
            self.dmqtt.publicaInterfazHilosMQTT("INTERACCION,PARADO")
            self.ac.decirFrase('No se ha podido conectar con el servicio en la nube, detengo el proceso.')
            sys.exit(0)
        except Exception:
            print "MainNAO # Exception!"
            self.asr.pause(True)
            if self.ac.isWaitingWord:
                self.memory.unsubscribeToEvent("WordRecognized", "Server")
                self.asr.unsubscribe("Server")
                self.dmqtt.pararMQTT()
            self.simremoto.paraSimuladorRemoto()
            self.dmqtt.publicaInterfazHilosMQTT("ESCENARIO,PARADO")
            self.dmqtt.publicaInterfazHilosMQTT("INTERACCION,PARADO")
            self.ac.decirFrase('Ha ocurrido algún problema, detengo el proceso.')
            sys.exit(0)
        
    
    def onWordRecognized(self, key, value, message):
        self.ac.palabraReconocida(value[0], value[1])

def main():
    # We need this broker to be able to construct
    # NAOqi modules and subscribe to other modules
    # The broker must stay alive until the program exists
    myBroker = ALBroker("myBroker",
       "0.0.0.0",   # listen to anyone
       0,           # find a free port and use it
       ip,         # parent broker IP
       9559)       # parent broker port

    # Warning: Server must be a global variable
    # The name given to the constructor must be the name of the
    # variable
    global Server
    Server = ServerModule("Server")

    try:
#        t = Thread(target = Server.es.run)
#        t.start()
        while True:
#            print 'Glucosa actual: ' + str(Server.simremoto.getGlucosaRemoto())
            time.sleep(2)
    except KeyboardInterrupt:
        print "Interrupted by user, shutting down"
        Server.asr.pause(True)
        if Server.ac.isWaitingWord:
            Server.memory.unsubscribeToEvent("WordRecognized", "Server")
            Server.asr.unsubscribe("Server")
            Server.dmqtt.pararMQTT()
        Server.simremoto.paraSimuladorRemoto()
        Server.dmqtt.publicaInterfazHilosMQTT("ESCENARIO,PARADO")
        Server.dmqtt.publicaInterfazHilosMQTT("INTERACCION,PARADO")
        Server.ac.decirFrase('Corto el módulo manualmente.')
        myBroker.shutdown()
        sys.exit(0)
    except Exception:
        print "MainNAO # Exception!"
        Server.asr.pause(True)
        if Server.ac.isWaitingWord:
            Server.memory.unsubscribeToEvent("WordRecognized", "Server")
            Server.asr.unsubscribe("Server")
            Server.dmqtt.pararMQTT()
        Server.simremoto.paraSimuladorRemoto()
        Server.dmqtt.publicaInterfazHilosMQTT("ESCENARIO,PARADO")
        Server.dmqtt.publicaInterfazHilosMQTT("INTERACCION,PARADO")
        Server.ac.decirFrase('Ha ocurrido algún problema, detengo el proceso.')
        myBroker.shutdown()
        sys.exit(0)

if __name__ == "__main__":
    main()