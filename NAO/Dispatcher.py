# -*- coding: utf-8 -*-
from Runnable import Runnable

PARADO = 0
CORRIENDO = 1
PAUSADO = 2 

class Escenario(Runnable):
    def __init__(self, d, ac):
        super().__init__() 
        self.datos = d
        self.acNAO = ac
        
    def setDatosCompartidos(self, d):
        self.datos = d
        
    def setAccionesNAO(self, ac):
        self.acNAO = ac