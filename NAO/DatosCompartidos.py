from threading import Lock

class DatosCompartidos():
    def __init__(self):
        self.mutex = Lock()
        self.mutexsim = Lock()
        self.datosSim = {'bolus' : 0.0, 'cho' : 0, 'ejercicio' : False,
                         'exercise' : [0,0,0]}
        # Diccionario o map
        self.datos = {}
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