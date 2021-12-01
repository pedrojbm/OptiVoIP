# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 11:44:32 2021

Version: 0.2

Author: Mireia Juguera Carrillo <mireiajc@correo.ugr.es>
Update by: Pedro Javier Belmonte Miñano <pedrojbm@correo.ugr.es>

Description: funciones de calculo de la distribucion erlang
"""

# https://en.wikipedia.org/wiki/Erlang_(unit)#Erlang_B_formula
#A  = Trafico
#m = lineas
from __future__ import division
from math import factorial

def extended_b_lines(usage, blocking):
	line_count = 1
	while extended_b(usage, line_count) > blocking:
		line_count += 1
	return line_count


def extended_b(usage, lines, recall=0):
	original_usage = usage
	while True:
		PB = erlang(usage, lines)
		magic_number_1 = (1 - PB) * usage + (1 - recall) * PB * usage
		magic_number_2 = 0.9999 * original_usage
		if magic_number_1 >= magic_number_2:
			return PB
		usage = original_usage + recall * PB * usage
	return -1

def erlang(A, m):
    L = (A ** m) / factorial(m)
    sum_ = 0
    for n in range(m + 1): sum_ += (A ** n) / factorial(n)

    return (L / sum_)
