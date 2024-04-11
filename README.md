# SourceTxProcessor
## What is it?
This tool takes in four texture maps and performs operations on them, in order to produce textures that can be used as PseudoPBR for the Source 1 Engine.  
This tool, although built in python, does NOT require python to run on your computer.  
The end result textures are: A processed diffuse/albedo, A processed normalmap, and an exponent mask texture.  

## Prerequisites  
Texture names must have prefixes or suffixes like so:  
- Diffuse texture - d_filename.extension or filename_d.extension
- Metalness texture - m_filename.extension or filename_m.extension
- Normalmap texture - n_filename.extension or filename_n.extension
- Roughness texture - r_filename.extension or filename_r.extension

Prefixes and suffixes (d,m,n,r) are not case sensitive.

All four textures must be in the same folder.  

## Usage
1. Make sure Diffuse, Metalness, Normalmap, and Roughness textures are all in the same folder and named properly.
2. Copy the folder path.
3. Paste/type it into the terminal window when asked for a path.
4. Program will locate files and process them.
5. Output textures will be saved in the specified folder.
6. Convert the textures to vtf and create vmts using VTFEdit.

## Warnings
Similarly named textures that are not relevant must NOT be in the folder.  
They may interfere with the process.  
(if folder has textures related to body material, similarly named textures related to face must not be present. one material at a time.)  

## IN THE CASE PROGRAM DOES NOT OPEN
Security error:
Right click the app in file explorer, open properties, and there may be an option to unblock the program on your computer.  WARNING! This is a risky procedure and you should only do this for apps and devs you trust.  You may also have to disable your antivirus software.  

Error on compile, bottle.py: Find bottle.py and comment out lines 72-76
