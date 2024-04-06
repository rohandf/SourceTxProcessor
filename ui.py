import eel
import os
import convert
import printredirect

eel.init('web')

def print(msg):
    printredirect.print_eel(msg)


@eel.expose
def output_folder_check(path: str) -> bool:
    if os.path.isdir(path):
        convert.set_exportpath(path)
        return True
    else:
        if path[-1]=='/' or path[-1]=='\\':
            h1= path[0:-1].rfind['/']
            h2= path[0:-1].rfind['\\']
            if h2>h1:
                h1=h2
            if h1 > -1:
                if os.path.exists(path[0:h1]): # if parent path of given path exists
                    os.mkdir(path) # create the folder at the end of the string.
                    convert.set_exportpath(path)
                    return True
                else:
                    return False
            
        
@eel.expose
def start_export_process(outputdir):
    convert.find_files()
    convert.diffuse_process()
    convert.normalmap_process()
    convert.exponent_process()
    print("====================")
    print("Processing finished.")
    print("====================")

@eel.expose
def input_folder_check(indir: str)-> bool:
    indir = indir.strip()
    if os.path.exists(indir):
        if indir[-1]!='\\' or indir[-1]!='/':
            indir = indir + '/'
        convert.set_inputpath(indir) # Sends input path to convert script
        print("Folder found." + indir)
        return True
        # Code Continues
    else:
        print("Folder not found." + indir)
        return False

eel.start('index.html',size=(700,800))