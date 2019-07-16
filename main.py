import webapp2
from EncolaSimuladores import EncolaSimuladores
# from Simulador import Simulador

es = EncolaSimuladores()

class MainPage(webapp2.RequestHandler):
    def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
 		self.response.write('Bienvenido!')

class RegisterNAO(webapp2.RequestHandler):
    def get(self):
        # Creamos un simulador para cada NAO que se registre
        # s = Simulador()
        s = 'sim'
        r = es.anyadirNAO(s)
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(r)
   
class GetByIDNAO(webapp2.RequestHandler):
    def get(self, nao_id):
        self.response.write('The NAO id is %s' % nao_id)
        
class DeleteNAO(webapp2.RequestHandler):
    def put(self, nao_id):
        es.quitarNAO(id)

app = webapp2.WSGIApplication([(r'/', MainPage),
                               (r'/RegisterNAO/', RegisterNAO),
                               (r'/RegisterNAO/(.*)/', GetByIDNAO),
                               (r'/RegisterNAO/(.*)/Delete/', DeleteNAO),]
                               , debug=True)