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
        self.btnImportAFN.clicked.connect(self.importAFN)

    def importAFN(self):
        options = QFileDialog.Options()
        fname, _ = QFileDialog.getOpenFileName(self,"Abrir configuracion", "","Config Files (*.json)")
        if fname:
            f = open(fname, "r")
            with f:
                self.data_afn = json.load(f)
                self.estados_afn = self.data_afn["Estados"]
                self.alfabeto_afn = self.data_afn["Alfabeto"]
                self.trans_afn = self.data_afn["Transiciones"]
                self.init_state_afn = self.data_afn["Estado_Inicial"]
                self.acept_states_afn = self.data_afn["Estados_Aceptacion"]
                self.nombre_config_afn = self.data_afn["Nombre"]
                self.convertAFN()
                
        else:
            pass

    def convertAFN(self):
        trans_map = []
        for item in self.trans_afn:
            if item["prev_state"] == self.init_state_afn:
                trans_map.append(item)

        for item in trans_map:
            next_items = item["next_state"]
            prev = ",".join(list(dict.fromkeys(next_items)))
            isIn = False
            for value in trans_map:
                if prev == value["prev_state"]:
                    isIn = True
                    break
            #FIN FOR Value - Trans Map
            if isIn == False:
                for letra in self.alfabeto_afn:
                    item_Add = {
                        "prev_state": prev,
                        "value": letra,
                        "next_state": []
                    }
                    for next_state in item["next_state"]:
                        #state_temp = []
                        for state in self.trans_afn:
                            if next_state == state["prev_state"] and state["value"] == letra:
                                next_add = list(dict.fromkeys(item_Add["next_state"]))
                                state_add = list(dict.fromkeys(state["next_state"]))
                                item_Add["next_state"] =  next_add + state_add
                                break
                            #Fin state - Trans AFN
                    #FIN FOR next_state - item["next_state"]
                    trans_map.append(item_Add)
                #FIN FOR letra - alfabeto
            #FIN IF
        #FIN FOR item - Trans Map
        print(json.dumps(trans_map, indent=4))
        ##Remapeo de asignacion
        print("Finalizando y volcando")
        acept_states = []
        new_states_arr = []
        new_states = {}
        index = 0
        for state in trans_map:
            prev_state = state["prev_state"]
            next_state = ",".join(state["next_state"])
            if prev_state not in new_states:
                new_state_prev = "q"+str(index)
                new_states[prev_state] = new_state_prev
                new_states_arr.append(new_state_prev)
                index += 1
                for acept_state in self.acept_states_afn:
                    if acept_state in prev_state:
                        if new_state_prev not in acept_states:
                            acept_states.append(new_state_prev)
            if next_state not in new_states:
                new_state_next = "q"+str(index)
                new_states[next_state] = new_state_next
                new_states_arr.append(new_state_next)
                index +=1
                for acept_state in self.acept_states_afn:
                    if acept_state in next_state:
                        if  new_state_next not in acept_states:
                            acept_states.append(new_state_next)
            #Hacer el cambio en prev y next
            state["prev_state"] = new_states[prev_state]
            state["next_state"] = new_states[next_state]
        #FIN FOR state - Trans Map
        self.txtConfig_Name.setText(self.nombre_config_afn)
        self.txtStates.setText(",".join(new_states_arr))
        self.txtInit_State.setText(self.init_state_afn)
        self.txtAcept_States.setText(",".join(acept_states))
        self.txtAlpha.setText(",".join(self.alfabeto_afn))
        self.txtTrans.setPlainText("")
        for value in trans_map:
            str_add = value["prev_state"] + "," + value["value"] + "," + value["next_state"]
            self.txtTrans.appendPlainText(str_add)
        #Volcado a archivo

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
            self.saveToFile()

    def saveToFile(self):
        self.estados_arr = self.estados.split(",")
        self.alpha_arr = self.alpha.split(",")
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
        try:
            file = open(name[0],'w')
            json.dump(self.dict, file, indent=4)
            file.close()
        except:
            self.showWarningDialog("Ha ocurrido un error al guardar los datos")
        

    
    def showWarningDialog(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText(message)
        msg.setWindowTitle("¡Advertencia!")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

