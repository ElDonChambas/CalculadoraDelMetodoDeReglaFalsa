from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtGui import QFont, QFontDatabase
import sys
import sympy
import os
import math
import re

everythingFine = False
errorAnumber = False
everythingFine = False
var_symbol = sympy
formula_expr = sympy
ite = 1
a = 0
b = 0
Fa = 0.0
Fb = 0.0
oldxi = 0.0
xi = 0.0
Fxi = 0.0
iError = float('inf')
errorAmount = 0
        
class mainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent = None):
        super(mainWindow, self).__init__(parent)

        bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
        menu = os.path.abspath(os.path.join(bundle_dir, 'interfaces\Main_window.ui'))

        uic.loadUi(menu, self)
        self.show()
        
        
        #Alineando el texto de las celdas al centro
        class AlignDelegate(QtWidgets.QStyledItemDelegate):
            def initStyleOption(self, option, index):
                super(AlignDelegate, self).initStyleOption(option, index)
                option.displayAlignment = QtCore.Qt.AlignCenter
        delegate = AlignDelegate(self.table)
        self.table.setItemDelegate(delegate)

        #Dando formato a la tabla, anchos de columna
        self.table.setColumnWidth(0, 50)
        self.table.setColumnWidth(1, 115)
        self.table.setColumnWidth(2, 115)
        self.table.setColumnWidth(3, 115)
        self.table.setColumnWidth(4, 115)
        self.table.setColumnWidth(5, 115)
        self.table.setColumnWidth(6, 115)
        self.table.setColumnWidth(7, 115)
        
        #No mostrar la fila de encabezado ni mensaje de error
        self.table.verticalHeader().setVisible(False)
        self.errorLabel.setVisible(False)

        #boton de calculadora para simbolos de la funcion
        self.calculatorFunc.clicked.connect(lambda: calculator(self).exec_())
        self.TeamBtn.clicked.connect(lambda: desarrolladores(self).exec_())
        self.Tutorial.clicked.connect(lambda: TutorialWindow(self).exec_())

        #limitando numeros de a, b y el error
        self.variableLine.setMaxLength(1)
        self.intervalA.setValidator(QIntValidator(-100000, 100000))
        self.intervalB.setValidator(QIntValidator(-100000, 100000))
        self.errorLine.setText("0.000010")
        
        #validando datos
        def generarTabla():

            global a, b, Fa, Fb, formula_expr, var_symbol, everythingFine, errorAnumber, errorAmount
            everythingFine = False
            errorAnumber = False
            variable = (self.variableLine.text())
            if variable == "":
                self.errorLabel.setText("ERROR: Por favor, ingrese una variable.")
                self.errorLabel.setVisible(True)
                return
            elif variable.isnumeric():
                self.errorLabel.setText("ERROR: La variable no puede ser un número.")
                self.errorLabel.setVisible(True)
                return
            elif variable.lower() in ("a", "b"):
                self.errorLabel.setText("ERROR: La variable no puede ser a o b.")
                self.errorLabel.setVisible(True)
                return
            else:
                var_symbol = sympy.symbols(variable)
                self.errorLabel.setVisible(False)
                a = self.intervalA.text()
                if a.lstrip("-").isnumeric() == False: 
                    self.errorLabel.setText("ERROR: a debe ser un número.")
                    self.errorLabel.setVisible(True)
                    return
                else:
                    self.errorLabel.setVisible(False)
                    a = float(a)

                    b = self.intervalB.text()
                    if b.lstrip("-").isnumeric() == False:
                        self.errorLabel.setText("ERROR: b debe ser un número.")
                        self.errorLabel.setVisible(True)
                        return
                    else:
                        self.errorLabel.setVisible(False)
                        b = float(b)
                        errorAmount = self.errorLine.text()
                        if errorAmount == "":
                            self.errorLabel.setText("ERROR: El error debe ser un número.")
                            self.errorLabel.setVisible(True)
                            return
                        else:
                            self.errorLabel.setVisible(False)

                            if (float(a) == float(b)) == True:
                                self.errorLabel.setText("Error Matematico: a y b no pueden ser iguales.")
                                self.errorLabel.setVisible(True)
                            else:
                                self.errorLabel.setVisible(False)
                                try:
                                    errorAmount = float(errorAmount)
                                    errorANumber = True
                                except ValueError:
                                    self.errorLabel.setText("ERROR: El error debe ser un número.")
                                    self.errorLabel.setVisible(True)
                                    return
                                    
                                if errorANumber and errorAmount < 0.000000000000000000000000001:
                                    self.errorLabel.setText("ERROR: El error debe ser un número positivo y mayor que cero.")
                                    self.errorLabel.setVisible(True)
                                    return
                                else:
                                    errorAmount = float(errorAmount)
                                    self.errorLabel.setVisible(False)

                                    formula = self.funcionLine.text()
                                    # Definir caracteres permitidos (caracteres matematicos y la variable definida anteriormente)
                                    allowed_chars = f"[{re.escape(variable.lower())}{re.escape(variable.upper())}0-9+*/()-^.]"
                                    # Revisar si hay caracteres no permitidos
                                    if re.fullmatch(allowed_chars + '*', formula):
                                        if ((variable.lower() in formula) or (variable.upper() in formula)):
                                            try:
                                                var_symbol = sympy.symbols(variable)
                                                formula_expr = formula.replace(variable.lower(), 'var_symbol').replace(variable.upper(), 'var_symbol').replace("√", 'math.sqrt').replace("^", '**')
                                                formula_expr = eval(formula_expr)
                                                Fa = formula_expr.subs(var_symbol, a)
                                                Fb = formula_expr.subs(var_symbol, b)
                                                calculateXi()
                                                
                                                #Se toma ruta a
                                                if (Fa<0) and (Fxi<0):
                                                    tableRow()
                                                    replaceA()
                                                    a_Route()

                                                    #Se toma ruta b
                                                elif (Fb>0) and (Fxi>0):
                                                    tableRow()
                                                    replaceB()
                                                    b_Route()

                                                    #No hay ruta a tomar pues no converge
                                                else:
                                                    self.errorLabel.setText("No converge.")
                                                    self.errorLabel.setVisible(True)
                                            except ValueError:
                                                self.errorLabel.setText("ERROR: La función debe contener la variable definida.")
                                                self.errorLabel.setVisible(True)
                                                return
                                            except NameError:
                                                self.errorLabel.setText("ERROR: La función debe contener la variable definida.")
                                                self.errorLabel.setVisible(True)
                                                return
                                            except SyntaxError:
                                                self.errorLabel.setText("ERROR: La función debe ser una expresión matemática válida.")
                                                self.errorLabel.setVisible(True)
                                                return
                                        else:
                                            self.errorLabel.setText("ERROR: La función debe contener la variable definida.")
                                            self.errorLabel.setVisible(True)
                                    else:
                                        self.errorLabel.setText("La formula contiene más de una variable o caracteres no permitidos. Por favor, ingrese una formula válida.")
                                        self.errorLabel.setVisible(True)                

        self.generar.clicked.connect(lambda:generarTabla())

        def limpiarTabla():
            global everythingFine, errorAnumber, var_symbol, formula_expr, ite, a, b, Fxi, Fa, Fb, oldxi, xi, iError
            everythingFine = False
            errorAnumber = False
            var_symbol = sympy
            formula_expr = sympy
            ite = 1
            a = 0
            b = 0
            Fa = 0.0
            Fb = 0.0
            oldxi = 0.0
            xi = 0.0
            Fxi = 0.0
            iError = float('inf')
            for i in reversed(range(self.table.rowCount())):
                self.table.removeRow(i)
                self.table.setRowCount(0)
            self.errorLabel.setVisible(False)
            self.generar.setEnabled(True)
            self.errorLine.setText("0.000010")
            self.variableLine.setText("")
            self.funcionLine.setText("")
            self.intervalA.setText("")
            self.intervalB.setText("")

        self.limpiar.clicked.connect(lambda:limpiarTabla())
        def tableRow():
            global ite, a, Fa, b, Fb, xi, Fxi, iError
            self.table.setRowCount(ite)
            if iError == float("inf"):
                self.table.setItem(ite-1, 0, QTableWidgetItem(str(ite)))
                self.table.setItem(ite-1, 1, QTableWidgetItem(str("%.6f" % a)))
                self.table.setItem(ite-1, 2, QTableWidgetItem(str("%.6f" %b)))
                self.table.setItem(ite-1, 3, QTableWidgetItem(str("%.6f" %Fa)))
                self.table.setItem(ite-1, 4, QTableWidgetItem(str("%.6f" %Fb)))
                self.table.setItem(ite-1, 5, QTableWidgetItem(str("%.6f" %xi)))
                self.table.setItem(ite-1, 6, QTableWidgetItem(str("%.6f" %Fxi)))
                self.table.setItem(ite-1, 7, QTableWidgetItem(str("----------")))
            else:
                self.table.setItem(ite-1, 0, QTableWidgetItem(str(ite)))
                self.table.setItem(ite-1, 1, QTableWidgetItem(str("%.6f" %a)))
                self.table.setItem(ite-1, 2, QTableWidgetItem(str("%.6f" %b)))
                self.table.setItem(ite-1, 3, QTableWidgetItem(str("%.6f" %Fa)))
                self.table.setItem(ite-1, 4, QTableWidgetItem(str("%.6f" %Fb)))
                self.table.setItem(ite-1, 5, QTableWidgetItem(str("%.6f" %xi)))
                self.table.setItem(ite-1, 6, QTableWidgetItem(str("%.6f" %Fxi)))
                self.table.setItem(ite-1, 7, QTableWidgetItem(str("%.6f" %iError)))           
                                
        #Ruta de A
        def a_Route():
            global ite, a, Fa, b, Fb, xi, Fxi, iError
            while (iError > errorAmount):
                if (iError < 0.0000001):
                    break
                else:
                    ite += 1
                    calculateXi()
                    calculateError()
                    if convergencia() == False:
                        break
                    tableRow()
                    replaceA()
            self.generar.setEnabled(False)
            self.errorLabel.setText("La respuesta es: %.6f" % xi)
            self.errorLabel.setVisible(True) 

        #Ruta de B
        def b_Route():
            global ite, a, Fa, b, Fb, xi, Fxi, iError
            while (iError > errorAmount):
                if (iError < 0.0000001):
                    break
                else:
                    ite += 1
                    calculateXi()
                    calculateError()
                    if convergencia() == False:
                        break
                    tableRow()
                    replaceB()
            self.generar.setEnabled(False)
            self.errorLabel.setText("La respuesta es: xi = %.6f" % xi)
            self.errorLabel.setVisible(True) 

        #reemplaza a por el resultado de Xi, y F(a) for f(Xi) si es necesario (solo en ruta de a)
        def replaceA():
            global a, Fa
            a = xi
            Fa = Fxi

        #reemplaza b por el resultado de Xi, y F(b) for f(Xi) si es necesario (solo en ruta de b)
        def replaceB():
            global b, Fb
            b = xi
            Fb = Fxi

        #calcula Xi
        def calculateXi():
            global a, Fa, b, Fb, xi, Fxi, oldxi, formula_expr, var_symbol
            oldxi = xi
            xi = a + ((a - b) * (Fa)) / (Fb - Fa)
            Fxi = formula_expr.subs(var_symbol, xi)

        #calcula el error
        def calculateError():
            global iError
            iError = abs(xi - oldxi)

        #Chequeo de convergencia
        def convergencia():
            return ((Fa*Fb)<0)
        
        self.formula_tomada = ""
    #agregar funcion de la calculadora a la ventana principal
    def agregarFuncion(self):
        self.funcionLine.setText(self.formula_tomada)


