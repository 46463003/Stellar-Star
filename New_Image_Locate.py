import bpy
import os
import sys
import inspect

path = ""
cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

from Property_Definition import (StellarPanel)

class CUSTOM_OT_OpenFile(bpy.types.Operator):
    bl_idname = "open.file"
    bl_label = "Select Image"
    filepath : bpy.props.StringProperty(subtype="DIR_PATH") 
    #somewhere to remember the address of the file

    def execute(self, context):
        display = self.filepath 
        global path
        path = display 
        print("path:", display) #Prints to console  
        print(get_path())
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
    bl_idname = "IMAGESELECT_PT_PANEL"
    bl_label = "Select Image Panel"

    def draw(self, context):
        layout = self.layout
        layout.row()
        layout.operator("open.file", text = "Select Image")
        if get_path():
            layout.label(text = get_path())
        else:
            layout.label(text = "No Image Selected")

def get_path():
    newp = ""
    for p in path:
        if p == '\\':
            newp = newp + p + "\\"
        else:
            newp = newp + p
    return str(newp)

#bpy.utils.register_class(CUSTOM_PT_Panel)

#bpy.utils.register_class(CUSTOM_OT_OpenFile)