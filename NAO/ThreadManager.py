# -*- coding: utf-8 -*-
from DatosCompartidos import DatosCompartidos
from multiprocessing import Lock
from time import time

PARADO = 0
CORRIENDO = 1
PAUSADO = 2 

class ThreadManager():
    def __init__(self, d):
        self.hiloExcluyenteCorriendo = None
        self.mutex = Lock()
        self.hilos = {}
        self.hilosExcluyentes = {}
        self.datosC = d
        
    def addHilo(self, id, rclass):
        ret = 1
        self.mutex.acquire()
        if self.isHilo(id):
            ret = -2
        else:
            self.hilos[id] = rclass
        self.mutex.release()
        return ret

    def addHiloExcluyente(self, id, rclass):
        ret = 1
        self.mutex.acquire()
        if self.isHilo(id):
            ret = -2
        else:
            self.hilos[id] = rclass
        self.mutex.release()
        return ret
        
    def setDatosCompartidos(self, d):
        if self.datosC != None:
            self.datosC = d
            self.datosC.setData('ESTADOHILOS','',True)
            return 1
        return -1
        
    def restart(self, id):
        time.sleep(1)
        self.parar(id)
        time.sleep(1)
        self.arrancar(id)
        time.sleep(2)
        
    def arrancar(self, id):
        ret = -1
        self.mutex.acquire()
        # Si el hilo ya esta y no esta corriendo, lo arranca
        if id in self.hilos.keys():
            h = self.hilos.get(id)
            if h.getEstado() != CORRIENDO:
                h.start()
                self.actualizarDatosEstadoHilos()
                ret = 1
        # Si el hilo excluyente no esta corriendo...
        if self.hiloExcluyenteCorriendo == None or self.hiloExcluyenteCorriendo == '':
            if id in self.hilosExcluyentes.keys():
                h = self.hilosExcluyentes.get(id)
                if h.getEstado() != CORRIENDO:
                    h.start()
                    self.hiloExcluyenteCorriendo = id
                    self.actualizarDatosEstadoHilos()
                    ret = 1
        # Pero si esta corriendo uno pos ya nada
        else:
            ret = -2
        self.mutex.release()
        return ret
        
    def parar(self,id):
        ret = -1
        self.mutex.acquire()
        # Si el hilo ya esta y no esta corriendo, lo arranca
        if id in self.hilos.keys():
            h = self.hilos.get(id)
            if h.getEstado() != PARADO:
                h.pararThread()
                h.join()
                self.actualizarDatosEstadoHilos()
                ret = 1
        if id in self.hilosExcluyentes.keys():
            h = self.hilosExcluyentes.get(id)
            if h.getEstado() != PARADO:
                h.pararThread()
                h.join()
                self.hiloExcluyenteCorriendo = None
                self.actualizarDatosEstadoHilos()
                ret = 1
        self.mutex.release()
        return ret
        
    def pausar(self, id):    
        ret = -1
        self.mutex.acquire()
        if id in self.hilos.keys():
            h = self.hilos.get(id)
            if h.getEstado() != PARADO:
                h.pausar()
                self.actualizarDatosEstadoHilos()
                ret = 1
        if id in self.hilosExcluyentes.keys():
            h = self.hilosExcluyentes.get(id)
            if h.getEstado() != PARADO:
                h.pausar()
                self.actualizarDatosEstadoHilos()
                ret = 1
        self.mutex.release()
        return ret
        
    def desPausar(self, id):
        ret = -1
        self.mutex.acquire()
        if id in self.hilos.keys():
            h = self.hilos.get(id)
            if h.getEstado() != PARADO:
                h.desPausar()
                self.actualizarDatosEstadoHilos()
                ret = 1
        if id in self.hilosExcluyentes.keys():
            h = self.hilosExcluyentes.get(id)
            if h.getEstado() != PARADO:
                h.desPausar()
                self.actualizarDatosEstadoHilos()
                ret = 1
        self.mutex.release()
        return ret
        
    def isHilo(self, id):
        if id in self.hilos.keys():
            return True
        if id in self.hilosExcluyentes.keys():
            return True
        return False
        
    def getEstadoHilos(self):
        res = ''
        for i in self.hilos.keys():
            res = res + str(i) + ':' + self.hilos.get(i) + ','
        res = res + '%'
        for i in self.hilosExcluyentes.keys():
            res = res + str(i) + ':' + self.hilosExcluyentes.get(i) + ','
            
#        if(hilosExcluyentes.size() > 0)
#        estadoHilos = estadoHilos.substr(0, estadoHilos.size()-1);
        return res
        
    def actualizarDatosEstadoHilos(self):
        if self.datosC != None:
            self.datosC.modifyData('ESTADOHILOS', self.getEstadoHilos())