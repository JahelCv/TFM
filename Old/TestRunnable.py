# -*- coding: utf-8 -*-
from multiprocessing import Lock
import time 
from Runnable import Runnable
import sys

class Consumidor(Runnable):
    def setdatoc(self,datoc):
        self.datoc = datoc
        
    def run(self):
        cont = 20
        while(cont > 0):
            time.sleep(1)
            res = self.datoc.res()
            print 'Consumidor ha dejado el contador a: ' + str(res)
#            if res <= 0:
#                print 'Consumidor - Se autopausa'
#                self.pausar()
            cont = cont - 1
        
    def empezar(self):
        self.start()

class Productor(Runnable):
    def setdatoc(self,datoc):
        self.datoc = datoc
    
    def run(self):
        cont = 20
        while(cont > 0):
            time.sleep(2)
            inc = self.datoc.inc()
            print 'Productor ha dejado el contador a: ' + str(inc)
#            if inc > 5:
#                print 'Productor - Se autopausa'
#                self.pausar()
            cont = cont - 1
        
    def empezar(self):
        self.start()
    
class DatoCompartido():
    def __init__(self):
        self.n = 0
        self.mut = Lock()
    
    def inc(self):
        aux = 0
        self.mut.acquire()
        self.n = self.n + 1
        aux = self.n
        self.mut.release()
        return aux
        
    def res(self):
        aux = 0
        self.mut.acquire()
        self.n = self.n - 1
        aux = self.n
        self.mut.release()
        return aux
    
    def get(self):
        aux = 0
        self.mut.acquire()
        aux = self.n
        self.mut.release()
        return aux
        
if __name__ == "__main__":
    d = DatoCompartido()
    c = Consumidor()
    c.setdatoc(d)
    p = Productor()
    p.setdatoc(d)
    c.empezar()
    p.empezar()
    cont = 10
    while(cont > 0):
        time.sleep(0.5)
        cont = cont - 1
        num = d.get()
        if num <= 0:
            print str(cont) + ') Main - Numero negativo ' + str(num) +', despauso el productor'
            c.pausar()
            p.desPausar()
        else:
            print str(cont) + ') Main - Numero positivo ' + str(num) +', despauso el consumidor'
            c.desPausar()
            if num >=5:
                p.pausar()
            
    sys.exit()
    