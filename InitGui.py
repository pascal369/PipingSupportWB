#***************************************************************************
#*    Copyright (C) 2023 
#*    This library is free software
#***************************************************************************
import inspect
import os
import sys
import FreeCADGui
import FreeCAD

class PipingSupportShowCommand:
    def GetResources(self):
        file_path = inspect.getfile(inspect.currentframe())
        module_path=os.path.dirname(file_path)
        return { 
          'Pixmap': os.path.join( module_path,"icons","PipingSupport.svg"),
          'MenuText': "PipingSupport",
          'ToolTip': "Show/Hide PipingSupport"}

    def IsActive(self):
        import PipingSupport
        PipingSupport
        return True

    def Activated(self):
        try:
          import PipingSupport
          PipingSuport.main.w.show()
        except Exception as e:
          FreeCAD.Console.PrintError(str(e) + "\n")
        
        file_path = inspect.getfile(inspect.currentframe())
        module_path=os.path.dirname(file_path)

    def IsActive(self):
        import PipingSupport
        return not FreeCAD.ActiveDocument is None

class PipingSupport(FreeCADGui.Workbench):
    def __init__(self):
        file_path = inspect.getfile(inspect.currentframe())
        module_path=os.path.dirname(file_path)
        self.__class__.Icon = os.path.join( module_path,"icons", "PipingSupport.svg")
        self.__class__.MenuText = "PipingSupport"
        self.__class__.ToolTip = "PipingSupport by Pascal"

    def Initialize(self):
        self.commandList = ["PipingSupport_Show"]
        self.appendToolbar("&PipingSupport", self.commandList)
        self.appendMenu("&PipingSupport", self.commandList)

    def Activated(self):
        import PipingSupport
        PipingSupport
        return

    def Deactivated(self):
        return

    def ContextMenu(self, recipient):
        return

    def GetClassName(self): 
        return "Gui::PythonWorkbench"
FreeCADGui.addWorkbench(PipingSupport())
FreeCADGui.addCommand("PipingSupport_Show", PipingSupportShowCommand())
