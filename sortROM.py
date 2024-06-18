import os
import shutil
import zipfile

source_dir = "CHANGE_ME"

extension_to_dir = {
    ".gbc": "Game Boy Color",
    ".nes": "NES",
    ".gba": "GBA",
    ".gb": "Game Boy",
    ".nez": "NES",
    ".smc": "SNES",
    ".sfc": "SNES",
    ".smd": "Genesis",
    ".md": "Genesis",
    ".gen": "Genesis",
    ".gg": "Genesis",
    '.n64': "Nintendo 64",
    ".z64": "Nintendo 64",
    ".nds": "Nintendo DS",
    ".a26": "Atari 2600",
    ".a52": "Atari 5200",
    ".sms": "Sega Master System",
    ".a78": "Atari 7800",
    ".pce": "TurboGrafx-16",
    ".32x": "Sega 32X",
    
}

def create_new_dir(extension):
    dir_name = input(f"Enter a directory name for the file extension '{extension}': ")
    extension_to_dir[extension] = dir_name
    os.makedirs(os.path.join(source_dir, dir_name), exist_ok=True)

def remove_trailing_spaces(filename):
    dot_position = filename.rfind('.')
    
    if dot_position != -1:
        name = filename[:dot_position]
        extension = filename[dot_position:]
        
        name = name.rstrip()
        
        filename = name + extension
    
    return filename

def unpack_and_sort_files():
    for filename in os.listdir(source_dir):
        file_path = os.path.join(source_dir, filename)

        if zipfile.is_zipfile(file_path):
            with zipfile.ZipFile(file_path, "r") as zip_ref:
                zip_ref.extractall(source_dir)

           
            os.remove(file_path)

   
    for filename in os.listdir(source_dir):
        file_path = os.path.join(source_dir, filename)

        
        if os.path.isfile(file_path):
            _, extension = os.path.splitext(filename)
            if extension in extension_to_dir:
                dir_name = extension_to_dir[extension]
                dest_dir = os.path.join(source_dir, dir_name)
                os.makedirs(dest_dir, exist_ok=True)
                shutil.move(file_path, os.path.join(dest_dir, filename))
            else:
                create_new_dir(extension)
                unpack_and_sort_files()  