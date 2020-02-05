from mainwindow import *
#from saveconfig import *
from addConfig import *
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import *
import sys
import json
from os.path import isfile, join

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    estados, alfabeto, trans, init_state, acept_states, data, nombre_config = [], [], [], "", [], [], ""

    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon("brain.png"))
        self.btnLoadConfig.clicked.connect(self.openFileNameDialog)
        self.btnValidate.clicked.connect(self.validateInput)
        self.btnCreateConfig.clicked.connect(self.createConfig)

    def createConfig(self):
        self.dialog = SaveConfig(self)
        self.dialog.show()

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        #options |= QFileDialog.Use
        fname, _ = QFileDialog.getOpenFileName(self,"Abrir configuracion", "","Config Files (*.json)")
        if fname:
            f = open(fname, "r")
            with f:
                self.data = json.load(f)
                self.estados = self.data["Estados"]
                self.alfabeto = self.data["Alfabeto"]
                self.trans = self.data["Transiciones"]
                self.init_state = self.data["Estado_Inicial"]
                self.acept_states = self.data["Estados_Aceptacion"]
                self.nombre_config = self.data["Nombre"]
                self.loadDataInLabels(fname)
                self.btnValidate.setEnabled(True)
                self.txtInput.setEnabled(True)

    def loadDataInLabels(self, fileName):
        self.lblConfig_File_Name.setText(fileName)
        self.lblNombre.setText(self.nombre_config)
        self.lblAlfabeto.setText("{ " + ", ".join(self.alfabeto) + " }")
        self.lblEstados.setText("{ " + ", ".join(self.estados) + " }")
        self.lblEst_Acept.setText("{ " + ", ".join(self.acept_states) + " }")

    def validateInput(self):
        cadena = self.txtInput.text()
        estado_actual = self.init_state
        for caracter in cadena:
            sigma = list()
            for transition in self.trans:
                if(transition["prev_state"] == estado_actual):
                    sigma.append(transition)
            for state in sigma:
                if(state["value"] == caracter):
                    estado_actual = state["next_state"]
        
        status = "Valida" if estado_actual in self.acept_states else "Invalida"

        self.lblResult.setText("La cadena es: " + status + ".\nEl estado final es: " + estado_actual)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()