import bpy
import os
import sys

from bpy.props import (StringProperty,
                       PointerProperty,
                       )

from bpy.types import (Panel,
                       Operator,
                       AddonPreferences,
                       PropertyGroup,
                       )
location = ""
dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)

from Property_Definition import (MyProperties)

class OBJECT_PT_Folder(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Stellar"
    bl_idname = "OBJ_PT_Folder"
    bl_label = "Folder"

    def draw(self, context):
        layout = self.layout
        scn = context.scene
        col = layout.column(align=True)
        col.prop(scn.my_tool, "path", text="")
        # print the path to the console
        #print (scn.my_tool.path)
        global location 
        location = scn.my_tool.path
        Images()

def Images():
    image_list = [f for f in os.listdir(location) if f.endswith('.tiff')]
    return image_list

classes = (
    MyProperties,
    OBJECT_PT_Folder
)


from bpy.utils import register_class
for cls in classes:
    register_class(cls)

bpy.types.Scene.my_tool = PointerProperty(type=MyProperties)

if __name__ == "Images":
    Images()
