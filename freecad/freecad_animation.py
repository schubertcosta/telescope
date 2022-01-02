import logging
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
            self.doc.base.Placement=App.Placement(App.Vector(0,0,0), App.Rotation(q1,0,0), App.Vector(0,0,0))
            self.doc.Corpo_telescopio_114mm_2.Placement=App.Placement(App.Vector(0,0,0), App.Rotation(q1, -q2,0), App.Vector(0,0,constants.l1 * 1000))
            self.doc.recompute()
            Gui.updateGui()

    def adjust_view(self):
        Gui.SendMsgToActiveView("ViewFit")
        Gui.ActiveDocument.ActiveView.setAxisCross(True)
        self.set_position([constants.initial_q_position])

    def free_gui(self):
        time.sleep(0.01)
        Gui.updateGui()
    
if __name__ == '__main__':
    FreeCadAnimation()