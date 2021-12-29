import constants
from coords import rad_2_degree 
import sys
sys.path.append(constants.freecad_path)
sys.path.insert(1, '../telescope')
import FreeCAD as App, FreeCADGui as Gui
import time
from PySide2 import QtWidgets

class FreeCadAnimation():
    def __init__(self):
        self.app=QtWidgets.QApplication(sys.argv)
        Gui.showMainWindow()
        self.doc = App.open(constants.freecad_mounting)
        self.adjust_view()
        Gui.updateGui()

    def set_position(self, q_list):
        for (q1, q2) in q_list:            
            time.sleep(0.3)
            q1_degree = rad_2_degree(q1)
            q2_degree = rad_2_degree(q2)
            self.doc.Base_rotativa.Placement=App.Placement(App.Vector(0,0,0), App.Rotation(q1_degree,0,0), App.Vector(0,0,0))
            self.doc.Tubo.Placement=App.Placement(App.Vector(0,0,0), App.Rotation(q1_degree, q2_degree,0), App.Vector(0,0,644))
            self.doc.recompute()
            Gui.updateGui()

    def adjust_view(self):
        Gui.SendMsgToActiveView("ViewFit")
        self.set_position([constants.initial_q_position])

    def free_gui(self):
        time.sleep(0.01)
        Gui.updateGui()
    
if __name__ == '__main__':
    FreeCadAnimation()