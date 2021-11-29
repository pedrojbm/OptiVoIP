# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 19:24:37 2021

Version: 0.2

Author: Mireia Juguera Carrillo <mireiajc@correo.ugr.es>
Update by: Pedro Javier Belmonte Miñano <pedrojbm@correo.ugr.es>

Description: 
"""

from mainUI import *
import numpy #Biblioteca matemática
import funciones #Script con nuestras funciones
import smtplib

#Cargamos los valores que guardamos en los exel
codecs = numpy.loadtxt(open("tabla_codecs.csv", "rb"), delimiter=";")
Retardo_alg = numpy.loadtxt(open("retardo_alg.csv", "rb"), delimiter=";")

#Valiables inicializadas
Rt = bht = BWres = otro_codec = idx_codec = 0
retardos = para_codecs = BWll = BWst = salidaBWST =[]


class MainWindows(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.showPage1()
        
    #Funcion que muestra la pagina 1 de la interfaz    
    def showPage1(self):
        global otro_codec, idx_codec        
        self.stackedWidget.setCurrentWidget(self.page)        
        if (otro_codec == 0):
            self.spinBox_MOS.setEnabled(1)
        otro_codec = 0            
        self.button_calculoRt.clicked.connect(self.showPage2)
        self.actualiza_valor()        
              
    #Funcion que muestra la pagina 2 de la interfaz     
    def showPage2(self):
        global otro_codec, idx_codec        
        self.stackedWidget.setCurrentWidget(self.page_2)        
        self.button_siguiente.clicked.connect(self.showPage3)
        self.button_calcularRt.clicked.connect(self.devolver_Rt)
        
	#Funcion que muestra la pagina 3 de la interfaz  	
    def showPage3(self):
        global otro_codec, idx_codec       
        self.stackedWidget.setCurrentWidget(self.page_3)       
        self.button_BHT.clicked.connect(self.devolver_bht)
        self.button_BWll.clicked.connect(self.devolver_bwll)
        self.button_BWSIPTRUNK.clicked.connect(self.devolver_bwst)
        self.comboBox_CODEC.activated.connect(self.combo_codec)
        self.button_cambiarParametros.clicked.connect(self.showPage1)        
        self.button_correo.clicked.connect(self.mandar_correo)
            
    #Leemos los valores de entrada y calculamos los retardos, el bht y los anchos de banda
    def asigna_valor(self):
        global mos, Nc, Nl, Tpll,  Pll, BWres, Rr, J,retardos, Rt, bht, BWll, BWst,  idx_codec, otro_codec, para_codecs       
        Nc = self.spinBox_Nc.value() #150
        Nl = self.spinBox_Nl.value() #20
        Tpll = self.SpinBox_Tpll.value() #3 min
        Pll = self.spinBox_Pll.value() #Durante la bht 100%
        BWres = self.spinBox_BWres.value() #4Mbps
        mos = self.spinBox_MOS.value() #4
        Rt = self.spinBox_Rt.value() #150
        Rr = self.spinBox_Rr.value() #75
        J = self.spinBox_jitter.value() #30           
        para_codecs = codecs[idx_codec,:]
        retardos = funciones.calculo_Rt(Rr, J, para_codecs[1], para_codecs[4], Retardo_alg[idx_codec]) #VPS columna 4 del exel, CSI columna 1
        bht = funciones.calculo_BHT(Nc,Nl,Tpll)
        BWll = funciones.calculo_BWll(para_codecs[0],para_codecs[1],para_codecs[3])
        BWst = funciones.calculo_BWST(bht,Pll,BWll[0],BWll[1])        
        if otro_codec==0: 
            idx_codec = funciones.elige_codec(mos, codecs)
            self.comboBox_CODEC.setCurrentIndex(idx_codec)
            self.label_CODEC_2.setText(self.comboBox_CODEC.itemText(idx_codec))
       
    #Funcion que muestra la lista de codecs
    def combo_codec(self):
        global idx_codec, otro_codec        
        otro_codec = 1
        idx_codec = self.comboBox_CODEC.currentIndex()
        self.spinBox_MOS.setEnabled(0)       
        self.label_CODEC_2.setText(str(self.comboBox_CODEC.currentText()))
        self.asigna_valor()
        self.showPage2()  
          
    #Actualiza el valor de los parametros de entrada que se encuentran en la pagina 1 de la interfaz
    def actualiza_valor(self):            
        self.spinBox_Nc.valueChanged.connect(self.asigna_valor)
        self.spinBox_Nl.valueChanged.connect(self.asigna_valor)
        self.SpinBox_Tpll.valueChanged.connect(self.asigna_valor)
        self.spinBox_Pll.valueChanged.connect(self.asigna_valor)
        self.spinBox_BWres.valueChanged.connect(self.asigna_valor)
        self.spinBox_MOS.valueChanged.connect(self.asigna_valor)
        self.spinBox_Rt.valueChanged.connect(self.asigna_valor)
        self.spinBox_Rr.valueChanged.connect(self.asigna_valor)
        self.spinBox_jitter.valueChanged.connect(self.asigna_valor)
             
    #Muestra el valor de los retardos calculados en la interfaz y devuelve el que cumple (si lo hay)
    def devolver_Rt(self):
        global retardos       
        self.label_RetardoTotal_15.setText(str(retardos[2]))
        self.label_RetardoTotal_2.setText(str(retardos[3]))        
        self.label_paquetesRTP_15.setText(str(retardos[4]))
        self.label_paquetesRTP_2.setText(str(retardos[5]))        
            
    #Muestra el valor del bht    
    def devolver_bht(self):
        global bht        
        self.label_BHT.setText(str(bht))
        
    #Muestra el valor del bwll    
    def devolver_bwll(self):
        global BWll       
        self.label_BWll_RTP.setText(str(BWll[0]))
        self.label_BWll_cRTP.setText(str(BWll[1]))

    #Muestra el valor del bwst
    def devolver_bwst(self):
        global BWst      
        self.label_BWst_RTP.setText(str(BWst[0]))
        self.label_BWst_cRTP.setText(str(BWst[1]))
    
    #Si el usuario quiere se le puede enviar un informe
    def mandar_correo(self):
        port=587
        smtp_server = "correo.ugr.es"
        sender_email="mireiajc@correo.ugr.es"
        receiver_email="usuario@correo.ugr.es"
        password = "contraseña"

        message="""\
            From: mireiajc@correo.ugr.es
            TO:usuario@correo.ugr.es
            Subject: Informe Practica 2
            
            Alumno: Mireia Juguera           
            
            Mensaje enviado con Python 
           """ 
        
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
            server.close()
        

if __name__ == "__main__":
	app = QtWidgets.QApplication([])
	windows = MainWindows()
	windows.show()
	app.exec_()


