# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 20:15:01 2019

@author: Jahel
"""
from threading import Lock, Condition

class AccionesNAO():
    def __init__(self, proxytts, proxysr, proxymem):
        self.mutex = Lock()
        self.cond = Condition()
        # TODO: Borrar
        print 'Acciones NAO creado'
        self.tts = proxytts
        self.sr = proxysr
        self.mem = proxymem
        
    def palabraReconocida(self, p, e):
        self.mutex.acquire()
        if self.isWaitingWord and (not self.isTalking):
            self.isWaitingWord = False
            self.exact = e
            self.palabra = self.palabra + p
            print 'Palabra reconocida: ' + self.palabra
            self.cond.acquire()
            self.cond.notifyAll()
            self.cond.release()
        self.mutex.release()