import bpy
import sys
import os
import imp

dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)

from New_Image_Locate import (CUSTOM_OT_OpenFile, CUSTOM_PT_Panel)
from GUI_Displacement import (WM_OT_Dismap, WM_PT_Dismap_Panel)
from GUI_AiryDisk import (WM_OT_Airydisk, WM_PT_AD_Panel, WM_OT_OpenFits)

classes = (
    CUSTOM_OT_OpenFile,
    CUSTOM_PT_Panel,
    WM_OT_Dismap,
    WM_PT_Dismap_Panel,
    WM_OT_Airydisk,
    WM_PT_AD_Panel,
    WM_OT_OpenFits
)

for cls in classes:
    bpy.utils.register_class(cls)