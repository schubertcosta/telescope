# import FreeCAD as App, FreeCADGui as Gui

# def get_solid_mass(solid_name, is_inverted):
#     model = App.ActiveDocument.getObject(solid_name)
#     model_copy = model.Shape.copy()
#     raw_volume = model_copy.Volume
#     return raw_volume_


# copy().getMomentOfInertia(App.Vector(0,0,0),App.Vector(0,0,1))


# model = FreeCADGui.Selection.getSelection()[0]
# test = model.Shape.copy()
# aaa = test.getMomentOfInertia(App.Vector(0,0,0),App.Vector(1,1,0))
# ccc = aaa*(10**-3)**2*1.24
# ccc

# obj = FreeCADGui.Selection.getSelection()[0]
# globalRotMatrix = obj.getGlobalPlacement().Rotation.toMatrix()
# globalmoiObj = obj.Shape.MatrixOfInertia
# localmoiObj =  globalRotMatrix.transposed() * globalmoiObj * globalRotMatrix