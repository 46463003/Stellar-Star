
####################### SECTION 1 - PREPARATION ####################### 

#----------- import libraries -----------
import bpy  # for interacting with the viewport using Python's code
import os   # for interacting with the operating system
import sys
import imp
dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)

import New_Image_Locate
imp.reload(New_Image_Locate)

#----------- variable declaration -----------
# !!!IMPORTANT: CHANGE THE FILE PATH TO THE IMAGE BEFORE RUNNING THE CODES
# MAKE SURE THE FOLDER IS SEPARATED BY A DOUBLE BACKLASH (\\) INSTEAD OF A SINGLE ONE (\)
#file_path = New_Image_Locate.get_path()
#z_scale = 1 # scale of the z axis
#channel_input = "" # R for Red, G for Green, and B for Blue


def main(col):
    channel_input = col # R for Red, G for Green, and B for Blue
    print(channel_input)
    z_scale = 1 # scale of the z axis

    #----------- remove all existing objects in the 3D viewport -----------
    for obj in bpy.data.objects:
        bpy.data.objects.remove(obj)


    # #----------- switch from solid to shading view in the 3D viewport -----------
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D': #once we find the 3D viewport, chnage the view to Material instead of solid
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    # Set the shading mode to 'MATERIAL'
                    space.shading.type = 'MATERIAL'
                    break



    ####################### SECTION 2 - IMAGE PROCESSING ####################### 
    #----------- load the image ----------- 
    image = bpy.data.images.load(filepath = str(New_Image_Locate.get_path()))

    # read the lenght and width of resolution
    pixel_length = image.size[0] #horizontal count of pixels
    pixel_width = image.size[1] # vertical count of pixels


    #----------- select a color channel to display ----------- 
    ### our methodology is to black-out the values of in all color channels that are not chosen
    ### e.g. if Red is chosen, then the values for Green and Blue channels of every pixel will be 0

    # Create a copy of the pixel data
    pixels = list(image.pixels)

    # Find the index based on the specified channel
    if channel_input == "R":
        channel_idx = 0
    elif channel_input == "G":
        channel_idx = 1
    elif channel_input == "B":
        channel_idx = 2
    else:
        raise ValueError("Invalid channel input")

    # Iterate through the pixels in blocks of 4 (R, G, B, A)
    for i in range(0, len(pixels), 4):
        # If it's not the chosen channel, set its value to 0
        for j in range(3):
            if j != channel_idx:
                pixels[i + j] = 0.0


    # Update the image pixels
    image.pixels = pixels



    #######################  SECTION 3 - GRID CREATION ####################### 
    bpy.ops.mesh.primitive_grid_add(size = 2, x_subdivisions = pixel_length, y_subdivisions = pixel_width)  #create grid
    grid = bpy.context.active_object
    grid.scale = (pixel_length/1000, pixel_width/1000, z_scale)  #define scale


    # flip the grid along x-axis by 180 degree
    #grid.rotation_euler[0] = 3.14159



    #######################  SECTION 4 - 3D DISPLACEMENT MAP ####################### 
    #----------- create displacement modifier -----------
    displace_modifier = grid.modifiers.new(name = "Stellar_Displacement", type='DISPLACE') #add Displace modifier
    texture = bpy.data.textures.new(name = "Stellar_Texture", type = 'IMAGE') #add an image texture
    displace_modifier.mid_level = 0  #set  mid-level to 0
    texture.image = image  #apply displace texture using the loaded image
    displace_modifier.texture = texture #assign the texture to the Displace modifier


    #----------- create material to overlay the image colour on the grid -----------
    material = bpy.data.materials.new(name = "Stellar_Material") #create new material
    material.use_nodes = True #enable node trees to overlay color

    # clear default nodes
    nodes = material.node_tree.nodes
    for node in nodes:
        nodes.remove(node)

    # add a Subsurface Scattering shader node
    sss_node = nodes.new(type='ShaderNodeSubsurfaceScattering')
    sss_node.location = (0,0)

    # add an Image Texture node - this allows us to use the color of an external image as texture
    image_texture_node = nodes.new(type='ShaderNodeTexImage')
    image_texture_node.location = (-500,0)
    image_texture_node.image = color_image # use the modified image as texture


    # connect the Image Texture node color to the Subsurface Scattering node color
    material.node_tree.links.new(image_texture_node.outputs["Color"], sss_node.inputs["Color"])

    # add a Material Output node
    material_output = nodes.new(type='ShaderNodeOutputMaterial')
    material_output.location = (400,0)

    # connect Subsurface Scattering node to the Output node
    material.node_tree.links.new(sss_node.outputs["BSSRDF"], material_output.inputs["Surface"])

    # apply the newly-created material to the object
    grid.data.materials.clear()  #clear all existing materials applied on the object
    grid.data.materials.append(material) #apply
    bpy.context.object.active_material.preview_render_type = 'FLAT' #change preview option to Flat



    #######################  SECTION 5 - IDENTIFY SATURATED STARS ####################### 
    # this section relates to the colors will be used to overlay color on the grid as texture

    # create a copy of the input image
    color_image = image.copy()
    color_image.name = "Color image"

    # update the values of color pixels
    color_pixels = list(color_image.pixels)
    for i in range(0, len(color_pixels), 4):
        if channel_input == 'R':
            if color_pixels[i] == 1: # Check if red channel is 1
                color_pixels[i] = 0  # Set red to 0
                color_pixels[i + 1] = 1 # Green
                color_pixels[i + 2] = 1 # Blue
            else:
                color_pixels[i + 1] = 0 # Green
                color_pixels[i + 2] = 0 # Blue
        elif channel_input == 'G':
            if color_pixels[i + 1] == 1: # Check if green channel is 1
                color_pixels[i] = 1 # Red
                color_pixels[i + 1] = 0  # Set green to 0
                color_pixels[i + 2] = 1 # Blue
            else:
                color_pixels[i] = 0 # Red
                color_pixels[i + 2] = 0 # Blue
        elif channel_input == 'B':
            if color_pixels[i + 2] == 1: # Check if blue channel is 1
                color_pixels[i] = 1 # Red
                color_pixels[i + 1] = 1 # Green
                color_pixels[i + 2] = 0  # Set blue to 0
            else:
                color_pixels[i] = 0 # Red
                color_pixels[i + 1] = 0 # Green

    # Update the color_image pixels with new color changes
    color_image.pixels = color_pixels
    image_texture_node.image = color_image

if __name__ == "__main__":
    main()

