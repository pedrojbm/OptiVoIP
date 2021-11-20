# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 19:24:37 2021

@author: mireia
"""

from P2_ui import *
from PyQt5.QtWidgets import QComboBox, QApplication, QWidget, QHBoxLayout, QLabel
import erlang 

Rt = 0
bht = 0
BWres = 0
retardos = []
codec_param = []
BWll = []
BWst = []
salidaBWST = []
cambiar_codec = 0
idx_codec = 0

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self) 
        
        self.pushButton.clicked.connect(self.muestra_Rt)
        
    def actualiza_valor(self):
        global retardos, calculado, Rt, bht, BWll, BWst, BWres, idx_codec, cambiar_codec, codec_param
        global mos, Nc, Nl, Pll, Tpll, Rr, J
        
        mos = self.comboBox_2.value() #4
        Nc = self.spinBox.value() #150
        Nl = self.spinBox_2.value() #20
        Tpll = self.spinBox_3.value() #3 min
        Pll = self.spinBox_4.value() #Durante la bht 100%
        BWres = self.spinBox_5.value() #4 Mbps
        Rt = self.spinBox_6.value() #150 ms
        Rr = self.spinBox_7.value() #75 ms
        J = self.spinBox_8.value() #30 ms
        
        #Identificamos CODEC
        
        self.comboBox.setCurrentIndex(idx_codec)
            
        codec_param = codecs[idx_codec,:]
        
        #Calculamos valores con las funciones disenadas
        retardos = retardo_total(Rr, J, codec_param[4], codec_param[1], Ralg[idx_codec])    
        
    def retardo_total(Rr,J,VPS,CSI,Ralg):
        #Retardo conjunto, CODEC + paquetizacion
        Rorg = VPS + 0.1*CSI
    
        #Retardos buffer antijitter
        Rjitter_1 = 1.5*J
        Rjitter_2 = 2*J
    
        #Retardo de decodificacion en el destino
        Rdest = 0.1*VPS

        #Retardo total (buffer antijitter x1.5 y x2)
        Rt1 = Rorg + Ralg + Rr + Rjitter_1 + Rdest
        Rt2 = Rorg + Ralg + Rr + Rjitter_2 + Rdest
    
        #Calculamos el numero de paquetes almacenados en el buffer antijitter
        #en cada caso
        Npaq1 = Rjitter_1//VPS
        Npaq2 = Rjitter_2//VPS
    
        return Rorg, Ralg, Rr, Rjitter_1, Rjitter_2, Rdest, Rt1, Rt2, Npaq1, Npaq2
    
    def muestra_Rt(self):
        global retardos, Rt
        
        self.label_8.setText(str(retardos[1]) + ' ms')
        #self.label_RetardoTotal2.setText(str(retardos[7]) + ' ms')

        

        
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
    