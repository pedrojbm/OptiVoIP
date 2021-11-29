# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 19:26:28 2021

Version: 0.2

Author: Mireia Juguera Carrillo <mireiajc@correo.ugr.es>
Update by: Pedro Javier Belmonte Miñano <pedrojbm@correo.ugr.es>

Description: 
"""

import erlang
import numpy #Biblioteca matemática 

#Elige un codec que cumpla con el mos introducido como parametro
def elige_codec(mos, codecs):
    dist = codecs[:,2] - mos #La columna del mos en el exel es la 2    
    for i in range(0,len(dist),1):
        if (dist[i]>=1):
            dist[i]=0
    codec = numpy.argmax(dist)
    
    return codec

#Calculamos el Rt como vimos en clase de seminarios    
def calculo_Rt(Rr,J,CSI,VPS,Ralg):    
    Rt1 = VPS + 0.1*CSI + Ralg + Rr + 1.5*J + 0.1*VPS
    Rt2 = VPS + 0.1*CSI + Ralg + Rr + 2*J + 0.1*VPS    
    Npaq1 = (1.5*J)//VPS
    Npaq2 = (2*J)//VPS
    
    return  Ralg, Rr, Rt1, Rt2, Npaq1, Npaq2


#Funcion para calcular el BHT
def calculo_BHT(Nc,Nl,Tpll):
    #La hora cargada corresponde al periodo de tiempo de 60 minutos consecutivos del día donde se presenta mayor tráfico
    #Por eso dividimos entre sesenta
    BHT=(Nc*Nl*Tpll)/60
    
    return BHT

#Funcion para calcular el BWll 
def calculo_BWll(CSS,CSI,VPS):
    #La cabecera RTP es de 40 bytes
    Cab_RTP=40
    
    #Sumamos el payload y pasamos a bits para tener la longitud final del paquete
    Paq_RTP=(Cab_RTP+VPS)*8
    
    #La abecera cRTP es la cabecera rtp entre 10
    Cab_cRTP=4
    
    #Igual que antes calculamos la longitud final del paquete
    Paq_cRTP=(Cab_cRTP+VPS)*8
    
    #Calculo CBR y el PPS
    CBR=(CSS*8)/(CSI/1000)
    PPS=CBR/(VPS*8)
    
    #Calculo ancho de banda de una llamada
    BWll_RTP=(Paq_RTP*PPS)/1000
    BWll_cRTP=(Paq_cRTP*PPS)/1000
     
    return BWll_RTP,BWll_cRTP

#Funcion para calcular el BWST
def calculo_BWST(BHT,Pb,BWll_RTP,BWll_cRTP):    
    Nllamadas=erlang.extended_b_lines(BHT,Pb/100)
    BWST_RTP=Nllamadas*BWll_RTP
    BWST_cRTP=Nllamadas*BWll_cRTP
    
    return BWST_RTP,BWST_cRTP

    
    
    