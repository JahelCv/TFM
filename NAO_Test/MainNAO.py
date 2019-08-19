# -*- encoding: UTF-8 -*-
""" Say 'hello, you' each time a human face is detected

"""

import sys
import time
from threading import Thread
from requests import exceptions

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
            self.dmqtt.publicaInterfazHilosMQTT("ESCENARIO,"+self.dc.getEstadoHiloExcluyente("ESCENARIO"))
            print 'Hago un publish al mqtt del ESCENARIO' 
            
            self.inte = Interaccion(self.dc, self.ac, self.simremoto, self.dmqtt)
            print 'Creo Interaccion'
            self.dc.addHiloExcluyente("INTERACCION", self.inte)
            print 'Anyado INTERACCION como hilo excluyente'
            self.dmqtt.publicaInterfazHilosMQTT("INTERACCION,"+self.dc.getEstadoHiloExcluyente("INTERACCION"))
            print 'Hago un publish al mqtt del INTERACCION'
            self.ac.decirFrase("Módulo arrancado exitosamente.")
        except exceptions.ConnectionError:
            print "MainNAO # Exception!"
            if self.ac.isWaitingWord:
                self.memory.unsubscribeToEvent("WordRecognized", "Server")
            self.dmqtt.publicaInterfazHilosMQTT("ESCENARIO,PARADO")
            self.dmqtt.publicaInterfazHilosMQTT("INTERACCION,PARADO")
            self.dmqtt.pararMQTT()
            self.ac.decirFrase('No se ha podido conectar con el servicio en la nube, detengo el proceso.')
            sys.exit(0)
        except Exception:
            print "MainNAO # Exception!"
            if self.ac.isWaitingWord:
                self.memory.unsubscribeToEvent("WordRecognized", "Server")
            self.dmqtt.publicaInterfazHilosMQTT("ESCENARIO,PARADO")
            self.dmqtt.publicaInterfazHilosMQTT("INTERACCION,PARADO")
            self.dmqtt.pararMQTT()
            self.ac.decirFrase('Ha ocurrido algún problema, detengo el proceso.')
            sys.exit(0)
        
    
    def onWordRecognized(self, key, value, message):
        self.ac.palabraReconocida(value[0], value[1])

def main():
    Server = ServerModule()

    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        print "Interrupted by user, shutting down"
        Server.dmqtt.publicaInterfazHilosMQTT("ESCENARIO,PARADO")
        Server.dmqtt.publicaInterfazHilosMQTT("INTERACCION,PARADO")
        Server.ac.decirFrase('Corto el módulo manualmente.')
        Server.dmqtt.pararMQTT()
        sys.exit(0)

if __name__ == "__main__":
    main()