#!/usr/bin/python
from __future__ import print_function
import sys
import json
from flask import Flask, request
from gevent.pywsgi import WSGIServer
from flask_restful import Resource, Api
from Simulador import Simulador

app = Flask(__name__)
api = Api(app)
s = None 

class HelloWorld(Resource):
    def get(self):
        return "Bienvenido!"
        
class Hilo(Resource):
    def get(self):
        global s
        if s == None:
            return "PARADO"
        else:
            return s.getEstadoHilo()
            
    # PARADO, PAUSADO, CORRIENDO
    def put(self):
        global s
        if request.form['data'] == "PARADO":
            if s != None:
                return s.pararSimulador()
                del s
                s = None
            else:
                return False
            
        elif request.form['data'] == "PAUSADO":
            if s != None:
                return s.pausarSimulador()
            else:
                return False
            
        elif request.form['data'] == "CORRIENDO":
            if s == None:
                s = Simulador()
                s.arrancarSimulador()
            else:
                if s.getEstadoHilo() == "PARADO":
                    s.arrancarSimulador()
                elif s.getEstadoHilo() == "PAUSADO":
                    s.despausarSimulador()
            return True
            
        return False
        
        
class ModoSimulador(Resource):
    def get(self):
        global s
        return s.getModo()
    def put(self):
        global s
        #print('Put sobre modosimulador: ',file=sys.stdout)
        #print(str(request.form))
        return s.setModo(request.form['data'])
        
class Glucosa(Resource):
    def get(self):
        global s
        if s != None:
            return s.getGlucosa()
        else:
            return False        

class DatosSimulacion(Resource):
    def get(self):
        global s
        return s.getDatosSimulacion()
        
    def put(self):
        global s
        content = request.form['data']
        print(content, file=sys.stdout)
        jsoncont = json.loads(content.replace("'", "\""))
        if s != None:
            return s.setDatosSimulacion(jsoncont)
        else:
            return False

api.add_resource(HelloWorld, '/')
api.add_resource(Hilo, '/Hilo/')
api.add_resource(ModoSimulador, '/Simulador/Modo/')
api.add_resource(Glucosa, '/Simulador/Glucosa/')
api.add_resource(DatosSimulacion, '/Simulador/DatosSimulacion/')

if __name__ == '__main__':
    http_server = WSGIServer(('', 8080), app)
    http_server.serve_forever()