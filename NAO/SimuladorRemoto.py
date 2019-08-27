# -*- coding: utf-8 -*-
import requests
from threading import Lock

class SimuladorRemoto:
    def __init__(self):
        self.mutex = Lock()
        self.urlroot = "http://34.76.240.69:8080/"
        self.urlglu = "http://34.76.240.69:8080/Simulador/Glucosa/"
        self.urldats = "http://34.76.240.69:8080/Simulador/DatosSimulacion/"
        self.urlhilo = "http://34.76.240.69:8080/Hilo/"
    
    def getGlucosaRemoto(self):
        self.mutex.acquire()
        r = requests.get(self.urlglu)
        self.mutex.release()
        return float(r.content)
        
    def arrancaSimuladorRemoto(self):
        self.mutex.acquire()
        r = requests.put(self.urlhilo, data={'data': "CORRIENDO"})
        self.mutex.release()
        if r.ok:
            return True
        else:
            return False
        
    def pausaSimuladorRemoto(self):
        self.mutex.acquire()
        r = requests.put(self.urlhilo, data={'data': "PAUSADO"})
        self.mutex.release()
        if r.ok:
            return True
        else:
            return False
            
    def despausaSimuladorRemoto(self):
        self.mutex.acquire()
        r = requests.put(self.urlhilo, data={'data': "CORRIENDO"})
        self.mutex.release()
        if r.ok:
            return True
        else:
            return False
        
    def paraSimuladorRemoto(self):
        self.mutex.acquire()
        r = requests.put(self.urlhilo, data={'data': "PARADO"})
        self.mutex.release()
        if r.ok:
            return True
        else:
            return False
    
    def enviaDatosSimulacion(self, b, c, e, e0, e1, e2):
        self.mutex.acquire()
        if e:
            aux_e = 'true'
        else:
            aux_e = 'false'
        msg = "{\'bolus\' : " + str(b) + ", \'cho\' : " + str(c) + ", \'ejercicio\' :" + aux_e + ", \'exercise\' : ["+ str(e0) + "," + str(e1) + "," + str(e2) + "]}"
        r = requests.put(self.urldats, data={'data': msg})
        self.mutex.release()
        if r.ok:
            return True
        else:
            return False