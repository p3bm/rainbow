import struct
import os
from parser.agilent import Agilent


# Tries to automatically identifies filetype
# Currently relies on file extension to do so
def read(filepath):
    """
    Function to read chromatogram data folders. 

    This function is the main way to use the package. 
    
    Returns a Chromatogram object based on filetype. 

    """
    ext = os.path.splitext(filepath)[1].lower() 
    
    # csv file
    # todo: check if the file is a csv by actually parsing it
    if os.path.isfile(filepath) and ext == ".csv":
        raise NotImplementedError

    # data folders
    if os.path.isdir(filepath): 
        if ext == ".d":
            return Agilent(filepath)
        elif ext == ".raw":
            raise NotImplementedError       