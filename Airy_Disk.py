######################## SECTION 1 - PREPARATION ########################
#----------- import libraries -----------
import bpy  # for interacting with the viewport using Python's code
#from astropy.io import fits # for reading .fits file containing plate-solved results
import math # to get sin and cos function


#----------- function to get pixel brightness -----------
### Define a helper to get pixel brightness of a given color channel based on x, y coordinates
def get_pixel_brightness(x, y, image, channel):
    
    # get image's dimension
    length = image.size[0]
    width = image.size[1]
    
    # Calculate the index of the pixel
    ### this is needed because the pixels is contained in image.pixels as a 1D list
    index = 4 * (int(y)*length + int(x))
    
    channel_map = {"R": 0, "G": 1, "B": 2}
    channel_idx = channel_map[channel]
    
    # Return the brightness of the chosen channel
    try:
        return image.pixels[index + channel_idx]
    except IndexError:
        return -1  # Return -1 if out of bounds
    

#----------- variable declaration -----------
corr_fits = "C:/Course Materials/COMP3850/Blender/plate-solved_images/corr.fits"
focal_length = 1000 # in mm
aperture = 130 # in mm
pixel_size = 0.5 # in micro-meters
channel_input = "R" # R for Red, G for Green, and B for Blue
no_directions = 32 # this specifies the number of directions to check for the length of saturated pixels
lambda_w = 650 # wavelength for different color channel - in nano-meters - user-defined 650 for R, 520 for G, 450 for B

def main():
    # calculate the Airy Disk's radius
    f = focal_length/aperture
    r_mm = 2.44*lambda_w*f*10**-3 # Airy Disk radius in micro-meters
    r_px = r_mm/pixel_size # radius in terms of number of pixels


    #----------- import data file -----------
    with fits.open(corr_fits) as hdul:
        data = [list(row) for row in hdul[1].data]
    hdul.close()


    #----------- clean all circles in the viewport -----------
    for obj in bpy.data.objects:
        if obj.name != "Grid":
            bpy.data.objects.remove(obj)



    ######################## SECTION 2 - AIRY DISK FOR REFERENCE STARS ########################

    # get the grid object
    grid = bpy.data.objects["Grid"]

    # ----------- set the scale -----------
    cell_length = (grid.scale.x * 2) / (grid.scale.x*1000)
    cell_width = (grid.scale.y * 2 )/ (grid.scale.y*1000)


    #----------- Define material for the AD circles -----------
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
    for row in data:
        x = row[0] * cell_length - grid.scale.x  # Translate and scale x-coordinate
        y = row[1] * cell_width - grid.scale.y  # Translate and scale y-coordinate
        
        # Add a circle curve for each reference star
        bpy.ops.mesh.primitive_circle_add(radius = r_px*cell_length, location = (x, y, 0))
        circle = bpy.context.active_object  # This is the mesh circle

        # Convert the mesh circle to a curve
        bpy.ops.object.convert(target = 'CURVE')
        circle = bpy.context.active_object  # This is now the curve circle

        # Adjust the curve properties
        circle.data.bevel_depth = 0.001

        # Assign colors to the AD
        if circle.data.materials:
            circle.data.materials[0] = AD_mat
        else:
            circle.data.materials.append(AD_mat)



    ######################## SECTION 3 - CREATE CIRCLES AROUND SATURATED STARS ########################

    # get the image used to make the Displace effect
    img = grid.modifiers["Stellar_Displacement"].texture.image

    # For each star's loci
    for row in data:
        
        x_loci = row[0] # loci's x coordinate
        y_loci = row[1] # loci's y coordinate
        distance_list = [] # list containing the length of the saturated region in every direction
        
        
        # loop through every direction to check the length of the saturated region
        for angle in [2*i*math.pi/no_directions for i in range(no_directions)]:
            
            x_dir = math.cos(angle) # x increment
            y_dir = math.sin(angle) # y increment
            print(x_dir)
            print(y_dir)
            
            # starting location of (x,y) coordinate
            x_current = x_loci
            y_current = y_loci
            
            # Move in the chosen direction until a non-saturated pixel is found
            while get_pixel_brightness(x_current, y_current, img, channel_input) == 1:
                x_current += x_dir
                y_current += y_dir
            
            # Calculate distance from star's loci to the non-saturated pixel at the boundary of the saturated area
            distance = math.sqrt((x_current - x_loci - 1)**2 + (y_current - y_loci - 1)**2)
            distance_list.append(distance)
        
        
        x = x_loci * cell_length - grid.scale.x # Translate and scale x-coordinate
        y = y_loci * cell_width - grid.scale.y # Translate and scale y-coordinate
        
        # Add a circle curve for each reference star
        bpy.ops.mesh.primitive_circle_add(radius = max(distance_list)*cell_length, location = (x, y, -1))
        circle = bpy.context.active_object  # This is the mesh circle

        # Convert the mesh circle to a curve
        bpy.ops.object.convert(target = 'CURVE')
        circle = bpy.context.active_object  # This is now the curve circle

        # Adjust the curve properties
        circle.data.bevel_depth = 0.001

        # Assign colors to the AD
        if circle.data.materials:
            circle.data.materials[0] = AD_mat
        else:
            circle.data.materials.append(AD_mat)


if __name__ == "__main__":
    main()


