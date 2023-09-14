import bpy
import sys
import os
import imp

dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)

import Displacement_Map_final
imp.reload(Displacement_Map_final)

import Displacement_Map_split_by_channel
imp.reload(Displacement_Map_split_by_channel)

import Airy_Disk
imp.reload(Airy_Disk)

class MESH_OT_ADD_DISPLACEMENT(bpy.types.Operator):
    bl_idname = "mesh.displacement_map_add"
    bl_label = "Create 3D Displacement Map"
    def execute(self, context):
        Displacement_Map_final.main()
        return {'FINISHED'}

class MESH_OT_ADD_COLOUR_SPLIT(bpy.types.Operator):
    bl_idname = "mesh.colour_split_add"
    bl_label = "Create colour split"
    def execute(self, context):
        Displacement_Map_split_by_channel.main()
        return {'FINISHED'}

class MESH_OT_RED(bpy.types.Operator):
    bl_idname = "mesh.red"
    bl_label = "Red"
    def execute(self, context):
        Displacement_Map_final.colour_value("R")
        return {'FINISHED'}

class MESH_OT_GREEN(bpy.types.Operator):
    bl_idname = "mesh.green"
    bl_label = "Green"
    def execute(self, context):
        Displacement_Map_final.colour_value("G")
        return {'FINISHED'}

class MESH_OT_BLUE(bpy.types.Operator):
    bl_idname = "mesh.blue"
    bl_label = "Blue"
    def execute(self, context):
        Displacement_Map_final.colour_value("B")
        return {'FINISHED'}

class MESH_OT_AIRY_DISK(bpy.types.Operator):
    bl_idname = "mesh.airy_disk"
    bl_label = "Airy_Disk"
    def execute(self, context):
        Airy_Disk.main()

class VIEW3D_PT_CUSTOM_PANEL(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Stellar"
    bl_category = "Stellar"
    #filename_ext = "*.png;*.jpg;*.jpeg;*.fits;*.tif;*.tiff" #

    def draw(self, context):
        row = self.layout.row()
        row.operator("mesh.primitive_cube_add", text="Add Cube")
        
        row = self.layout.row()
        row.operator("mesh.displacement_map_add", text = "Add Displacement Map")
        
        row = self.layout.row()
        row.operator("mesh.colour_split_add", text = "Add Colour Split")

        row = self.layout.row()
        row.operator("mesh.red", text = "Red")

        row = self.layout.row()
        row.operator("mesh.green", text = "Green")

        row = self.layout.row()
        row.operator("mesh.blue", text = "Blue")

bpy.utils.register_class(VIEW3D_PT_CUSTOM_PANEL)
bpy.utils.register_class(MESH_OT_ADD_DISPLACEMENT)
bpy.utils.register_class(MESH_OT_ADD_COLOUR_SPLIT)
bpy.utils.register_class(MESH_OT_RED)
bpy.utils.register_class(MESH_OT_GREEN)
bpy.utils.register_class(MESH_OT_BLUE)

