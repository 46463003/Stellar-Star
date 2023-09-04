import bpy
import Displacement_Map
import Displacement_Map_split_by_channel

class MESH_OT_ADD_DISPLACEMENT(bpy.types.Operator):
    bl_idname = "mesh.displacement_map_add"
    bl_label = "Create 3D Displacement Map"
    Displacement_Map.main()

class MESH_OT_ADD_COLOUR_SPLIT(bpy.types.Operator):
    bl_idname = "mesh.colour_split_add"
    bl_label = "Create colour split"
    Displacement_Map_split_by_channel.main()

class VIEW3D_PT_CUSTOM_PANEL(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Displacement_Map"
    bl_category = "Displacement_Map"

    def draw(self, context):
        row = self.layout.row()
        row.operator("mesh.primitive_cube_add", text="Add Cube")
        
        row = self.layout.row()
        row.operator("mesh.displacement_map_add", text = "Add Displacement Map")
        
        row = self.layout.row()
        row.operator("mesh.colour_split_add", text = "Add Colour Split")


bpy.utils.register_class(VIEW3D_PT_CUSTOM_PANEL)
bpy.utils.register_class(MESH_OT_ADD_DISPLACEMENT)
bpy.utils.register_class(MESH_OT_ADD_COLOUR_SPLIT)
