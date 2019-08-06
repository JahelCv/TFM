# -*- encoding: UTF-8 -*-
""" Say 'hello, you' each time a human face is detected

"""

import sys
import time
from threading import Thread

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

from AccionesNAO import AccionesNAO
# TODO: Descomentar
from DatosCompartidos import DatosCompartidos
from SimuladorRemoto import SimuladorRemoto
from DispatchGCloud import DispatchGCloud
from Escenario import Escenario
#from Interaccion import Interaccion
#from ThreadManager import ThreadManager

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
        self.ac.decirFrase("Creo proxies exitosamente")        
        self.ac.setLedsOjosRed(False)
        self.ac.setLedsOjosGreen(True)
        self.ac.setLedsOjosBlue(False)
        
        # Creo conexion con simulador 
        self.simremoto = SimuladorRemoto()
        
        # Lanza hilo en remoto
        if self.simremoto.arrancaSimuladorRemoto():
            self.ac.decirFrase('Se ha arrancado el simulador en remoto')
        else:
            self.ac.decirFrase('Error arrancando el simulador en remoto')
            
        # DatosCompartidos tendrá un mejor uso más adelante
        # Se puede fusionar con ThreadManager
        self.dc = DatosCompartidos()
        self.dc.setData("EXACPALABRA",0.4,False)
        
        # El que interactua de verdad con el usuario
        self.es = Escenario(self.dc, self.ac, self.simremoto)
        
        # Crea el que atiende a los subscriptores
        self.dgc = DispatchGCloud(self.ac)
    
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

    # Warning: HumanGreeter must be a global variable
    # The name given to the constructor must be the name of the
    # variable
    global Server
    Server = ServerModule("Server")

    try:
        t = Thread(target = Server.es.run)
        t.start()
        while True:
            print 'Glucosa actual: ' + str(Server.simremoto.getGlucosaRemoto())
            time.sleep(2)
    except KeyboardInterrupt:
        print "Interrupted by user, shutting down"
        Server.asr.pause(True)
        if Server.ac.isWaitingWord:
            Server.memory.unsubscribeToEvent("WordRecognized", "Server")
            Server.asr.unsubscribe("Server")
        myBroker.shutdown()
        sys.exit(0)

if __name__ == "__main__":
    main()