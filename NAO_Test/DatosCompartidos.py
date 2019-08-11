from threading import Lock
import time

class DatosCompartidos():
    def __init__(self):
        # Los mutex
        self.mutex = Lock()
        self.mutexsim = Lock()
        self.mutexHilosExc = Lock()
        
        # Diccionario o map
        self.datosSim = {'bolus' : 0.0, 'cho' : 0, 'ejercicio' : False,
                         'exercise' : [0,0,0]}
        self.datos = {} #Inicialmente esta vacio
        
        # Aqui ira toda la informacion de los hilos ESCENARIO E INTERACCION (de momento)
        # Es un diccionario que tiene key = el ID ("ESCENARIO" o "INTERACCION")
        # y de valor = list(el objeto en si en posicion 0 y el estado el posicion 1)
        # siendo el estado = "PARADO", "CORRIENDO" o "PAUSADO"
        self.hilosExcluyentes = {}
        self.hiloExcluyenteCorriendo = None

    # suponiendo que no existe previamente
    def setData(self, id, data):
        aux = -1
        self.mutex.acquire()
        if not (id in self.datos.keys()):
            self.datos[id] = data
            aux = 1
        self.mutex.release()
        return aux
        
    # suponiendo que existe previamente
    def modifyData(self,id, data):
        aux = -1
        self.mutex.acquire()
        if id in self.datos.keys():
            self.datos[id] = data
            aux = 1
        self.mutex.release()
        return aux

    #devuelve -1 si el dato no existe 
    def getData(self, id):
        aux = -1
        self.mutex.acquire()
        if id in self.datos.keys():
            aux = self.datos.get(id)    
        self.mutex.release()
        return aux

    def deleteData(self, id):
        self.mutex.acquire()
        if id in self.datos.keys():
            self.datos.pop(id)    
        self.mutex.release()
        
    ##################################################################
    ############# Sobre hilos excluyentes ############################
    ##################################################################
        
    def isHiloExcluyente(self, id):
        ret = False
        if id in self.hilosExcluyentes.keys():
            ret = True
        return ret
        
    def addHiloExcluyente(self, id, rclass):
        ret = True
        self.mutexHilosExc.acquire()
        if self.isHiloExcluyente(id):
            ret = False
        else:
            self.hilosExcluyentes[id] = [rclass, "PARADO"]
        self.mutexHilosExc.release()
        return ret
    
    def modificaEstadoHiloExcluyente(self, id, estado):
        ret = True
        self.mutexHilosExc.acquire()
        if self.isHiloExcluyente(id):
            self.hilosExcluyentes[id][1] = estado
            ret = True
        self.mutexHilosExc.release()
        return ret
        
    def getEstadoHiloExcluyente(self, id):
        res = ''
        self.mutexHilosExc.acquire()
        if self.isHiloExcluyente(id):
            res = self.hilosExcluyentes[id][1]
        self.mutexHilosExc.release()
        return res
        
    def restartHiloExcluyente(self, id):
        self.mutexHilosExc.acquire()
        time.sleep(1)
        self.hilosExcluyentes[id][0].parar()
        time.sleep(1)
        self.hilosExcluyentes[id][0].arrancar()
        time.sleep(2)
        self.mutexHilosExc.release()
        
    def arrancarHiloExcluyente(self, id):
        ret = True
        self.mutexHilosExc.acquire()
        if self.hiloExcluyenteCorriendo == None or self.hiloExcluyenteCorriendo == '':
            if id in self.hilosExcluyentes.keys():
                h = self.hilosExcluyentes[id][0]
                if self.hilosExcluyentes[id][1] == "PARADO":
                    self.hilosExcluyentes[id][1] = "CORRIENDO"
                    self.hiloExcluyenteCorriendo = id
                    h.startThread()
                    ret = True
        # Pero si esta corriendo uno pos ya nada
        else:
            ret = False
        self.mutexHilosExc.release()
        return ret
        
    def pararHiloExcluyente(self,id):
        ret = False
        self.mutexHilosExc.acquire()
        print 'DatosCompartidos - Para hilo excluyente'
        if id in self.hilosExcluyentes.keys():
            h = self.hilosExcluyentes[id][0]
            if self.hilosExcluyentes[id][1] != "PARADO":
                h.pararThread()
                self.hiloExcluyenteCorriendo = None
                self.hilosExcluyentes[id][1] = "PARADO"
                ret = True
        self.mutexHilosExc.release()
        return ret
        
    def pausarHiloExcluyente(self, id):    
        ret = False
        self.mutexHilosExc.acquire()
        if id in self.hilosExcluyentes.keys():
            h = self.hilosExcluyentes[id][0]
            if self.hilosExcluyentes[id][1] != "PARADO":
                h.pausar()
                ret = True
        self.mutexHilosExc.release()
        return ret
        
    def desPausarHiloExcluyente(self, id):
        ret = False
        self.mutexHilosExc.acquire()
        if id in self.hilosExcluyentes.keys():
            h = self.hilosExcluyentes[id][0]
            if self.hilosExcluyentes[id][1] != "PARADO":
                h.desPausar()
                ret = True
        self.mutexHilosExc.release()
        return ret