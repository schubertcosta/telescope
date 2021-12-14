
FREECADPATH = 'C:/Program Files/FreeCAD 0.19/bin/' # path to your FreeCAD.so or FreeCAD.dll file
from math import pi
import sys
sys.path.append(FREECADPATH)
sys.path.insert(1, '../telescope')
import FreeCAD as App, FreeCADGui as Gui
import time
import constants

class FreeCadAnimation():
    def __init__(self):
        Gui.showMainWindow()
        self.doc = App.open(constants.freecad_path)
        self.adjust_view()
        Gui.updateGui()

    def set_position(self, q_list):
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
    
if __name__ == '__main__':
    FreeCadAnimation()