from multiprocessing import Lock

# Datos del simulador
class DatosSimulador():
    def __init__(self):
        self.bolus = 0
        self.cho = 0
        self.ejercicioTiempo = 0
        self.ejercicioIntesidad = 0
        self.ejercicioDuracion = 0
        self.ejercicio = False
        
    def setDatosSimulacion(self,bolus,cho,ejercicio,ejTiempo,ejIntesidad,ejDuracion):
        self.bolus = bolus
        self.cho = cho
        self.ejercicioTiempo = ejTiempo
        self.ejercicioIntesidad = ejIntesidad
        self.ejercicioDuracion = ejDuracion
        self.ejercicio = ejercicio
        
# Clase principal de compartidos
class DatosCompartidos():
    
    def __init__(self):
        self.mutex = Lock()
        self.mutexsim = Lock()
        self.datosSim = DatosSimulador()
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
        self.datosSim.setDatosSimulacion(bolus,cho,ejercicio,ejTiempo,ejIntesidad,ejDuracion)
        self.mutexsim.release()
        
    def getDatosSimulacion(self):
        self.mutexsim.acquire()
        aux = self.datosSim
        self.datosSim.setDatosSimulacion(0,0,False,0,0,0)
        self.mutexsim.release()
        return aux