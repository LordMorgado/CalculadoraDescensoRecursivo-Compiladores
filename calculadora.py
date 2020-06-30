from os import system
import math 
from graphviz import Digraph
from automata import *
from lexico import *

def dibujaAutomata(afnd):
    f = Digraph('finite_state_machine', filename='afnd.gv')
    f.attr(rankdir='LR', size='5,5')
    f.attr('node', shape='doublecircle')
    for estado in afnd.edosceptacion:
        f.node(str(estado.id))
    
    f.attr('node', shape='circle')
    afnd.edosAutomata.sort(key=lambda x: x.id, reverse=False)

    for estado in afnd.edosAutomata:
        for trs in estado.transiciones:
            f.edge(str(estado.id), str(trs.estadoDestino.id), label=trs.simbolo)
    f.view()

class SyntaxAnalyzerCalc:

    def __initAutomatas(self):
        #CREAMOS EL AUTÓMATA QUE CONTIENE A TODOS LOS NÚMEROS "(0-9)+"
        NUM = Automata('1')
        NUM.unirAutomata(Automata('2'))
        NUM.unirAutomata(Automata('3'))
        NUM.unirAutomata(Automata('4'))
        NUM.unirAutomata(Automata('5'))
        NUM.unirAutomata(Automata('6'))
        NUM.unirAutomata(Automata('7'))
        NUM.unirAutomata(Automata('8'))
        NUM.unirAutomata(Automata('9'))
        NUM.unirAutomata(Automata('0'))
        NUM.cerraduraPositiva()

        DOT = Automata('.')
        DOT.concatena(NUM.duplicar())
        DOT.cerraduraSigno()

        NUM.concatena(DOT.duplicar())
        NUM.setClaseLexica('NUM')
        #CREAMOS LOS DEMÁS AUTÓMATAS CORRESPONDIETES A LAS FUNCIONES Y OPERACIONES
        MAS = Automata('+')
        MAS.setClaseLexica('MAS')
        MENOS = Automata('-')
        MENOS.setClaseLexica('MENOS')
        PROD = Automata('*')
        PROD.setClaseLexica('PROD')
        DIV = Automata('/')
        DIV.setClaseLexica('DIV')
        POT = Automata('^')
        POT.setClaseLexica('POT')
        PAR_I = Automata('(')
        PAR_I.setClaseLexica('PAR_I')
        PAR_D = Automata(')')
        PAR_D.setClaseLexica('PAR_D')

        SIN = Automata('S')
        SIN.concatena(Automata('I'))
        SIN.concatena(Automata('N'))
        SIN.setClaseLexica('SIN')

        COS = Automata('C')
        COS.concatena(Automata('O'))
        COS.concatena(Automata('S'))
        COS.setClaseLexica('COS')

        TAN = Automata('T')
        TAN.concatena(Automata('A'))
        TAN.concatena(Automata('N'))
        TAN.setClaseLexica('TAN')

        EXP = Automata('E')
        EXP.concatena(Automata('X'))
        EXP.concatena(Automata('P'))
        EXP.setClaseLexica('EXP')

        LN = Automata('L')
        LN.concatena(Automata('N'))
        LN.setClaseLexica('LN')

        LOG = Automata('L')
        LOG.concatena(Automata('O'))
        LOG.concatena(Automata('G'))
        LOG.setClaseLexica('LOG')

        return [NUM, MENOS, MAS, PROD, DIV, POT, PAR_D, PAR_I, SIN, COS, TAN, EXP, LN, LOG]
    
    def __init__(self, cadena):
        self.automataGeneral = Automata()
        for auto in self.__initAutomatas():
            self.automataGeneral.unirAutomata(auto)


        self.lexico = LexicAnalyzer(self.automataGeneral, cadena)

    def getResultadoLex(self):
        return self.lexico.getResultadoLex()

    def solve(self):
        val = []
        string = []
        if (self.G(val, string)):
            _val = val[0]
            _str = string[0]
            return(_val, _str)
        else:
            print("Error sintáctico")
            return None

    def G(self, v, s):
        if (self.E(v,s)):
            tok = self.lexico.getToken()
            if (tok == "END"):
                return True
        return False

    def E(self, v, s):
        if (self.T(v,s)):
            if (self.Ep(v,s)):
                return True
        return False

    def Ep(self, v, s):
        v1 = []
        s1 = []
        tok = self.lexico.getToken()
        if (tok == "MAS" or tok == "MENOS"):
            if (self.T(v1, s1)):
                if tok == "MAS":
                    v[0] += v1[0]
                else:
                    v[0] -= v1[0]
                #s[0] = tok == "MAS"? "+" : "-" s[0] + s1[0]
                if (self.Ep(v,s)):
                    return True
            return False
        self.lexico.returnToken()
        return True

    def T(self, v, s):
        if (self.P(v,s)):
            if (self.Tp(v,s)):
                return True
        return False

    def Tp(self, v, s):
        v1 = []
        s1 = []
        tok = self.lexico.getToken()
        if (tok == "PROD" or tok == "DIV"):
            if (self.P(v1, s1)):
                if tok == "PROD":
                    v[0] *= v1[0]
                else:
                    v[0] = V[0]/v1[0]
                #s[0] = tok == "PROD" ? "*" : "/" s[0] + s1[0]
                if (self.Tp(v,s)):
                    return True
            return False
        self.lexico.returnToken()
        return True

    def P(self, v, s):
        if (self.F(v,s)):
            if (self.Pp(v,s)):
                return True
        return False

    def Pp(self, v, s):
        v1 = []
        s1 = []
        tok = self.lexico.getToken()

        if (tok == "POT"):
            if (self.F(v1, s1)):
                v[0] = pow(v[0], v1[0])
                #s[0] = `^ ${s[0]} ${s1[0]}`
                if (self.Pp(v,s)):
                    return True
            return False
        self.lexico.returnToken()
        return True
    
    def F(self, v, s):
        tok = self.lexico.getToken()
        if tok == "PAR_I":
            if (self.E(v,s)):
                tok = self.lexico.getToken()
                if (tok == "PAR_D"):
                    return True
            return False

        elif tok == "SIN":
            if (self.lexico.getToken() == "PAR_I"):
                if (self.E(v,s)):
                    if (self.lexico.getToken() == "PAR_D"):
                        v[0] = math.sin(v[0])
                        s[0] = "sin " + s[0]
                        return True
            return False

        elif tok == "COS":
            if (self.lexico.getToken() == "PAR_I"):
                if (self.E(v,s)):
                    if (self.lexico.getToken() == "PAR_D"):
                        v[0] = math.cos(v[0])
                        s[0] = "cos " + s[0]
                        return True
            return False

        elif tok == "TAN":
            if (self.lexico.getToken() == "PAR_I"):
                if (self.E(v,s)):
                    if (self.lexico.getToken() == "PAR_D"):
                        v[0] = math.tan(v[0])
                        s[0] = "tan " + s[0]
                        return True
            return False

        elif tok == "EXP":
            if (self.lexico.getToken() == "PAR_I"):
                if (self.E(v,s)):
                    if (self.lexico.getToken() == "PAR_D"):
                        v[0] = math.exp(v[0])
                        s[0] = "exp " + s[0]
                        return True
            return False

        elif tok == "LN":
            if (self.lexico.getToken() == "PAR_I"):
                if (self.E(v,s)):
                    if (self.lexico.getToken() == "PAR_D"):
                        v[0] = math.log(v[0])
                        s[0] = "ln " + s[0]
                        return True
            return False

        elif tok == "LOG":
            if (self.lexico.getToken() == "PAR_I"):
                if (self.E(v,s)):
                    if (self.lexico.getToken() == "PAR_D"):
                        v[0] = math.log(v[0],10)
                        s[0] = "log " + s[0]
                        return True
            return False

        elif tok == "NUM":
            lexem = float(self.lexico.getCurrentLexem())
            v.append(lexem)
            s.append(self.lexico.getCurrentLexem())
            return True
        else:
            return False

#calcu = SyntaxAnalyzerCalc("(3*COS(0))^2")
#res = calcu.solve()
#print(res)