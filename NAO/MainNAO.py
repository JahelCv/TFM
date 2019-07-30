# -*- encoding: UTF-8 -*-
""" Say 'hello, you' each time a human face is detected

"""

import sys
import time

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

from AccionesNAO import AccionesNAO
# TODO: Descomentar
#from DatosCompartidos import DatosCompartidos
#from Dispatcher import Dispatcher
#from Escenario import Escenario
#from Interaccion import Interaccion
#from ThreadManager import ThreadManager

NAO_IP = "0.0.0.0"

# Global variable to store the Server module instance
Server = None
memory = None


class ServerModule(ALModule):
    def __init__(self, name):
        ALModule.__init__(self, name)
        # No need for IP and port here because
        # we have our Python broker connected to NAOqi broker

        # Create a proxy to ALTextToSpeech for later use
        self.tts = ALProxy("ALTextToSpeech")
        self.sr = ALProxy("ALSpeechRecognition")
        global memory
        memory = ALProxy("ALMemory")
        # Deberia ser la ip del robot 127.0.0.1, pero lo quito
        # porque en los demas ALProxyes no lo pone
        # self.leds = ALProxy("ALLeds","127.0.0.1",9559)
        self.leds = ALProxy("ALLeds")
#        memory.subscribeToEvent("onWordRecognized")
        
        # Inicializo clases
        self.ac = AccionesNAO(self.tts, self.sr, self.memory, self.leds)
        # TODO: DESCOMENTAR
#        self.dc = DatosCompartidos()
#        self.dc.setData("EXACPALABRA",0.4,False)
#        self.tm = ThreadManager(self.dc)
#        self.disp = Dispatcher(self.dc, self.tm, self.ac)
#        self.es = Escenario(self.dc, self.ac)
#        self.int = Interaccion(self.dc, self.ac)
#        self.tm.addHiloExcluyente("INTERACCION",self.int)
#        self.tm.addHiloExcluyente("ESCENARIO",self.es)
#        self.memory.unsubscribeToEvent(self.getName(), "onWordRecognized")
        time.sleep(1)
        self.ac.decirFrase("Simulacion lanzada")
        time.sleep(1)
        
        self.ac.setLedsOjosRed(False)
        self.ac.setLedsOjosGreen(True)
        self.ac.setLedsOjosBlue(False)
        
        #self.memory.subscribeToEvent("WordRecognized",self.getName(), "onWordRecognized")
#        self.sr.pause(False)
        self.sr.subscribe("TEST_ASR")
        self.sr.setLanguage("Spanish")
        self.sr.setVocabulary(["Me oyes","Si","No","Dime tu glucosa"],False)
        data = (None, 0)
        while not data[0]:
            print str(data)
            data = memory.getData("WordRecognized")
        #stops listening after he hears yes or no
        self.sr.unsubscribe("TEST_ASR")
#        self.sr.subscribe("TEST_ASR")
#        time.sleep(20)
#        data = self.memory.getData("WordRecognized")
#        print data[0]
#        self.sr.unsubscribe("TEST_ASR")
#        try:
#            # join() algun hilo
#            while True:
#                time.sleep(1)
#        except KeyboardInterrupt:
#            print
#            print "Interrupted by user, shutting down"
#            # myBroker.shutdown()
#            sys.exit(0)
            
        
        # TODO: Mensaje a GCloud para arrancar el simulador
        
        # Subscribe to the FaceDetected event:
        

#    def onSpeechRecognized(self, *_args):
#        """ This will be called each time a face is
#        detected.
#
#        """
#        # Unsubscribe to the event when talking,
#        # to avoid repetitions
#        memory.unsubscribeToEvent("FaceDetected",
#            "HumanGreeter")
#
#        self.tts.say("Hello, you")
#
#        # Subscribe again to the event
#        memory.subscribeToEvent("FaceDetected",
#            "HumanGreeter",
#            "onFaceDetected")
    
    def onWordRecognized(self, key, value, message):
        self.ac.palabraReconocida(value[0], value[1])


def main():
    # We need this broker to be able to construct
    # NAOqi modules and subscribe to other modules
    # The broker must stay alive until the program exists
    myBroker = ALBroker("myBroker",
       "0.0.0.0",   # listen to anyone
       0,           # find a free port and use it
       NAO_IP,         # parent broker IP
       9559)       # parent broker port

    # Warning: HumanGreeter must be a global variable
    # The name given to the constructor must be the name of the
    # variable
    global Server
    Server = ServerModule("Server")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print
        print "Interrupted by user, shutting down"
        myBroker.shutdown()
        sys.exit(0)

if __name__ == "__main__":
    main()