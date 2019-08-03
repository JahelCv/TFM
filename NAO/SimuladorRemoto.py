# -*- coding: utf-8 -*-
import requests

class SimuladorRemoto:
    def __init__(self):
        self.urlroot = "http://34.77.125.204:80/"
        self.urlmod = "http://34.77.125.204:80/ModoSimulador/"
        self.urlglu = "http://34.77.125.204:80/Glucosa/"
        self.urlpara = "http://34.77.125.204:80/ParaHilo/"
        self.urldats = "http://34.77.125.204:80/DatosSimulacion/"
        self.urlarranca = "http://34.77.125.204:80/ArrancaHilo/"
        self.urlpausa = "http://34.77.125.204:80/PausaHilo/"
        self.urldespausa = "http://34.77.125.204:80/DespausaHilo/"
    
    def getGlucosaRemoto(self):
        r = requests.get(self.urlglu)
        return float(r.content)
        
    def arrancaSimuladorRemoto(self):
        r = requests.get(self.urlarranca)
        return r.content
        
    def pausaSimuladorRemoto(self):
        r = requests.get(self.urlpausa)
        return r.content
        
    def paraSimuladorRemoto(self):
        r = requests.get(self.urlpara)
        return r.content
    
    def enviaDatosSimulacion(self, b, c, e, e0, e1, e2):
        r = requests.put(self.urldats, json={'bolus' : b, 'cho' : c, 
                'ejercicio' : e, 'exercise' : [e0,e1,e2]})
        if r.ok:
            return True
        else:
            return False