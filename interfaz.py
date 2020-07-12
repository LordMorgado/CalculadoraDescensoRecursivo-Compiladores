import PySimpleGUI as sg
from calculadora import *

sg.theme('GreenTan')
btnCadena = 'Analizar cadena'
txtInput= 'texto entrada'
txtSin = 'Caja de texto Sintac'

# STEP 1 define the layout
layout = [

		[
        sg.Multiline(key=txtSin, default_text='', size=(80, 10)) #análisis sin
        ],

        [
			sg.Text('Analizar cadena'),
			sg.In(key=txtInput),
			sg.Button(btnCadena),
		]
	]

#STEP 2 - create the window
window = sg.Window('Calculadora con descenso recursivo', layout, grab_anywhere=True)

# STEP3 - the event loop
while True:
	event, values = window.read()   # Read the event that happened and the values dictionary
	if event == sg.WIN_CLOSED:     # If user closed window with X or if user clicked "Exit" button then exit
		break
	elif event == btnCadena:
		if window[txtInput].get() is not None and window[txtInput].get() is not '':
			window[txtSin]('')
			cadena = window[txtInput].get()

			calcu = SyntaxAnalyzerCalc(cadena)
			window[txtSin].Update(value='\n' + calcu.getResultadoLex(), append=True)
			res = calcu.solve()
			window[txtSin].Update(value='\n' + str(res), append=True)

window.close()