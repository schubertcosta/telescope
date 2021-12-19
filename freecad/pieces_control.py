
from math import pi
import constants
import sys
sys.path.append(constants.freecad_path)
sys.path.insert(1, '../telescope')
import FreeCAD as App, FreeCADGui as Gui
import time
from PySide2 import QtWidgets

class FreeCadAnimation():
    def __init__(self):
        # self.app=QtWidgets.QApplication(sys.argv)
        Gui.showMainWindow()
        self.doc = App.open(constants.freecad_mounting)
        self.adjust_view()
        Gui.updateGui()

    def set_position(self, q_list):
        print(q_list)
        for (q1, q2) in q_list:
            time.sleep(0.5)
            self.doc.Base_rotativa.Placement=App.Placement(App.Vector(0,0,0), App.Rotation(q1 * 180/pi,0,0), App.Vector(0,0,0))
            self.doc.Tubo.Placement=App.Placement(App.Vector(0,0,0), App.Rotation(q1* 180/pi,q2* 180/pi,0), App.Vector(0,0,644))
            self.doc.recompute()
            Gui.updateGui()

    def adjust_view(self):
        Gui.activeDocument().activeView().setCameraType("Perspective")
        Gui.runCommand('Std_OrthographicCamera',0)
        Gui.runCommand('Std_PerspectiveCamera',1)
        Gui.activeDocument().activeView().viewIsometric()
        Gui.ActiveDocument.ActiveView.setAxisCross(True)
        self.set_position([constants.initial_q_position])
    
if __name__ == '__main__':
    FreeCadAnimation()