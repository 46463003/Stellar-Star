import bpy

from bpy.props import (StringProperty,
                       BoolProperty,
                       PointerProperty,
                       )

from bpy.types import (Panel,
                       Operator,
                       AddonPreferences,
                       PropertyGroup,
                       )

class MyProperties(PropertyGroup):

    my_path : StringProperty(
        name="",
        description="Path to Directory",
        default="",
        maxlen=1024,
        subtype='DIR_PATH')
    
class StellarPanel:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Stellar"
    