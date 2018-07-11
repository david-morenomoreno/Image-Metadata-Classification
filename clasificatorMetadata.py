import os
import shutil
from datetime import datetime

from PIL import Image

from pyexiftool import exiftool


def fcopy(src,DestY,DestM):
    """
    Copy file from source to dest.  dest can include an absolute or relative path
    If the path doesn't exist, it gets created
    """

    new_path = "/" #Path where save all collection

    dest_dir = os.path.join(os.path.join(new_path, DestY), DestM)
    try:
        os.makedirs(dest_dir)
    except os.error as e:
        pass
    shutil.move(src,dest_dir)



if __name__ == '__main__':

    root = "/"  #path to start to visit and get all file from folder and subdirectoy

    for path, subdirs, files in os.walk(root):
        for name in files:
            try:
                pathfile = os.path.join(path, name)
                if pathfile.endswith('.jpg') or pathfile.endswith('.png') :
                    with exiftool.ExifTool() as et:
                        metadata = et.get_metadata(pathfile)
                        dt = datetime.strptime(metadata['File:FileModifyDate'][:19], '%Y:%m:%d %H:%M:%S')

                        im = Image.open(pathfile)
                        width, height = im.size  #Remove al thumbails of photorec
                        if (width or height) <= 160:
                            os.remove(pathfile)
                        else:
                            fcopy(pathfile,str(dt.year), str(dt.month))
                else:
                    print("File Format don't accepted")
            except Exception as e:
                print(e)
                pass



