# -*- coding: utf-8 -*-
#from __future__ import print_function
from flask import Flask, request
from flask_restful import Resource, Api
from Simulador import Simulador
from threading import Thread

app = Flask(__name__)
api = Api(app)
s = Simulador()    

class HelloWorld(Resource):
    def get(self):
        return "Bienvenido!"
        
class ModoSimulador(Resource):
    def get(self):
        return s.getModo()
    def put(self):
        return s.setModo(request.form['data'])
        
class Glucosa(Resource):
    def get(self):
        return s.getGlucosa()
    def put(self):
        return s.setGlucosa(request.form['data'])
        
class ArrancaHilo(Resource):
    def get(self):
        t = Thread(target=s.run)
        t.start()
        
class ParaHilo(Resource):
    def get(self):
        return s.pararSimulador()

api.add_resource(HelloWorld, '/')
api.add_resource(ArrancaHilo, '/ArrancaHilo/')
api.add_resource(ParaHilo, '/ParaHilo/')
api.add_resource(ModoSimulador, '/ModoSimulador/')
api.add_resource(Glucosa, '/Glucosa/')

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=80, debug=True)