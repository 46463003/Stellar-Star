import bpy
import sys
import os
import imp

#############   is not finished

dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)

def delete_objects():
    for obj in bpy.data.objects:
        bpy.data.objects.remove(obj)

def shading_to_3D():
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D': #once we find the 3D viewport, chnage the view to Material instead of solid
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    # Set the shading mode to 'MATERIAL'
                    space.shading.type = 'MATERIAL'

def grid_creation(pixel_length, pixel_width, z_scale):
    bpy.ops.mesh.primitive_grid_add(size = 2, x_subdivisions = pixel_length, y_subdivisions = pixel_width)  #create grid
    grid = bpy.context.active_object
    grid.scale = (pixel_length/1000, pixel_width/1000, z_scale)  #define scale

def image_loading():
    #----------- create displacement modifier -----------
    displace_modifier = grid.modifiers.new(name = "Stellar_Displacement", type='DISPLACE') #add Displace modifier
    texture = bpy.data.textures.new(name = "Stellar_Texture", type = 'IMAGE') #add an image texture
    displace_modifier.mid_level = 0  #set  mid-level to 0
    texture.image = image  #apply displace texture using the loaded image
    displace_modifier.texture = texture #assign the texture to the Displace modifier