class calculator(QDialog):
    def __init__(self, main_window):
        super(calculator, self).__init__()
        self.main_window = main_window
        bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
        calcui = os.path.abspath(os.path.join(bundle_dir, 'interfaces\calculadoraFuncion.ui'))
        uic.loadUi(calcui, self)

        self.uno.clicked.connect(lambda: agregarTexto(self, '1'))
        self.dos.clicked.connect(lambda: agregarTexto(self, '2'))
        self.tres.clicked.connect(lambda: agregarTexto(self, '3'))
        self.cuatro.clicked.connect(lambda: agregarTexto(self, '4'))
        self.cinco.clicked.connect(lambda: agregarTexto(self, '5'))
        self.seis.clicked.connect(lambda: agregarTexto(self, '6'))
        self.siete.clicked.connect(lambda: agregarTexto(self, '7'))
        self.ocho.clicked.connect(lambda: agregarTexto(self, '8'))
        self.nueve.clicked.connect(lambda: agregarTexto(self, '9'))
        self.ceroBtn.clicked.connect(lambda: agregarTexto(self, '0'))

        self.quitar.clicked.connect(lambda: borrarUltimo(self))
        self.diezElevado.clicked.connect(lambda: agregarTexto(self, '*10^'))
        self.division.clicked.connect(lambda: agregarTexto(self, '/'))
        self.elevar.clicked.connect(lambda: agregarTexto(self, '^'))
        self.equis.clicked.connect(lambda: agregarTexto(self, 'x'))
        self.mas.clicked.connect(lambda: agregarTexto(self, '+'))
        self.menos.clicked.connect(lambda: agregarTexto(self, '-'))
        self.multiplicacion.clicked.connect(lambda: agregarTexto(self, '*'))

        self.parentDer.clicked.connect(lambda: agregarTexto(self, ')'))
        self.parentIzq.clicked.connect(lambda: agregarTexto(self, '('))
        self.punto.clicked.connect(lambda: agregarTexto(self, '.'))
        self.raiz.clicked.connect(lambda: agregarTexto(self, '√()'))
        self.ye.clicked.connect(lambda: agregarTexto(self, 'y'))

        self.borrar.clicked.connect(lambda: borrarTodo(self))

        self.proceder.clicked.connect(lambda: completed(self))

        def agregarTexto(self, text):
            current_text = self.funcLine.text()
            new_text = current_text + text
            self.funcLine.setText(new_text)

        def borrarUltimo(self):
            current_text = self.funcLine.text()
            if current_text:
                new_text = current_text[:-1]
                self.funcLine.setText(new_text)

        def borrarTodo(self):
            self.funcLine.setText("")

        def completed(self):
            formula = self.funcLine.text()
            self.main_window.formula_tomada = formula
            self.main_window.agregarFuncion()
            self.accept()

        def close_dialog(self):
            self.accept()

        self.exit.clicked.connect(lambda: close_dialog(self))

class desarrolladores(QDialog):
    def __init__(self, main_window):
        super(desarrolladores, self).__init__()
        self.main_window = main_window
        bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
        desarrolladoresUI = os.path.abspath(os.path.join(bundle_dir, 'interfaces\desarrolladores.ui'))
        uic.loadUi(desarrolladoresUI, self)
        self.exit.clicked.connect(lambda:self.accept())

class TutorialWindow(QDialog):
    def __init__(self, main_window):
        super(TutorialWindow, self).__init__()
        self.main_window = main_window
        bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
        tutorialUI = os.path.abspath(os.path.join(bundle_dir, 'interfaces\Tutorial.ui'))
        uic.loadUi(tutorialUI, self)
        self.exit.clicked.connect(lambda:self.accept())

#Se ejecuta el programa
app = QtWidgets.QApplication(sys.argv)
window = mainWindow()
app.exec_()