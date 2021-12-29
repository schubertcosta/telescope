
# FREECADPATH = 'C:/Program Files/FreeCAD 0.19/bin/' # path to your FreeCAD.so or FreeCAD.dll file
# import sys
# sys.path.append(FREECADPATH)


# from PySide2 import QtCore, QtGui, QtWidgets
# import FreeCAD as App, FreeCADGui as Gui


# def test(app):
#     acum = 0
#     for i in range(20):            
#         time.sleep(0.5)
#         doc.Base_rotativa.Placement=App.Placement(App.Vector(0,0,0), App.Rotation(acum + 25,0,0), App.Vector(0,0,0))
#         doc.Tubo.Placement=App.Placement(App.Vector(0,0,0), App.Rotation(acum + 25,acum + 10,0), App.Vector(0,0,644))
#         doc.recompute()
#         acum = acum + 25
#         Gui.updateGui()
#         # app.processEvents()
        
# # 

# app=QtWidgets.QApplication(sys.argv)

# Gui.showMainWindow()

# import time
# # doc.recompute()

# doc = App.open("G:\\Meu Drive\\Projetos\\Telescopio\\CAD\\First version1\\monting.FCStd")
# Gui.activeDocument().activeView().setCameraType("Perspective")
# Gui.runCommand('Std_OrthographicCamera',0)
# Gui.runCommand('Std_PerspectiveCamera',1)
# Gui.activeDocument().activeView().viewIsometric()
# Gui.ActiveDocument.ActiveView.setAxisCross(True)
# test(app)

# # creates a document and a Part feature with the cube
# # Part.show(cube)
# # app.processEvents()
# # app.processEvents()
# app.exec_()

# import matplotlib.pyplot as plt
# import numpy as np
# f, axes = plt.subplots(1,2)  # 1 row containing 2 subplots.

# # Plot random points on one subplots.
# axes[0].scatter(np.random.randn(10), np.random.randn(10))

# # Plot histogram on the other one.
# axes[1].hist(np.random.randn(100))

# # Adjust the size and layout through the Figure-object.
# f.set_size_inches(10, 5)
# f.tight_layout()
# plt.show()


import numpy as np

# matrix = np.array([[2,2,2,2],[4,4,4,4],[6,6,6,6], [10,10,10,10]])

# vector = np.array([2,4,6,10])
# print(matrix)
# print(vector.reshape(4,1))

# aa = np.linalg.lstsq(matrix, vector.reshape(4,1))
# print(np.array(aa))

print(5*np.eye(3))