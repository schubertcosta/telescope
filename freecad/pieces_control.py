
FREECADPATH = 'C:/Program Files/FreeCAD 0.19/bin/' # path to your FreeCAD.so or FreeCAD.dll file
import sys
sys.path.append(FREECADPATH)
import FreeCAD as App, FreeCADGui as Gui
import time
import constants

def set_position(doc, q_list):
    for (q1, q2) in q_list:
        time.sleep(0.5)
        doc.Base_rotativa.Placement=App.Placement(App.Vector(0,0,0), App.Rotation(q1,0,0), App.Vector(0,0,0))
        doc.Tubo.Placement=App.Placement(App.Vector(0,0,0), App.Rotation(q1,q2,0), App.Vector(0,0,644))
        doc.recompute()
        Gui.updateGui()

def adjust_view():
    Gui.activeDocument().activeView().setCameraType("Perspective")
    Gui.runCommand('Std_OrthographicCamera',0)
    Gui.runCommand('Std_PerspectiveCamera',1)
    Gui.activeDocument().activeView().viewIsometric()
    Gui.ActiveDocument.ActiveView.setAxisCross(True)

def start_freecad():
    Gui.showMainWindow()
    doc = App.open(constants.freecad_path)
    adjust_view()
    return doc
