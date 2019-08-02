# -*- encoding: UTF-8 -*-
""" Say 'hello, you' each time a human face is detected

"""

import sys
import time

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

from AccionesNAO import AccionesNAO
from Ejemplo import Ejemplo
# TODO: Descomentar
#from DatosCompartidos import DatosCompartidos
#from Dispatcher import Dispatcher
#from Escenario import Escenario
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

        # Create a proxy to ALTextToSpeech for later use
#        global memory
        self.memory = ALProxy("ALMemory")
        self.tts = ALProxy("ALTextToSpeech")
        self.asr = ALProxy("ALSpeechRecognition")        
        self.leds = ALProxy("ALLeds")
        self.postureProxy = ALProxy("ALRobotPosture")
        self.motionProxy = ALProxy("ALMotion")
        self.autmov = ALProxy("ALAutonomousMoves")
        self.aspeech = ALProxy("ALAnimatedSpeech")
        
#        # Inicializo clases
        self.ac = AccionesNAO(self.tts, self.asr, self.memory, self.leds, self.postureProxy, 
                              self.motionProxy, self.autmov, self.aspeech, "Server")        
        # TODO: DESCOMENTAR
#        self.dc = DatosCompartidos()
#        self.dc.setData("EXACPALABRA",0.4,False)
#        self.tm = ThreadManager(self.dc)
#        self.disp = Dispatcher(self.dc, self.tm, self.ac)
#        self.es = Escenario(self.dc, self.ac)
#        self.int = Interaccion(self.dc, self.ac)
#        self.tm.addHiloExcluyente("INTERACCION",self.int)
#        self.tm.addHiloExcluyente("ESCENARIO",self.es)
#        memory.unsubscribeToEvent(self.getName(), "onWordRecognized")
        self.ac.decirFrase("Cargo proxies exitosamente")
        
#        self.ac.setLedsOjosRed(False)
#        self.ac.setLedsOjosGreen(True)
#        self.ac.setLedsOjosBlue(False)
#        time.sleep(1)
        
#        self.asr.subscribe("Server")
#        self.memory.subscribeToEvent("WordRecognized", "Server", "onWordRecognized")
#        
#        self.asr.pause(False)
    
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
        # Inicializo clases
#        (ret, p, e) = Server.ac.esperarPalabra(["Me oyes","Si","No","Dime tu glucosa"], 15)
#        print 'MAIN(Ret = '+str(ret)+'): Se obtiene palabra: ' + str(p) + ' con exactitud: ' + str(e)
        Server.ac.decirFrase("Accion quetalestás.")
        Server.ac.accionQUETALESTAS(1)
        time.sleep(5)   
        Server.ac.decirFrase("Acción despedida.")
        Server.ac.accionDespedida(1)
        time.sleep(2)
        Server.ac.decirFrase("Acción saludo.")
        Server.ac.accionSaludo(1)
        time.sleep(2)
        Server.ac.decirFrase("Acción comer.")
        Server.ac.accionComer()
        time.sleep(2)
#        Server.ac.accionLevantarse()
        while True:
            time.sleep(1)
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