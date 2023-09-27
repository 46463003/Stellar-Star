import typing
import bpy
import sys
import os
import imp

from bpy.types import Context

dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)

from Property_Definition import (StellarPanel)
import Airy_Disk
imp.reload(Airy_Disk)

class WM_OT_Airydisk(bpy.types.Operator):
    bl_label = "Create Airy Disk"
    bl_idname = "wm.airydisk"
    focal_lenght : bpy.props.StringProperty(name = "Focal Length", default = "")
    aperture : bpy.props.StringProperty(name = "Aperture", default = "")
    pixel_size : bpy.props.StringProperty(name = "Pixel Size", default = "")
    wavelength : bpy.props.StringProperty(name = "Wavelength", default = "")

    def execute(self, context):
        fl = self.focal_lenght
        a = self.aperture
        p = self.pixel_size
        w = self.wavelength
        Airy_Disk.set_val(fl, a, p, w)
        Airy_Disk.main()
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self) 

class WM_PT_AD_Panel(StellarPanel, bpy.types.Panel):
    bl_idname = "PANEL_PT_AIRYDISK"
    bl_label = "Airy Disk"
    def draw(self,context):
        layout = self.layout
        layout.label(text="This is the Airy Disk panel.")
        row = self.layout.row()
        row.operator("wm.airydisk", text = "Airy Disk")

#bpy.utils.register_class(WM_OT_Airydisk)
#bpy.utils.register_class(WM_PT_Main_Panel)