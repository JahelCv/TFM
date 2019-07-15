# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 20:12:17 2019

@author: Jahel
"""

import requests
import time

r = requests.get("http://localhost:8080/")
print r.content
time.sleep(1)
r = requests.get("http://localhost:8080/RegisterNAO/")
print r.content
time.sleep(1)
r = requests.get("http://localhost:8080/RegisterNAO/" + str(r.content) + "/")
print r.content
time.sleep(1)