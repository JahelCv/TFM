# -*- coding: utf-8 -*-
from threading import Thread, Condition
from datetime import datetime
# from multiprocessing import Lock
# No Lock necessary -> 
# https://www.bogotobogo.com/python/Multithread/python_multithreading_Synchronization_Condition_Objects_Producer_Consumer.php

PARADO = 0
CORRIENDO = 1
PAUSADO = 2 

class Runnable(object):
    
    def __init__(self):
        #define PARADO 0
        #define CORRIENDO 1
        #define PAUSADO 2         
        self.estado = PARADO
        self.hilo = None
        self.pausa = False
        self.cond = Condition()
        #self.mut = Lock()

    ##### SOBREESCRIBIR ESTOS METODOS ######
    def run(self):
        print 'Run - El del Runnable'
        
    def pausar(self):
        print 'Pausar: Se despausa'
    
    def desPausar(self):
        print 'DesPausar - El del Runnable '
        
    def pararThread(self):
        print 'PararThread - El del Runnable'
    ########################################
    
    def start(self):
        if self.estado != CORRIENDO and self.estado != PAUSADO and self.hilo == None:
            self.hilo = Thread(target=self.run)
            self.hilo.start()
            self.estado = 1
            return 1
        return -1
    
    def getHilo(self):
        return self.hilo
    
    def esperarCondicion(self):
        self.pausa = True
        self.estado = PAUSADO
        self.cond.acquire()
        while(self.pausa):
            self.cond.wait()
        self.cond.release()
    
    def liberarCondicion(self):
        self.cond.acquire()
        self.estado = CORRIENDO
        self.pausa = False
        self.cond.notify()
        self.cond.release()
    
    def setEstadoHilo(self, e):
        self.estado = e
    
    def join(self):
        if(self.hilo != None):
            print 'parada'
            self.hilo.join()
            print 'salimos join'
            self.estado = PARADO
            del self.hilo
            self.hilo = None
            return 1
        return -1
    
    def getEstado(self):
        return self.estado