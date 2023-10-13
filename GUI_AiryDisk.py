import typing
import bpy
import sys
import os
import inspect
import imp

from bpy.types import Context

cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
fits = ""
from Property_Definition import (StellarPanel)
import Airy_Disk
imp.reload(Airy_Disk)

class WM_OT_OpenFits(bpy.types.Operator):
    bl_idname = "open.fits"
    bl_label = "Select fits file"
    filepath : bpy.props.StringProperty(subtype="DIR_PATH") 

    def execute(self, context):
        display = self.filepath 
        global fits
        fits = display 
        print("path:", display)
        Airy_Disk.pathway(fits)        
        return {'FINISHED'}

    def invoke(self, context, event):

        context.window_manager.fileselect_add(self) 

        return {'RUNNING_MODAL'}  

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
class WM_OT_Circle(StellarPanel, bpy.types.Panel):
    bl_idname = "wm.createcircle"
    bl_label = "Create Circle"

class WM_PT_AD_Panel(StellarPanel, bpy.types.Panel):
    bl_idname = "PANEL_PT_AIRYDISK"
    bl_label = "Airy Disk"
    def draw(self,context):
        layout = self.layout
        layout.label(text="This is the Airy Disk panel.")
        layout.row()
        layout.operator("open.fits", text = "Select fits file")
        if get_fits():
            layout.label(text = get_fits())
        else:
            layout.label(text = "No Image Selected")
        layout.row()
        row = self.layout.row()
        row.operator("wm.airydisk", text = "Airy Disk")
        layout.row
        row.operator("wm.createcircle", text = "Create Circle")


def get_fits():
    newf = ""
    for p in fits:
        if p == '\\':
            newf = newf + p + "\\"
        else:
            newf = newf + p
    return str(newf)
#bpy.utils.register_class(WM_OT_Airydisk)
#bpy.utils.register_class(WM_PT_Main_Panel)