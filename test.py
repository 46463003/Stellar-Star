import bpy
import os
import sys
dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)

from Property_Definition import (StellarPanel)

class CUSTOM_OT_OpenBrowser(bpy.types.Operator):
    bl_idname = "open.browser"
    bl_label = "Select Image"

    filepath : bpy.props.StringProperty(subtype="DIR_PATH") 
    #somewhere to remember the address of the file


    def execute(self, context):
        display = "filepath = ", str(self.filepath)  
        print(display) #Prints to console  
        #Window>>>Toggle systen console

        return {'FINISHED'}

    def invoke(self, context, event): # See comments at end  [1]

        context.window_manager.fileselect_add(self) 
        #Open browser, take reference to 'self' 
        #read the path to selected file, 
        #put path in declared string type data structure self.filepath

        return {'RUNNING_MODAL'}  
        # Tells Blender to hang on for the slow user input

class CUSTOM_PT_Panel(StellarPanel, bpy.types.Panel):
    bl_idname = "CUSTON_PT_PANEL"
    bl_label = "My Custom Panel"

# Zeichnet den Button zum Öffnen des Message Fensters
    def draw(self, context):
        layout = self.layout
        layout.row()
        layout.operator("open.browser", text = "Browser Bowser")

bpy.utils.register_class(CUSTOM_PT_Panel)

bpy.utils.register_class(CUSTOM_OT_OpenBrowser)

