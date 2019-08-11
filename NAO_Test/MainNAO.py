# -*- encoding: UTF-8 -*-
""" Say 'hello, you' each time a human face is detected

"""

import sys
import time
from threading import Thread

from AccionesNAO import AccionesNAO
# TODO: Descomentar
from DatosCompartidos import DatosCompartidos
from SimuladorRemoto import SimuladorRemoto
from DispatchMQTT import DispatchMQTT
from Escenario import Escenario
from Interaccion import Interaccion

ip = "andy.local"

# Global variable to store the Server module instance
Server = None

class ServerModule(object):
    def __init__(self):
        
        # Inicializo clases
        self.ac = AccionesNAO()      
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
        self.dc.setData("EXACPALABRA",0.4)
        
        # Crea el que atiende a los subscriptores
        self.dmqtt = DispatchMQTT(self.ac, self.dc)
        
        # El que interactua de verdad con el usuario
        self.es = Escenario(self.dc, self.ac, self.simremoto)
        self.dc.addHiloExcluyente("ESCENARIO", self.es)
        self.dmqtt.publicaInterfazHilosMQTT("ESCENARIO,"+self.dc.getEstadoHiloExcluyente("ESCENARIO"))
        
        self.inte = Interaccion(self.dc, self.ac, self.simremoto)
        self.dc.addHiloExcluyente("INTERACCION", self.inte)
        self.dmqtt.publicaInterfazHilosMQTT("INTERACCION,"+self.dc.getEstadoHiloExcluyente("INTERACCION"))
        
    
    def onWordRecognized(self, key, value, message):
        self.ac.palabraReconocida(value[0], value[1])

def main():
    Server = ServerModule()

    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        print "Interrupted by user, shutting down"
        Server.dmqtt.pararMQTT()
        sys.exit(0)

if __name__ == "__main__":
    main()