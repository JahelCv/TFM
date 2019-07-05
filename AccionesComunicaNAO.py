# -*- coding: utf-8 -*-
from multiprocessing import Lock
from collections import deque

class AccionesComunicaNAO():
    def __init__(self):
        self.isWaitingWord = False
        self.isTalking = False
        self.isMoving = False
        # variable que indica si un thread quiere uso exclusivo
        self.isThreadBlock = False
        self.exact = -1
        self.palabra = ''
        self.mutBlock = Lock()
        self.mut = Lock()
        self.mutHablar = Lock() # en decirFrase
        self.mutexAcciones = Lock()

    def setThreadBock(self,flag):
        self.mutBlock.acquire()
        self.isThreadBlock = flag
        self.mutBlock.release()

    def getThreadBlock(self):
        self.mutBlock.acquire()
        aux = self.isThreadBlock
        self.mutBlock.release()
        return aux
    
    # Se omiten para el server de esta parte setParentBroker,
    # getDCMCycleTime y configurarGruposLeds. Al ser librerías 
    # de NAO, deben ir en el robot
    
    # Se recibe una dequeue y se retorna una tupla (resp, palabra, exac)
    def esperarPalabra(self, dq, sec):
        # TODO: Aquí se debe comunicar con el robot para enviar
        # peticion y recibir palabra escuchada
        print 'Se ejecuta acNAO.esperarPalabra'
        return (1,'palabra',self.exact)
    
    def decirFrase(self,frase):
        # TODO: Comunicacion con robot
        self.mutHablar.acquire()
        print 'Se ejecuta acNAO.decirFrase: ' + frase
        self.mutHablar.release()
        return frase
        
    def accionMedirGlucosa(self):
        # TODO: Comunicacion con robot
        print 'Se ejecuta acNAO.accionMedirGlucosa'
        return 'Se ejecuta acNAO.accionMedirGlucosa'
        
    def accionComer(self):
        # TODO: Comunicacion con robot
        print 'Se ejecuta acNAO.accionComer'
        return 'Se ejecuta acNAO.accionComer'
        
    def accionPinchate(self):
        # TODO: Comunicacion con robot
        print 'Se ejecuta acNAO.accionPinchate'
        return 'Se ejecuta acNAO.accionPinchate'
        
    def accionLevantarse(self):
        # TODO: Comunicacion con robot
        print 'Se ejecuta acNAO.accionLevantarse'
        return 'Se ejecuta acNAO.accionLevantarse'
        
    def accionCorrer(self):
        # TODO: Comunicacion con robot
        print 'Se ejecuta acNAO.accionCorrer'
        return 'Se ejecuta acNAO.accionCorrer'
        
    def posicionParada(self):
        # TODO: Comunicacion con robot
        print 'Se ejecuta acNAO.posicionParada'
        return 'Se ejecuta acNAO.posicionParada'
        
    def setLedsOjosBlue(self, onoff):
        # TODO: Comunicacion con robot
        print 'Se ejecuta acNAO.setLedsOjosBlue: ' + str(onoff)
        return 'Se ejecuta acNAO.setLedsOjosBlue'  + str(onoff)
        
    def setLedsOjosRed(self, onoff):
        # TODO: Comunicacion con robot
        print 'Se ejecuta acNAO.setLedsOjosRed: ' + str(onoff)
        return 'Se ejecuta acNAO.setLedsOjosRed'  + str(onoff)
        
    def setLedsOjosGreen(self, onoff):
        # TODO: Comunicacion con robot
        print 'Se ejecuta acNAO.setLedsOjosGreen: ' + str(onoff)
        return 'Se ejecuta acNAO.setLedsOjosGreen'  + str(onoff)
        
    def accionSaludo(self, num):
        # TODO: Comunicacion con robot
        print 'Se ejecuta acNAO.accionSaludo: ' + str(num)
        return 'Se ejecuta acNAO.accionSaludo'  + str(num)
        
    def accionDespedida(self, num):
        # TODO: Comunicacion con robot
        print 'Se ejecuta acNAO.accionDespedida: ' + str(num)
        return 'Se ejecuta acNAO.accionDespedida'  + str(num)
    
    def accionQUETALESTAS(self, num):
        # TODO: Comunicacion con robot
        print 'Se ejecuta acNAO.accionQUETALESTAS: ' + str(num)
        return 'Se ejecuta acNAO.accionQUETALESTAS'  + str(num)
        
    def accionChocarMano(self):
        # TODO: Comunicacion con robot
        print 'Se ejecuta acNAO.accionChocarMano'
        return 'Se ejecuta acNAO.accionChocarMano'
        
    def accionTumbarse(self):
        # TODO: Comunicacion con robot
        print 'Se ejecuta acNAO.accionTumbarse'
        return 'Se ejecuta acNAO.accionTumbarse'