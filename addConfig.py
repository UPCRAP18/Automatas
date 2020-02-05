from saveconfig import *
from PyQt5.QtWidgets import QMessageBox, QFileDialog
import json

class SaveConfig(QtWidgets.QMainWindow, Ui_SaveWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon("brain.png"))
        self.btnCancelar.clicked.connect(self.closeWindow)
        self.btnAddConfig.clicked.connect(self.addConfig)
        
    def closeWindow(self):
        self.close()

    def addConfig(self):
        self.nombre_config = self.txtConfig_Name.text()
        self.estados = self.txtStates.text()
        self.alpha = self.txtAlpha.text()
        self.init_state = self.txtInit_State.text()
        self.acept_states = self.txtAcept_States.text()
        self.trans = self.txtTrans.toPlainText()

        if len(self.estados) == 0:
            self.showWarningDialog("No puede dejar los estados vacios")
        elif len(self.alpha) == 0:
            self.showWarningDialog("No puede quedar vacio el alfabeto")
        elif len(self.init_state) == 0:
            self.showWarningDialog("Por favor especifique un estado inicial")
        elif len(self.acept_states) == 0:
            self.showWarningDialog("Por favor especifique al menos un estado de aceptación")
        elif len(self.trans) == 0:
            self.showWarningDialog("Por favor especifique al menos una transicion")
        else:
            self.estados_arr = self.estados.split(",")
            self.alpha_arr = self.estados.split(",")
            self.acept_states_arr = self.acept_states.split(",")
            self.trans_arr = self.trans.split("\n")
            self.transitions_arr = []
            for transition in self.trans_arr:
                temp = transition.split(",")
                self.transitions_arr.append({
                    "prev_state": temp[0],
                    "value":temp[1],
                    "next_state":temp[2]
                })
            self.dict = {
                "Nombre" : self.nombre_config,
                "Estados": self.estados_arr,
                "Alfabeto": self.alpha_arr,
                "Estado_Inicial": self.init_state,
                "Estados_Aceptacion": self.acept_states_arr,
                "Transiciones": self.transitions_arr
            }

            name = QFileDialog.getSaveFileName(self,"Guardar configuracion", "","Config Files (*.json)")
            file = open(name[0],'w')
            json.dump(self.dict, file)
            file.close()

    def showWarningDialog(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText(message)
        msg.setWindowTitle("¡Advertencia!")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

