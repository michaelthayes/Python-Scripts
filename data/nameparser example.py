# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 16:37:18 2021

@author: Mike
"""


#https://pypi.org/project/nameparser/
from nameparser import HumanName

name = HumanName("Dr. Juan Q. Xavier de la Vega III (Doc Vega)")
print(name)
print(name.last)
print(name.first)
print(name.middle)


name = HumanName('Hayes, Michael Terrence')
print(name)
print(name.last)
print(name.first)
print(name.middle)
print(name.middle[0])


name = HumanName('Galyn "Rip" Rippentrop')
print(name)
print(name.last)
print(name.first)
print(name.middle)
print(name.surnames)
print(name.nickname)



name = HumanName('Jennifer J. Ambrose-Miranda')
print(name)
print(name.last)
print(name.first)
print(name.middle)


name = HumanName('MELINDA KERNS')
print(name)
print(name.capitalize())

