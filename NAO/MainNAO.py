# -*- encoding: UTF-8 -*-
""" Say 'hello, you' each time a human face is detected

"""

import sys
import time

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

from AccionesNAO import AccionesNAO
from DatosCompartidos import DatosCompartidos
from Dispatcher import Dispatcher
from Escenario import Escenario
from Interaccion import Interaccion
from ThreadManager import ThreadManager

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
        self.memory = ALProxy("ALMemory")
#        memory.subscribeToEvent("onWordRecognized")
        
        # Inicializo clases
        self.ac = AccionesNAO(self.tts, self.sr, self.memory)
        self.dc = DatosCompartidos()
        self.dc.setData("EXACPALABRA",0.4,False)
        self.tm = ThreadManager(self.dc)
        self.disp = Dispatcher(self.dc, self.ac)
        self.es = Escenario(self.dc, self.ac)
        self.int = Interaccion(self.dc, self.ac)
        # TODO: Ver que hago con el TCPServer(...)
        self.tm.addHiloExcluyente("INTERACCION",self.int)
        self.tm.addHiloExcluyente("ESCENARIO",self.es)
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



