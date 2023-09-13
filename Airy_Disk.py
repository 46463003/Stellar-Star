######################## SECTION 1 - PREPARATION ########################

#----------- import libraries -----------
import bpy  # for interacting with the viewport using Python's code
from astropy.io import fits


#----------- variable declaration -----------
corr_fits = "C:/Course Materials/COMP3850/Blender/plate_solved_results/corr.fits"
f = 995.93931*10**-3 # focal length in meters
channel_input = "G" # R for Red, G for Green, and B for Blue

# wavelength for different color channel
if channel_input == "R":
    lambda_w = 650*10**-9
elif channel_input == "G":
    lambda_w = 520*10**-9
elif channel_input == "B":
    lambda_w = 450*10**-9


#----------- import data file -----------
with fits.open(corr_fits) as hdul:
    data = [list(row) for row in hdul[1].data]
hdul.close()


#----------- clean all circles in the viewport -----------
for obj in bpy.data.objects:
    if obj.name != "Grid":
        bpy.data.objects.remove(obj)

######################## SECTION 2 - DRAW A CIRCLE AROUND REFERENCE STARS ########################

grid = bpy.data.objects["Grid"]

# set the scale
cell_length = (grid.scale.x * 2) / (grid.scale.x*1000)
cell_width = (grid.scale.y * 2 )/ (grid.scale.y*1000)

# Define material for the AD circles
if "ADMaterial" not in bpy.data.materials:
    AD_mat = bpy.data.materials.new(name = "ADMaterial")
    
    # assign colors to the AD based on the selected channels
    if channel_input == "R":
        AD_mat.diffuse_color = (0, 1, 1, 1)  # cyan for Red
    elif channel_input == "G":
        AD_mat.diffuse_color = (1, 0, 1, 1)  # magenta for Green 
    elif channel_input == "B":
        AD_mat.diffuse_color = (1, 1, 0, 1)  # yellow for Blue
else:
    AD_mat = bpy.data.materials["ADMaterial"]
    

#----------- draw the Airy Disk -----------
for i, row in enumerate(data):
    x = row[4] * cell_length - grid.scale.x  # Translate and scale x-coordinate
    y = row[5] * cell_width - grid.scale.y  # Translate and scale y-coordinate
    
    # Add a circle curve for each reference star
    bpy.ops.mesh.primitive_circle_add(radius=0.5, location=(x, y, 0))
    circle = bpy.context.active_object  # This is the mesh circle

    # Convert the mesh circle to a curve
    bpy.ops.object.convert(target='CURVE')
    circle = bpy.context.active_object  # This is now the curve circle

    # Adjust the curve properties
    circle.data.bevel_depth = 0.001

    # Assign colors to the AD
    if circle.data.materials:
        circle.data.materials[0] = AD_mat
    else:
        circle.data.materials.append(AD_mat)
