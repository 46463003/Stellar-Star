import bpy

class VIEW3D_PT_CUSTOM_PANEL(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Custom Panel"
    bl_category = "Custom Catergory"

    def draw(self, context):
        #self.layout.label(text="Hello World")
        pass

bpy.utils.register_class(VIEW3D_PT_CUSTOM_PANEL)
