bl_info = {
    "name" : "Stellar Star",
    "author" : "Innovation Labs",
    "description" : "For astronomers",
    "blender" : (2, 80, 1),
    "version" : (0, 0, 1),
    "location" : "View3D > UI panel > Stellar",
    "categroy" : "Object"
}

import bpy
import sys
import os
import inspect

cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

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