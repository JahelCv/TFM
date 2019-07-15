# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import webapp2
#from AccionesComunicaNAO import AccionesComunicaNAO
#import xalglib


class MainPage(webapp2.RequestHandler):
    
#    def __init__(self):
#        self.ac = AccionesComunicaNAO()
#        self.ac.decirFrase('Empezamos')
    
    def get(self):

#		# L-BFGS optimizer with m=2 is created, one result is returned
#		s = xalglib.minlbfgscreate(2,[0,0,0])
#
#		# function with no output values is called
#		xalglib.minlbfgssetcond(s, 0, 0, 0, 10)
#
#		# some optimization code here 
#		xalglib.minlbfgsoptimize_g(s, function1_grad)
#
#		# and, finally, call to function with multiple outputs 
#		x, rep = xalglib.minlbfgsresults(s)
		self.response.headers['Content-Type'] = 'text/plain'
#		self.response.write(str(x))
		self.response.write('holi')

app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)

#def function1_grad(x, grad, param):
#	func = 100*(x[0]+3)**4 + (x[1]-3)**4
#	grad[0] = 400*(x[0]+3)**3
#	grad[1] = 4*(x[1]-3)**3
#	return func