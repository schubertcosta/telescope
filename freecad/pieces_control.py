
FREECADPATH = 'C:/Program Files/FreeCAD 0.19/bin/' # path to your FreeCAD.so or FreeCAD.dll file
import sys
sys.path.append(FREECADPATH)
from PySide2 import QtCore, QtGui, QtWidgets
import FreeCAD as App, FreeCADGui as Gui
import time


def test(app):
    acum = 0
    for i in range(20):            
        time.sleep(0.5)
        doc.Base_rotativa.Placement=App.Placement(App.Vector(0,0,0), App.Rotation(acum + 25,0,0), App.Vector(0,0,0))
        doc.Tubo.Placement=App.Placement(App.Vector(0,0,0), App.Rotation(acum + 25,acum + 10,0), App.Vector(0,0,644))
        doc.recompute()
        acum = acum + 25
        Gui.updateGui()

app=QtWidgets.QApplication(sys.argv)
Gui.showMainWindow()
doc = App.open("G:\\Meu Drive\\Projetos\\Telescopio\\CAD\\First version1\\monting.FCStd")
Gui.activeDocument().activeView().setCameraType("Perspective")
Gui.runCommand('Std_OrthographicCamera',0)
Gui.runCommand('Std_PerspectiveCamera',1)
Gui.activeDocument().activeView().viewIsometric()
Gui.ActiveDocument.ActiveView.setAxisCross(True)
test(app)
app.exec_()
