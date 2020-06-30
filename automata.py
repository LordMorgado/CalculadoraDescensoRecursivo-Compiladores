import copy
from prettytable import PrettyTable
class Transicion:
    def __init__(self, simbolo=None, estadoDestino=None):
        if simbolo is None:
            self.simbolo = None
        else:
            self.simbolo = simbolo
        
        if estadoDestino is None:
            self.estadoDestino = None
        else:
            self.estadoDestino = estadoDestino

class Estado:
    _id = 0
    def __init__(self, transiciones=None, simboloAFD=None):
        self.id = Estado._id
        self.token = "0"
        if transiciones is None:
            self.transiciones = []
        else:
            self.transiciones = transiciones
        if simboloAFD is None:
            self.simboloAFD = ""
        else:
            self.simboloAFD = simboloAFD
        Estado._id = Estado._id + 1
        self.aceptacion = False
        
    def acepta(self):
        if self.aceptacion:
            self.aceptacion = False
        else:
            self.aceptacion = True

    def getTransitionsBySymbol(self, simbolo):   
        for transicion in self.transiciones:
            if transicion.simbolo == simbolo:
                return transicion.estadoDestino
        return None

    def setToken(self, token):
        self.token = token

    def getToken(self):
        return self.token

class Automata:
    def __init__(self, simbolo=None):
        self.edosceptacion = []
        self.edosAutomata = []
        self.kleene = False
        self.positiva = False
        self.signo = False
        self.afd = False
        if simbolo is None:
            self.edoInicial = Estado()
            self.alfabeto = ["ε"]
        else:
            self.alfabeto = ["ε", simbolo]
            self.edoInicial = Estado()
            estadoAceptacion = Estado()
            estadoAceptacion.acepta()
            self.edosceptacion.append(estadoAceptacion)
            self.edosAutomata = [self.edoInicial, estadoAceptacion]
            self.edoInicial.transiciones.append(Transicion(simbolo, estadoAceptacion))
    
    def unirAutomata(self, automata):
        e1 = Estado()
        e2 = Estado()
        e1.transiciones.append(Transicion("ε", self.edoInicial))
        e1.transiciones.append(Transicion("ε", automata.edoInicial))
        for estTran in self.edosceptacion:
          estTran.transiciones.append(Transicion("ε", e2))
          estTran.acepta()

        for estTran2 in automata.edosceptacion:
          estTran2.transiciones.append(Transicion("ε", e2))
          estTran2.acepta()
        e2.acepta()

        self.alfabeto = list(set(self.alfabeto) | set(automata.alfabeto) )
        self.edosAutomata = list(set(self.edosAutomata) | set(automata.edosAutomata) )
        self.edosAutomata.append(e1)
        self.edosAutomata.append(e2)
        self.edosceptacion = []
        self.edosceptacion.append(e2)
        self.edoInicial = e1
        automata = None
        if self.afd:
            self.afd = False
            if "ε" not in self.alfabeto:
                self.alfabeto.append("ε")

        return self
    
    def concatena(self, automata):
        for e in self.edosceptacion:
            e.transiciones = list(set(e.transiciones) | set(automata.edoInicial.transiciones) )
            if not automata.edoInicial.aceptacion:
                e.acepta()
        automata.edoInicial.transiciones = []
        self.alfabeto = list(set(self.alfabeto) | set(automata.alfabeto) ) #union de los alfabetos
        self.edosceptacion = []
        self.edosceptacion = automata.edosceptacion
        for e in self.edosAutomata:
            if e.aceptacion:
                self.edosceptacion.append(e)
        self.edosAutomata = list(set(self.edosAutomata) | set(automata.edosAutomata) )
        self.edosAutomata.remove(automata.edoInicial)
        if(automata.edoInicial in automata.edosceptacion):
            self.edosceptacion.remove(automata.edoInicial)
        automata = None
        if self.afd:
            self.afd = False
            if "ε" not in self.alfabeto:
                self.alfabeto.append("ε")

        return self

    def cerraduraPositiva(self):
        if not self.kleene and not self.positiva:
            self.positiva = True
            en1 = Estado()
            en2 = Estado()
            eAux = self.edoInicial

            for e in self.edosceptacion:
                e.transiciones.append(Transicion("ε", en1))
                e.acepta()
                e.transiciones.append(Transicion("ε", self.edoInicial))
            self.edosceptacion = []
            en1.acepta()
            self.edosceptacion.append(en1)
            self.edosAutomata.append(en1)

            self.edosAutomata.remove(self.edoInicial)
            self.edosAutomata.append(eAux)
            en2.transiciones.append(Transicion("ε", eAux))
            self.edoInicial = en2

            for e in self.edosAutomata:
                if e.id == 0:
                    e.id = self.edoInicial.id
                    self.edoInicial.id = 0
                    break

            self.edosAutomata.append(self.edoInicial)

            if self.afd:
                self.afd = False
                if "ε" not in self.alfabeto:
                    self.alfabeto.append("ε")
        return self

    def cerraduraKleene(self):
        if self.signo and self.positiva:
            return self
        self.cerraduraPositiva()
        self.cerraduraSigno()        
        self.kleene = True
        if self.afd:
            self.afd = False
            if "ε" not in self.alfabeto:
                self.alfabeto.append("ε")
        return self

    def cerraduraSigno(self):
        if not self.kleene and not self.signo:
            for e in self.edosceptacion:
                self.edoInicial.transiciones.append(Transicion("ε", e))
            self.signo = True
        if self.afd:
            self.afd = False
            if "ε" not in self.alfabeto:
                self.alfabeto.append("ε")

    def setClaseLexica(self, nombre):
        for est in self.edosceptacion:
            est.setToken(nombre)
    
    def duplicar(self):
        automata2 = copy.deepcopy(self)
        return automata2

    def tablaDeTransiciones(self):
        #if self.afd:
        x = PrettyTable()

        headers = ["Estado"]
        for simbolo in self.alfabeto:
            headers.append(simbolo)
        headers.append("Aceptación")
        
        x.field_names = headers
        fila = []
        for estado in self.edosAutomata:
            fila.append(estado.id)
            for simbolo in self.alfabeto:
                if estado.getTransitionsBySymbol(simbolo) == None:
                    fila.append("-1")
                else:
                    fila.append(estado.getTransitionsBySymbol(simbolo).id)
            if estado.aceptacion:
                fila.append(estado.getToken())
            else:
                fila.append("-1")
            x.add_row(fila)
            fila.clear()

        print(x)


