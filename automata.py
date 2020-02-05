#!/usr/bin/python3
import json
from os import system, name, listdir
from os.path import isfile, join

#Custom LS
def ls(ruta = './configs'):
    global confs
    cont = 1
    configs_dict = {}
    config_list = listdir(ruta)
    for config in config_list:
        print(str(cont) + ". " + config)
        configs_dict[cont] = config
        cont+=1
    confs = configs_dict
    
#Muestro la lista de archivos de configuracion disponibles
def showConfigs():
    #clear()
    print("Archivos de configuracion disponibles: ")
    ls()
    index = int(input("Seleccione el archivo a cargar: "))
    loadData(confs[index])

#Limpieza de pantalla
def clear():
    if name == "nt":
        _ = system("cls")
    else:
        _ = system("clear")

#Cargo el archivo especificado e inicializo las variables globales
def loadData(archivo):
    global estados, alfabeto, trans, init_state, acept_states, data
    with open("./configs/" + archivo) as config:
        data = json.load(config)
        estados = data["Estados"]
        alfabeto = data["Alfabeto"]
        trans = data["Transiciones"]
        init_state = data["Estado_Inicial"]
        acept_states = data["Estados_Aceptacion"]

#Muestra de datos de configuracion cargados
def showData():
    print(data)

#Menu principal
def showMenu():
    #clear()
    print("Bienvenido al AFD validator V1.0-Alpha de Rodrigo ❤️")
    print("Menu principal")
    print("1. Cargar archivo de configuracion")
    print("2. Crear una nueva configuracion")
    print("3. Validar cadena")
    print("4. Salir")
    return int(input("Seleccione una opcion: "))

def getUserString():
    #usr_in = ""
    print("El alfabeto disponible es: ")
    print("{", end=" ")
    for letter in alfabeto:
        print(letter, end=" ")
    print("}")
    print("*Nota: Para representar Epsilon (ε), utilice un espacio")
    usr_in = input("Introduzca su cadena a validar: ")
    validateString(usr_in)



def validateString(cadena):
    estado_actual = init_state
    for caracter in cadena:
        sigma = list()
        #next_trans = {}
        for transition in trans:
            if(transition["prev_state"] == estado_actual):
                sigma.append(transition)
        for state in sigma:
            if(state["value"] == caracter):
                #next_trans = state
                estado_actual = state["next_state"]
        
    print(estado_actual)

### EJECUCION PRINCIPAL ###
salir = False
opcion = 0
while not salir:
    showMenu()
    opcion = showMenu()
    if opcion == 1:
        showConfigs()
        getUserString()
    elif opcion == 2:
        print("Opcion 2")
    elif opcion == 3:
        pass
    elif opcion == 4:
        salir = True

print("Hasta luego")



