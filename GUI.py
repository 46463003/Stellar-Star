import bpy
import Displacement_Map

class MESH_OT_add_Displacement_Map(bpy.types.Operator):
    bl_idname = "mesh.displacement_map_add"
    bl_label = "Create 3D Displacement Map"
    Displacement_Map.main()

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


bpy.utils.register_class(VIEW3D_PT_CUSTOM_PANEL)
bpy.utils.register_class(MESH_OT_add_Displacement_Map)
