# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 11:44:32 2021

@author: mireia
"""

# https://en.wikipedia.org/wiki/Erlang_(unit)#Erlang_B_formula
#A  = Trafico
#m = lineas
from math import factorial

def erlang(A, m):
    L = (A ** m) / factorial(m)
    sum_ = 0
    for n in range(m + 1): sum_ += (A ** n) / factorial(n)

    return (L / sum_)
