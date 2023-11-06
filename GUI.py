import bpy
import sys
import os
import imp

dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)


bl_info = {
    "name" : "Stellar Star",
    "author" : "Innovation Labs",
    "description" : "For astronomers",
    "blender" : (3, 6, 1),
    "version" : (0, 0, 1),
    "location" : "View3D > UI panel > Stellar",
    "categroy" : "Object"
}
from New_Image_Locate import (CUSTOM_OT_OpenFile, CUSTOM_PT_Panel)
from GUI_Displacement import (WM_OT_Dismap, WM_PT_Dismap_Panel, WM_OT_Id_Stars)
from GUI_AiryDisk import (WM_OT_Airydisk, WM_PT_AD_Panel, WM_OT_OpenFits)



classes = (
    CUSTOM_OT_OpenFile,
    CUSTOM_PT_Panel,
    WM_OT_Dismap,
    WM_PT_Dismap_Panel,
    WM_OT_Id_Stars,
    WM_OT_Airydisk,
    WM_PT_AD_Panel,
    WM_OT_OpenFits
)
def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()