def mover(conjunto, simbolo):
    R = []
    for e in conjunto:
        for t in e.transiciones:
            if t.simbolo == simbolo:
                R.append(t.estadoDestino)
    return R

def cerraduraE (e: Estado):
    R = []
    pila = []
    pila.append(e)
    while pila:
        e2 = pila.pop()
        if e2 in R:
            continue
        R.append(e2)
        for trn in e2.transiciones:
            if trn.simbolo == "ε":
                if not (trn.estadoDestino in R):
                    pila.append(trn.estadoDestino)
    return R
    
def cerraduraEestados(conjunto):
    R = []
    for e in conjunto:
        R = list(set(R) | set(cerraduraE(e)))
    return R

def goTo (stados, simbolo):
        return cerraduraEestados(mover(stados, simbolo));


def afnToafd(afn: Automata):

    if (afn.afd):
        return afn
    
    afd = Automata()
    afd.kleene = False
    afd.positiva = False
    afd.signo = False
    afd.afd = True
    
    estadoInicial = Estado()
    estadoInicial.id = 0
    Sn = [] #new Set<State>();
    estadoAProcesar = [] #new Set<State>();
    conjuntoA = [] #new Set<Set<State>>(); //Es un conjunto de conjuntos de conjuntoA
    conjuntoAAFD = []#new Set<State>(); //Contendra conjuntoA numerados de 0 a n
    transicion = Transicion()
    state =  Estado()

    queueA = []
    conjuntoA.clear()

    afd.alfabeto = afn.alfabeto # Se copia el alfabeto del AFN al AFD
    if "ε" in afd.alfabeto:
        afd.alfabeto.remove("ε") # Elimina Epsilon del alfabeto perteneciente al AFD
    Sn = cerraduraE(afn.edoInicial) # Se calcula la cerradura epsilon del estado inicial y se guarda en Sn
    for s in Sn:
        if s in afn.edosceptacion:
            estadoInicial.acepta()
            afd.edosceptacion.append(estadoInicial)
            break
    queueA.append(Sn)
    conjuntoA.append(Sn)
    afd.edosAutomata.append(estadoInicial) # Agrega el inicial
    afd.edoInicial = estadoInicial
        
    while len(queueA) != 0:
        estadoAProcesar = queueA[0] # quita de cola
        for simb in afd.alfabeto:
            Sn = goTo(estadoAProcesar, simb) # representa la S
            if not (Sn in conjuntoA) and Sn != []: # Si no exisitia este subconjunto de conjuntoA va a conformar un nuevo estado del AFD con su transicion
                state = Estado()
                queueA.append(Sn) # se va a analizar el siguiente
                conjuntoA.append(Sn)
                transicion = Transicion(simb, state)
                for estadosDeSn in Sn:
                    if estadosDeSn in afn.edosceptacion: #Si el conjunto contiene al menos un estado de aceptacion
                        state.acepta()
                        afd.edosceptacion.append(state)
                        break
                for estadosDeSn in Sn:
                    if estadosDeSn.getToken() != "0":
                        state.setToken(estadosDeSn.getToken())
                        break


                afd.edosAutomata[conjuntoA.index(estadoAProcesar)].transiciones.append(transicion)
                afd.edosAutomata.append(state)
            elif Sn != []:
                transicion = Transicion(simb, afd.edosAutomata[conjuntoA.index(Sn)])
                afd.edosAutomata[conjuntoA.index(estadoAProcesar)].transiciones.append(transicion)
        queueA.pop(0)

    return afd