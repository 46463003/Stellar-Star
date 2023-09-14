
####################### SECTION 1 - PREPARATION ####################### 

#----------- import libraries -----------
import bpy  # for interacting with the viewport using Python's code
import os   # for interacting with the operating system
#import Import_Images

#----------- variable declaration -----------
# !!!IMPORTANT: CHANGE THE FILE PATH TO THE IMAGE BEFORE RUNNING THE CODES
# MAKE SURE THE FOLDER IS SEPARATED BY A DOUBLE BACKLASH (\\) INSTEAD OF A SINGLE ONE (\)
images = r"C:\Users\joshu\OneDrive\Documents\Stellar-Star\Sample_Images\1. Helix Nebula @ w = 4844.tiff" #import all images from the sample files
#size = Import_Images.get_image_size()
pixel_length = 4944 #horizontal count of pixels
pixel_width = 3284 # vertical count of pixels
z_scale = 1 # scale of the z axis
#print(pixel_length, pixel_width)
def main():
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



    #######################  SECTION 2 - GRID CREATION ####################### 
    bpy.ops.mesh.primitive_grid_add(size = 2, x_subdivisions = pixel_length, y_subdivisions = pixel_width)  #create grid
    grid = bpy.context.active_object
    grid.scale = (pixel_length/1000, pixel_width/1000, z_scale)  #define scale



    ####################### SECTION 3 - 3D DISPLACEMENT MAP CREATION ####################### 

    #----------- load the image ----------- 
    image = bpy.data.images.load(filepath = images)


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
    image_texture_node.location = (-300,0)
    image_texture_node.image = image # use the loaded image as texture

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

if __name__ == "__main__":
    main()