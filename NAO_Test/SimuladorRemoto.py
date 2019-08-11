# -*- coding: utf-8 -*-
import requests
from threading import Lock

class SimuladorRemoto:
    def __init__(self):
        self.mutex = Lock()
        self.urlroot = "http://34.76.240.69:80/"
        self.urlmod = "http://34.76.240.69:80/ModoSimulador/"
        self.urlglu = "http://34.76.240.69:80/Glucosa/"
        self.urlpara = "http://34.76.240.69:80/ParaHilo/"
        self.urldats = "http://34.76.240.69:80/DatosSimulacion/"
        self.urlarranca = "http://34.76.240.69:80/ArrancaHilo/"
        self.urlpausa = "http://34.76.240.69:80/PausaHilo/"
        self.urldespausa = "http://34.76.240.69:80/DespausaHilo/"
    
    def getGlucosaRemoto(self):
        self.mutex.acquire()
        r = requests.get(self.urlglu)
        self.mutex.release()
        return float(r.content)
        
    def arrancaSimuladorRemoto(self):
        self.mutex.acquire()
        r = requests.get(self.urlarranca)
        self.mutex.release()
        return r.content
        
    def pausaSimuladorRemoto(self):
        self.mutex.acquire()
        r = requests.get(self.urlpausa)
        self.mutex.release()
        return r.content
        
    def paraSimuladorRemoto(self):
        self.mutex.acquire()
        r = requests.get(self.urlpara)
        self.mutex.release()
        return r.content
    
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