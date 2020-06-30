from automata import *
import numpy as np


class LexicAnalyzer:
    def __init__(self, automata, inputString):
        #Atributos del analizador
        self.automaton = afnToafd(automata)
        self.inputString = inputString
        #Atributos de estado
        self.indexStack = []
        self.i = 0
        self.lastLexemIndex = 0

        ultimoEstadoAceptado = None
        estadoAnterior = None
        self.tabla = [("", "")]
        principioDelLexema = 0
        currentState = self.automaton.edoInicial#Empieza en el inicial
        while self.i < len(self.inputString): #Recorremos la cadena
            c = self.inputString[self.i]
            destinoConSimbolo = currentState.getTransitionsBySymbol(c)
            if destinoConSimbolo != None:
                self.i += 1
                currentState = destinoConSimbolo
                
                if currentState.aceptacion: #Si el estado al que nos movimos es de aceptación
                    self.lastLexemIndex = self.i
                    ultimoEstadoAceptado = currentState
                    self.tabla[len(self.tabla) -1] = list(self.tabla[len(self.tabla) -1])#make a[0] mutable
                    self.tabla[len(self.tabla) -1][0] = self.inputString[principioDelLexema:self.i] #now new assignment will be valid
                    self.tabla[len(self.tabla) -1][1] = currentState.getToken()
                    self.tabla[len(self.tabla) -1] = tuple(self.tabla[len(self.tabla) -1]) #make a[0] again a tuple                    
            else:#El siguiente simbolo no tiene transición
                if ultimoEstadoAceptado == None:#hay error
                    currentState = self.automaton.edoInicial#vuelve al estado inicial
                    self.i += 1
                    self.tabla[len(self.tabla) -1] = list(self.tabla[len(self.tabla) -1])#make a[0] mutable
                    self.tabla[len(self.tabla) -1][0] = self.inputString[principioDelLexema:self.i] #now new assignment will be valid
                    self.tabla[len(self.tabla) -1][1] = "ERROR"
                    self.tabla[len(self.tabla) -1] = tuple(self.tabla[len(self.tabla) -1]) #make a[0] again a tuple
                    principioDelLexema = self.i

                    tupla = ("", "")
                    self.tabla.append(tupla)
                else:
                    self.tabla[len(self.tabla) -1] = list(self.tabla[len(self.tabla) -1])#make a[0] mutable
                    self.tabla[len(self.tabla) -1][0] = self.inputString[principioDelLexema:self.i] #now new assignment will be valid
                    self.tabla[len(self.tabla) -1][1] = currentState.getToken()
                    self.tabla[len(self.tabla) -1] = tuple(self.tabla[len(self.tabla) -1]) #make a[0] again a tuple
                    tupla = ("", "")
                    self.tabla.append(tupla)
                    self.i = self.lastLexemIndex
                    principioDelLexema = self.i
                    ultimoEstadoAceptado = None
                    currentState = self.automaton.edoInicial#vuelve al estado inicial
        tupla = ("", "END")
        self.tabla.append(tupla)
        
        headers = [("Lexema ","Token")]
        max_length_column = []
        elements_in_tuple = 2

        for i in range(elements_in_tuple):
            max_length_column.append(max(max(len(e[i])+2 for e in self.tabla), max(len(e[i])+2 for e in headers) ) )    

        self.resultadoLex = ""
        for e in headers:
            for i in range(elements_in_tuple):
                print(e[i].ljust(max_length_column[i]), end='')
                self.resultadoLex += e[i].ljust(max_length_column[i])
        self.resultadoLex += '\n'  
        print('\n')
        for e in self.tabla:
            for i in range(elements_in_tuple):
                print(e[i].ljust(max_length_column[i]), end='')
                self.resultadoLex += e[i].ljust(max_length_column[i])
            self.resultadoLex += '\n'
            print('\n')
        self.i = 0

    def getResultadoLex(self):
        return self.resultadoLex

    def reset(self, inputString):
        self.indexStack = []
        self.inputString = inputString

    def setInput(self, inputString):
        self.inputString = inputString

    def getToken(self):#SDDMASDDPDD.DDDMDDDBMTTTLDLLLDMMDD.DPLDLD
        if (self.i == len(self.tabla)):
            return self.tabla[self.i-1][1]
        aux = self.tabla[self.i][1]
        self.i += 1
        return aux


    def returnToken(self):
        self.i -= 1
    
    def getCurrentLexem(self):
        return self.tabla[self.i-1][0]

    def getLexicState(self):
        return [self.i, self.lastLexemIndex, self.indexStack]
        

    def setLexicState(self, lexicState):
        self.i = lexicState[0]
        self.lastLexemIndex = lexicState[1]
        self.indexStack = lexicState[2]
        
