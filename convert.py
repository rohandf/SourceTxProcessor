# SourceTxProcessor for Source 1 created by Blapman007

# Input folder must contain: Roughness, Metalness, Normalmap, Diffuse
# Output folder will have: Diffuse, Normalmap, Exponent Mask

# Input file naming convention:
# Albedo/Diffuse: "texturename_D"
# Metalness: "texturename_M"
# Normalmap: "texturename_N"
# Roughness: "texturename_R"

from PIL import Image
from PIL import ImageChops
import pillow_lut
import os

#testpath
exerelpath = '_internal/'

# directory paths
inputdir = None
outputdir = None
# input textures paths
diffusepath = None
metalpath = None
normalpath = None
roughpath = None
d = None
m = None
n = None
r = None


# step 0: introductions
def intro()-> None:
    print("========SourceTxProcessor by Blapman007========")
    print("                     1.0.0 \n")
    print("Output textures will be in a subfolder of")
    print("input folder called 'processed' \n")
    print("If issues, please message on discord or twitter")
    print("@blapman007")
    print("===============================================")
    get_input_dir()     # CALL NEXT STEP

# step 1: get input directory, where textures are stored
def get_input_dir()-> None:
    global inputdir
    inputdir = input("Input Folder: ")
    inputdir = inputdir.strip()
    if inputdir == "quit":
        return 0
    if os.path.exists(inputdir):
        print("Folder found.")
        if inputdir[-1]!='\\' or inputdir[-1]!='/':
            inputdir = inputdir + '/'
        set_output_dir()      # CALL NEXT STEP
    else:
        print("Folder not found.")
        get_input_dir()      # RUN FUNCTION AGAIN

# step 2: set output directory
def set_output_dir()-> None:
    global inputdir
    global outputdir
    outputdir = inputdir + 'processed/'
    if not os.path.exists(outputdir):
        os.mkdir(outputdir)
    print("Output Directory Set.")
    find_input_files()      # CALL NEXT STEP

# step 3: find and get file paths of textures
def find_input_files()-> None:
    global diffusepath
    global metalpath
    global normalpath
    global roughpath
    global inputdir
    global d
    global m
    global n
    global r
    print("Finding textures...")
    files=os.listdir(inputdir)
    for f in files:
        if ("_d" in f.lower()) or ("d_" in f.lower()): # Find Diffuse
            diffusepath = inputdir+f
            d=f
            print("Diffuse tga found.")
        elif ("_m" in f.lower()) or ("m_" in f.lower()): # Find Metalness
            metalpath = inputdir+f
            m=f
            print("Metalness tga found.")
        elif ("_n" in f.lower()) or ("n_" in f.lower()): # Find Normalmap
            normalpath = inputdir+f
            n=f
            print("Normalmap tga found.")
        elif ("_r" in f.lower()) or ("r_" in f.lower()): # Find Roughness
            roughpath = inputdir+f
            r=f
            print("Roughness tga found.")
    
    if diffusepath and metalpath and normalpath and roughpath:
        print("Textures have been found.")
        print("Diffuse = "+d)
        print("Metalness = "+m)
        print("Normal = "+n)
        print("Roughness = "+r)
        print("Calling function diffuse_process")
        diffuse_process()
    else:
        print("Textures not found. \n Make sure they are named correctly and are Targa .tga files.")
    
# step 4: diffuse processing
def diffuse_process()-> None:
    print("Starting diffuse processing...")
    d_im = Image.open(diffusepath)
    print("Opened diffuse...")
    m_im = Image.open(metalpath)
    print("Opened metalness...")
    # assumes that r=g=b
    m_im_r = m_im.getchannel("R") # get redchannel
    print("R channel extracted...")
    d_im.putalpha(m_im_r) # metalness[r] into alpha
    print("Diffuse alpha replaced...")
    d_im.save(outputdir+"diffuse.tga")
    print("Diffuse processing finished. Image saved.")
    print("Calling function normalmap_process")
    normalmap_process()
    
# step 5: normalmap processing
def normalmap_process()-> None:
    print("Starting normalmap processing...")
    n_im = Image.open(normalpath)
    print("Opened normals...")
    r_im = Image.open(roughpath)
    print("Opened roughness...")
    gloss = ImageChops.invert(r_im)
    print("Roughness to gloss...")
    lut = pillow_lut.load_cube_file(exerelpath+'m6ob10.cube')
    print("Loaded LUT m6ob10...")
    gloss = gloss.filter(lut)
    print("Gloss LUTted...")
    # assumes that r=g=b
    gloss_r = gloss.getchannel("R")
    print("R channel extracted...")
    n_im.putalpha(gloss_r)
    print("Normals alpha replaced...")
    n_im.save(outputdir+"normals.tga")
    print("Normals processing finished. Image saved.")
    print("Calling function exponent_process")
    exponent_process()

# step 6: exponent processing
def exponent_process()-> None:
    print("Starting exponent mask creation...")
    r_im = Image.open(roughpath)
    print("Opened roughness...")
    r_size = r_im.size
    gloss = ImageChops.invert(r_im)
    print("Roughness to gloss...")
    lut = pillow_lut.load_cube_file(exerelpath+'m24.cube')
    print("Loaded LUT m24...")
    gloss = gloss.filter(lut)
    print("Gloss LUTted...")
    gloss_r=gloss.getchannel("R")
    print("R channel extracted...")
    i_white = Image.new(mode="L",size=r_size,color="white")
    print("White image created...")
    exponent = Image.merge("RGB",(gloss_r,i_white,i_white))
    print("gloss_r white white merged rgb...")
    exponent.save(outputdir+"exponent.tga")
    print("Exponent mask creation finished. Image saved.")
    print("ALL PROCESSING FINISHED SUCCESSFULLY.")
    print("YOU MAY CLOSE THE PROGRAM, OR PROCESS ANOTHER FOLDER.")
    print("TYPE quit TO QUIT")
    get_input_dir()

intro() #kick off the chain