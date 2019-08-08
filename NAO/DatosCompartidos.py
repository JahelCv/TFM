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
        self.datos = {'ESTADOHILOS':''} #Inicialmente esta vacio
        self.hilosExcluyentes = {}
        self.hiloExcluyenteCorriendo = None
        
        # Lista o vector
        self.datosEnviables = []

    # suponiendo que no existe previamente
    def setData(self, id, data, env):
        aux = -1
        self.mutex.acquire()
        if not (id in self.datos.keys()):
            self.datos[id] = data
            aux = 1
            if env == True:
                self.datosEnviables.append(id)
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
    
    def getDatosEnviables(self):    
        self.mutex.acquire()
        aux = self.datosEnviables
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
        
    # Sobre datos de simulacion
    def setDatosSimulacion(self,bolus,cho,ejercicio,ejTiempo,ejIntesidad,ejDuracion):
        self.mutexsim.acquire()
        self.datosSim['bolus'] = bolus
        self.datosSim['cho'] = cho
        self.datosSim['ejercicio'] = False
        # exercise = ejerciciotiempo, ejercicioIntesidad, ejercicioDuracion
        self.datosSim['exercise'] = [ejTiempo,ejIntesidad,ejDuracion]
        self.mutexsim.release()
        
    def getDatosSimulacion(self):
        self.mutexsim.acquire()
        aux = self.datosSim
        self.datosSim = {'bolus' : 0.0, 'cho' : 0, 'ejercicio' : False,
                         'exercise' : [0,0,0]}
        self.mutexsim.release()
        return aux
        
    # Sobre hilos excluyentes
    def isHiloExcluyente(self, id):
        ret = False
        self.mutexHilosExc.acquire()
        if id in self.hilosExcluyentes.keys():
            ret = True
        self.mutexHilosExc.release()
        return ret
        
    def addHiloExcluyente(self, id, rclass):
        ret = True
        self.mutexHilosExc.acquire()
        if self.isHiloExcluyente(id):
            ret = False
        else:
            self.hilosExcluyentes[id] = rclass
        self.mutexHilosExc.release()
        return ret
        
    def getEstadoHilosExcluyente(self):
        res = ''
        self.mutexHilosExc.acquire()
        for i in self.hilosExcluyentes.keys():
            res = res + str(i) + ':' + self.hilosExcluyentes[i].getEstado() + ','
        self.mutexHilosExc.release()
        return res
        
    def restartHiloExcluyente(self, id):
        self.mutexHilosExc.acquire()
        time.sleep(1)
        self.hilosExcluyentes[id].parar()
        time.sleep(1)
        self.hilosExcluyentes[id].arrancar()
        time.sleep(2)
        self.mutexHilosExc.release()
        
    def arrancarHiloExcluyente(self, id):
        ret = True
        self.mutexHilosExc.acquire()
        # Si el hilo excluyente no esta corriendo...
        if self.hiloExcluyenteCorriendo == None or self.hiloExcluyenteCorriendo == '':
            if id in self.hilosExcluyentes.keys():
                h = self.hilosExcluyentes[id]
                if h.getEstado() != "CORRIENDO":
                    h.start()
                    self.hiloExcluyenteCorriendo = id
                    self.actualizarDatosEstadoHilos()
                    ret = True
        # Pero si esta corriendo uno pos ya nada
        else:
            ret = False
        self.mutexHilosExc.release()
        return ret
        
    def pararHiloExcluyente(self,id):
        ret = False
        self.mutexHilosExc.acquire()
        if id in self.hilosExcluyentes.keys():
            h = self.hilosExcluyentes.get(id)
            if h.getEstado() != "PARADO":
                h.pararThread()
                h.join()
                self.hiloExcluyenteCorriendo = None
                self.actualizarDatosEstadoHilos()
                ret = True
        self.mutexHilosExc.release()
        return ret
        
    def pausarHiloExcluyente(self, id):    
        ret = False
        self.mutexHilosExc.acquire()
        if id in self.hilosExcluyentes.keys():
            h = self.hilosExcluyentes[id]
            if h.getEstado() != "PARADO":
                h.pausar()
                self.actualizarDatosEstadoHilos()
                ret = True
        self.mutexHilosExc.release()
        return ret
        
    def desPausarHiloExcluyente(self, id):
        ret = False
        self.mutexHilosExc.acquire()
        if id in self.hilosExcluyentes.keys():
            h = self.hilosExcluyentes.get(id)
            if h.getEstado() != "PARADO":
                h.desPausar()
                self.actualizarDatosEstadoHilos()
                ret = True
        self.mutexHilosExc.release()
        return ret
        
    def actualizarDatosEstadoHilos(self):
        self.modifyData('ESTADOHILOS', self.getEstadoHilos())