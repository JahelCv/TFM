# -*- coding: utf-8 -*-
import webapp2

class GlucosaPage(webapp2.RequestHandler):
    
    def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.write('holi glucosa')

app = webapp2.WSGIApplication([
    ('/glucosa/', GlucosaPage),
], debug=True)