# -*- coding: utf-8 -*-
from multiprocessing import Lock

class EncolaSimuladores:
    def __init__(self):
        self.s = {}
        self.mutex= Lock()
        self.nextID = 0
        self.limiteNAOs = 10
        
    def isID(self, id):
        self.mutex.acquire()
        ret = id in self.s.keys()
        self.mutex.release()
        return ret
        
    def anyadirNAO(self, n):
        self.mutex.acquire()
        self.s[self.nextID] = n
        ret = self.nextID
        self.nextID = (self.nextID + 1) % self.limiteNAOs
        self.mutex.release()
        return ret
        
    def quitarNAO(self, id):
        self.mutex.acquire()
        del self.s[id]
        self.mutex.release()