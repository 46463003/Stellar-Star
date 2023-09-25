import bpy
import sys
import os
import imp

from bpy.props import (StringProperty)

dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)

import Image_Locate
imp.reload(Image_Locate)

#import Displacement_Map_final
#imp.reload(Displacement_Map_final)

#import Displacement_Map_split_by_channel
#imp.reload(Displacement_Map_split_by_channel)


class StellarPanel:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Stellar"

class MESH_PT_Main_Panel(StellarPanel, bpy.types.Panel):
    bl_idname = "PANEL_PT_STELLAR"
    bl_label = "Stellar"

    def draw(self, context):
        layout = self.layout
        for i in Image_Locate.Images():
            layout.label(text= i)

class MESH_PT_Displacement_Panel(StellarPanel, bpy.types.Panel):
    bl_parent_id = "PANEL_PT_STELLAR"
    bl_label = "Displacement_Map"

    def draw(self,context):
        layout = self.layout
        layout.label(text="This is the displacement panel.")

class MESH_PT_Airy_Disk_Panel(StellarPanel, bpy.types.Panel):
    bl_parent_id = "PANEL_PT_STELLAR"
    bl_label = "Airy_Disk"

    def draw(self,context):
        layout = self.layout
        layout.label(text="This is the Airy Disk panel.")

classes = (
    MESH_PT_Main_Panel,
    MESH_PT_Displacement_Panel,
    MESH_PT_Airy_Disk_Panel
)

for cls in classes:
    bpy.utils.register_class(cls)
