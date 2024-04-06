# SourceTxProcessor for Source 1 created by Blapman007
# v2

from PIL import Image as pim
from PIL import ImageChops
import pillow_lut
import os
import printredirect

def print(msg):
    printredirect.print_eel(msg)

#path to assets in relation to exe, use first in exe form, use 2nd in code form
#exerelpath = '_internal/'
exerelpath = ''

# folder paths
inputpath = None
exportpath = None

# paths to each import texture
dpath = None
mpath = None
npath = None
rpath = None
# names of each file
d = None
m = None
n = None
r = None

def set_inputpath(indir)-> None:
    global inputpath
    inputpath = indir

def set_exportpath(odir)-> None:
    global exportpath
    exportpath = odir
    if exportpath[-1]!='\\' or exportpath[-1]!='/':
        exportpath = exportpath + '/'

def find_files()-> None:
    global dpath
    global mpath
    global npath
    global rpath
    global inputpath
    global d
    global m
    global n
    global r
    print("Finding textures...")
    files=os.listdir(inputpath)
    for f in files:
        if ("_d" in f.lower()) or ("d_" in f.lower()): # Find Diffuse
            dpath = inputpath+f
            d=f
            print("Diffuse texture found.")
        elif ("_m" in f.lower()) or ("m_" in f.lower()): # Find Metalness
            mpath = inputpath+f
            m=f
            print("Metalness texture found.")
        elif ("_n" in f.lower()) or ("n_" in f.lower()): # Find Normalmap
            npath = inputpath+f
            n=f
            print("Normalmap texture found.")
        elif ("_r" in f.lower()) or ("r_" in f.lower()): # Find Roughness
            rpath = inputpath+f
            r=f
            print("Roughness texture found.")

# step 4: diffuse processing
def diffuse_process()-> None:
    print("Starting diffuse processing...")
    d_im = pim.open(dpath)
    print("Opened diffuse...")
    m_im = pim.open(mpath)
    print("Opened metalness...")
    # assumes that r=g=b
    m_im_r = m_im.getchannel("R") # get redchannel
    print("R channel extracted...")
    d_im.putalpha(m_im_r) # metalness[r] into alpha
    print("Diffuse alpha replaced...")
    d_im.save(exportpath+"diffuse.tga")
    print("Diffuse processing finished. Image saved.")
    print("Calling function normalmap_process")
    
# step 5: normalmap processing
def normalmap_process()-> None:
    print("Starting normalmap processing...")
    n_im = pim.open(npath)
    print("Opened normals...")
    r_im = pim.open(rpath)
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
    n_im.save(exportpath+"normals.tga")
    print("Normals processing finished. Image saved.")
    print("Calling function exponent_process")

# step 6: exponent processing
def exponent_process()-> None:
    print("Starting exponent mask creation...")
    r_im = pim.open(rpath)
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
    i_white = pim.new(mode="L",size=r_size,color="white")
    print("White image created...")
    exponent = pim.merge("RGB",(gloss_r,i_white,i_white))
    print("gloss_r white white merged rgb...")
    exponent.save(exportpath+"exponent.tga")
    print("Exponent creation finished. Image saved.")
