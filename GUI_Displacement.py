import bpy
import sys
import os
import imp

dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)

from Property_Definition import (StellarPanel)
import Displacement_Map
imp.reload(Displacement_Map)
import New_Image_Locate

class WM_OT_Dismap(bpy.types.Operator):
    bl_label = "Create Displacement_Map"
    bl_idname = "wm.dismap"
    
    #text : bpy.props.StringProperty(name= "Enter Text", default= "")
    red : bpy.props.BoolProperty(name = "Red", default = False)
    green : bpy.props.BoolProperty(name = "Green", default = False)
    blue : bpy.props.BoolProperty(name = "Blue", default = False)
    
    def execute(self, context):
        col = ""
        r = self.red
        g = self.green
        b = self.blue
        if(r is True):
            col = "R"
        if(g is True):
            col = "G"
        if(b is True):
            col = "B"
        Displacement_Map.main(col)
        return {'FINISHED'}
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

class WM_PT_Dismap_Panel(StellarPanel, bpy.types.Panel):
    bl_idname = "PANEL_PT_DISMAP"
    bl_label = "Displacement Map"
    def draw(self,context):
        layout = self.layout
        layout.label(text="This is the displacement panel.")
        row = self.layout.row()
        row.operator("wm.dismap", text = "Displacement_Map")
        if New_Image_Locate.get_path():
            layout.label(text = New_Image_Locate.get_path())
        else:
            layout.label(text = "No Image Selected")

#bpy.utils.register_class(WM_PT_Main_Panel)
#bpy.utils.register_class(WM_OT_Dismap)

